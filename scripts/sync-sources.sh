#!/usr/bin/env bash
#
# sync-sources.sh — Download registered sources into sources/cache/
#
# Run this on your LOCAL machine (not in the claude.ai sandbox).
# It reads sources/sources.json and downloads any source that has an
# origin_url but no cached file on disk.
#
# Usage:
#   bash scripts/sync-sources.sh            # from project root
#   bash scripts/sync-sources.sh --dry-run  # show what would be fetched
#   bash scripts/sync-sources.sh --force    # re-download even if cached
#
# Requirements: jq, curl
# Optional: lynx or w3m (for clean web page text extraction)

set -euo pipefail

# ── Config ──────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCES_JSON="$PROJECT_ROOT/sources/sources.json"
CACHE_BASE="$PROJECT_ROOT/sources/cache"

DRY_RUN=false
FORCE=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --force)   FORCE=true ;;
    --help|-h)
      echo "Usage: bash scripts/sync-sources.sh [--dry-run] [--force]"
      echo "  --dry-run  Show what would be downloaded without fetching"
      echo "  --force    Re-download even if cache file exists"
      exit 0
      ;;
  esac
done

# ── Dependency check ────────────────────────────────────────────────────────
if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is required. Install with: brew install jq (macOS) or apt install jq (Linux)"
  exit 1
fi
if ! command -v curl &>/dev/null; then
  echo "ERROR: curl is required."
  exit 1
fi

# Prefer lynx for HTML-to-text, fall back to w3m, then raw curl
HTML_TO_TEXT=""
if command -v lynx &>/dev/null; then
  HTML_TO_TEXT="lynx"
elif command -v w3m &>/dev/null; then
  HTML_TO_TEXT="w3m"
fi

# ── Counters ────────────────────────────────────────────────────────────────
fetched=0
skipped=0
failed=0
no_url=0

# ── Helper: extract Internet Archive item ID from URL ───────────────────────
ia_item_id() {
  local url="$1"
  # https://archive.org/details/ITEM_ID → ITEM_ID
  echo "$url" | sed -E 's|https?://archive\.org/details/||; s|/.*||'
}

# ── Helper: generate cache_path from source_id if none registered ───────────
generate_cache_path() {
  local source_id="$1"
  local origin="$2"
  local type="$3"

  case "$origin" in
    internet_archive)
      case "$type" in
        periodical) echo "sources/cache/green-triangle/${source_id#src_}.txt" ;;
        *)          echo "sources/cache/web-pages/${source_id#src_}.txt" ;;
      esac
      ;;
    *)
      echo "sources/cache/web-pages/${source_id#src_}.txt"
      ;;
  esac
}

# ── Helper: download a single source ────────────────────────────────────────
fetch_source() {
  local source_id="$1"
  local origin="$2"
  local origin_url="$3"
  local cache_path="$4"
  local type="$5"
  local title="$6"

  local full_path="$PROJECT_ROOT/$cache_path"
  local dir
  dir="$(dirname "$full_path")"

  # Skip if already cached (unless --force)
  if [[ -f "$full_path" ]] && [[ "$FORCE" != true ]]; then
    echo "  SKIP  $source_id (cached: $cache_path)"
    ((skipped++))
    return
  fi

  if [[ "$DRY_RUN" == true ]]; then
    echo "  WOULD FETCH  $source_id → $cache_path"
    echo "    URL: $origin_url"
    return
  fi

  mkdir -p "$dir"

  case "$origin" in
    internet_archive)
      local item_id
      item_id="$(ia_item_id "$origin_url")"

      # Try OCR text first (most useful for our purposes)
      local djvu_url="https://archive.org/download/${item_id}/${item_id}_djvu.txt"
      echo "  FETCH $source_id"
      echo "    Trying: $djvu_url"

      if curl -sL --fail -o "$full_path" "$djvu_url" 2>/dev/null; then
        local size
        size=$(wc -c < "$full_path" | tr -d ' ')
        if [[ "$size" -gt 100 ]]; then
          echo "    OK    ${size} bytes → $cache_path"
          ((fetched++))
          return
        fi
        # Too small — probably an error page
        rm -f "$full_path"
      fi

      # Try alternate filename patterns common on IA
      # Some items use spaces or different naming
      for suffix in "_djvu.txt" ".txt" "_text.txt"; do
        local alt_url="https://archive.org/download/${item_id}/${item_id}${suffix}"
        if curl -sL --fail -o "$full_path" "$alt_url" 2>/dev/null; then
          local alt_size
          alt_size=$(wc -c < "$full_path" | tr -d ' ')
          if [[ "$alt_size" -gt 100 ]]; then
            echo "    OK    ${alt_size} bytes → $cache_path (via ${suffix})"
            ((fetched++))
            return
          fi
          rm -f "$full_path"
        fi
      done

      # Try the metadata API to find the actual text file name
      echo "    Trying metadata API..."
      local meta_json
      meta_json=$(curl -sL "https://archive.org/metadata/${item_id}/files" 2>/dev/null || echo "")
      if [[ -n "$meta_json" ]]; then
        local txt_file
        txt_file=$(echo "$meta_json" | jq -r '.result[]? | select(.name | test("_djvu\\.txt$|_text\\.txt$|\\.txt$")) | .name' 2>/dev/null | head -1)
        if [[ -n "$txt_file" && "$txt_file" != "null" ]]; then
          local meta_url="https://archive.org/download/${item_id}/${txt_file}"
          echo "    Found via metadata: $txt_file"
          if curl -sL --fail -o "$full_path" "$meta_url" 2>/dev/null; then
            local meta_size
            meta_size=$(wc -c < "$full_path" | tr -d ' ')
            if [[ "$meta_size" -gt 100 ]]; then
              echo "    OK    ${meta_size} bytes → $cache_path"
              ((fetched++))
              return
            fi
            rm -f "$full_path"
          fi
        fi
      fi

      echo "    FAIL  Could not download text for $item_id"
      ((failed++))
      ;;

    web|concordia_archives)
      echo "  FETCH $source_id"
      echo "    URL: $origin_url"

      if [[ "$origin_url" =~ \.pdf$ ]] || [[ "$origin_url" =~ \.pdf\? ]]; then
        # PDF — download as-is
        local pdf_path="${full_path%.txt}.pdf"
        mkdir -p "$(dirname "$pdf_path")"
        if curl -sL --fail -o "$pdf_path" "$origin_url" 2>/dev/null; then
          local pdf_size
          pdf_size=$(wc -c < "$pdf_path" | tr -d ' ')
          echo "    OK    ${pdf_size} bytes → ${cache_path%.txt}.pdf"
          ((fetched++))
        else
          echo "    FAIL  Could not download PDF"
          rm -f "$pdf_path"
          ((failed++))
        fi
      else
        # Web page — extract clean text
        if [[ "$HTML_TO_TEXT" == "lynx" ]]; then
          if curl -sL --fail "$origin_url" 2>/dev/null | lynx -stdin -dump -nolist > "$full_path" 2>/dev/null; then
            local web_size
            web_size=$(wc -c < "$full_path" | tr -d ' ')
            if [[ "$web_size" -gt 50 ]]; then
              echo "    OK    ${web_size} bytes → $cache_path"
              ((fetched++))
              return
            fi
            rm -f "$full_path"
          fi
        elif [[ "$HTML_TO_TEXT" == "w3m" ]]; then
          if curl -sL --fail "$origin_url" 2>/dev/null | w3m -T text/html -dump > "$full_path" 2>/dev/null; then
            local w3m_size
            w3m_size=$(wc -c < "$full_path" | tr -d ' ')
            if [[ "$w3m_size" -gt 50 ]]; then
              echo "    OK    ${w3m_size} bytes → $cache_path"
              ((fetched++))
              return
            fi
            rm -f "$full_path"
          fi
        fi

        # Fallback: raw curl (HTML, but still useful)
        if curl -sL --fail -o "$full_path" "$origin_url" 2>/dev/null; then
          local raw_size
          raw_size=$(wc -c < "$full_path" | tr -d ' ')
          if [[ "$raw_size" -gt 50 ]]; then
            echo "    OK    ${raw_size} bytes → $cache_path (raw HTML)"
            ((fetched++))
          else
            echo "    FAIL  Empty or too small response"
            rm -f "$full_path"
            ((failed++))
          fi
        else
          echo "    FAIL  Could not download"
          rm -f "$full_path"
          ((failed++))
        fi
      fi
      ;;

    *)
      echo "  SKIP  $source_id (origin: $origin — not auto-fetchable)"
      ((skipped++))
      ;;
  esac
}

# ── Main ────────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════════════"
echo "  Kanawana Source Sync"
echo "  Project: $PROJECT_ROOT"
echo "  Sources: $SOURCES_JSON"
if [[ "$DRY_RUN" == true ]]; then
  echo "  Mode:    DRY RUN"
fi
if [[ "$FORCE" == true ]]; then
  echo "  Mode:    FORCE (re-downloading all)"
fi
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Count total sources
total=$(jq '.sources | length' "$SOURCES_JSON")
echo "Found $total registered sources."
echo ""

# Process each source
jq -c '.sources[]' "$SOURCES_JSON" | while IFS= read -r source; do
  source_id=$(echo "$source" | jq -r '.source_id')
  origin=$(echo "$source" | jq -r '.origin')
  origin_url=$(echo "$source" | jq -r '.origin_url // empty')
  cache_path=$(echo "$source" | jq -r '.cache_path // empty')
  type=$(echo "$source" | jq -r '.type')
  title=$(echo "$source" | jq -r '.title')

  # Skip if no URL
  if [[ -z "$origin_url" ]]; then
    echo "  SKIP  $source_id (no origin_url)"
    ((no_url++))
    continue
  fi

  # Skip catalog references that are just finding aid pages (not downloadable content)
  if [[ "$type" == "catalog_reference" ]] && [[ "$origin" == "concordia_archives" ]]; then
    # Only fetch if it has a dedicated cache_path (like the full AtoM extraction)
    if [[ -z "$cache_path" ]]; then
      echo "  SKIP  $source_id (catalog reference — no cached content expected)"
      ((skipped++))
      continue
    fi
  fi

  # Generate cache_path if not set
  if [[ -z "$cache_path" ]]; then
    cache_path=$(generate_cache_path "$source_id" "$origin" "$type")
    echo "  NOTE  Generated cache_path: $cache_path"
  fi

  fetch_source "$source_id" "$origin" "$origin_url" "$cache_path" "$type" "$title"
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Summary"
echo "  Fetched:   $fetched"
echo "  Skipped:   $skipped"
echo "  Failed:    $failed"
echo "  No URL:    $no_url"
echo "═══════════════════════════════════════════════════════════════"

if [[ "$fetched" -gt 0 ]] && [[ "$DRY_RUN" != true ]]; then
  echo ""
  echo "Next steps — commit cached sources to git so they're available in future sessions:"
  echo ""
  echo "  cd $PROJECT_ROOT"
  echo "  git add sources/cache/"
  echo "  git commit -m 'Add cached source texts from sync-sources.sh'"
  echo "  git push"
  echo ""
fi
