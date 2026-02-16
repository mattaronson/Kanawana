# sync-sources.ps1 — Download registered sources into sources/cache/
#
# Run this on your LOCAL Windows machine from the project root.
# It reads sources/sources.json and downloads any source that has an
# origin_url but no cached file on disk.
#
# Usage:
#   .\scripts\sync-sources.ps1              # download missing sources
#   .\scripts\sync-sources.ps1 -DryRun      # show what would be fetched
#   .\scripts\sync-sources.ps1 -Force       # re-download even if cached
#
# Requirements: PowerShell 5.1+, internet access

param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Continue"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$SourcesJson = Join-Path $ProjectRoot "sources\sources.json"
$CacheBase = Join-Path $ProjectRoot "sources\cache"

# Counters
$fetched = 0
$skipped = 0
$failed = 0
$noUrl = 0

function Get-IAItemId {
    param([string]$Url)
    # https://archive.org/details/ITEM_ID -> ITEM_ID
    if ($Url -match "archive\.org/details/([^/]+)") {
        return $Matches[1]
    }
    return $null
}

function Get-GeneratedCachePath {
    param(
        [string]$SourceId,
        [string]$Origin,
        [string]$Type
    )
    $name = $SourceId -replace "^src_", ""
    if ($Origin -eq "internet_archive") {
        if ($Type -eq "periodical") {
            return "sources/cache/green-triangle/$name.txt"
        }
    }
    return "sources/cache/web-pages/$name.txt"
}

function Fetch-Source {
    param(
        [string]$SourceId,
        [string]$Origin,
        [string]$OriginUrl,
        [string]$CachePath,
        [string]$Type,
        [string]$Title
    )

    $fullPath = Join-Path $ProjectRoot ($CachePath -replace "/", "\")
    $dir = Split-Path -Parent $fullPath

    # Skip if already cached (unless -Force)
    if ((Test-Path $fullPath) -and -not $Force) {
        Write-Host "  SKIP  $SourceId (cached: $CachePath)" -ForegroundColor DarkGray
        $script:skipped++
        return
    }

    if ($DryRun) {
        Write-Host "  WOULD FETCH  $SourceId -> $CachePath" -ForegroundColor Yellow
        Write-Host "    URL: $OriginUrl" -ForegroundColor DarkYellow
        return
    }

    # Ensure directory exists
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    switch ($Origin) {
        "internet_archive" {
            $itemId = Get-IAItemId $OriginUrl
            if (-not $itemId) {
                Write-Host "  FAIL  $SourceId (could not parse item ID from URL)" -ForegroundColor Red
                $script:failed++
                return
            }

            Write-Host "  FETCH $SourceId" -ForegroundColor Cyan

            # Try common text file URL patterns
            $suffixes = @("_djvu.txt", ".txt", "_text.txt")
            $success = $false

            foreach ($suffix in $suffixes) {
                $url = "https://archive.org/download/$itemId/$itemId$suffix"
                Write-Host "    Trying: $url" -ForegroundColor DarkGray

                try {
                    $response = Invoke-WebRequest -Uri $url -OutFile $fullPath -PassThru -ErrorAction Stop
                    $size = (Get-Item $fullPath).Length

                    if ($size -gt 100) {
                        Write-Host "    OK    $size bytes -> $CachePath" -ForegroundColor Green
                        $script:fetched++
                        $success = $true
                        break
                    }
                    Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
                }
                catch {
                    Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
                }
            }

            if (-not $success) {
                # Try the metadata API to find actual text file name
                Write-Host "    Trying metadata API..." -ForegroundColor DarkGray
                try {
                    $metaUrl = "https://archive.org/metadata/$itemId/files"
                    $meta = Invoke-RestMethod -Uri $metaUrl -ErrorAction Stop
                    $txtFile = $meta.result | Where-Object {
                        $_.name -match "(_djvu\.txt|_text\.txt|\.txt)$"
                    } | Select-Object -First 1

                    if ($txtFile) {
                        $downloadUrl = "https://archive.org/download/$itemId/$($txtFile.name)"
                        Write-Host "    Found via metadata: $($txtFile.name)" -ForegroundColor DarkGray

                        try {
                            Invoke-WebRequest -Uri $downloadUrl -OutFile $fullPath -ErrorAction Stop
                            $size = (Get-Item $fullPath).Length
                            if ($size -gt 100) {
                                Write-Host "    OK    $size bytes -> $CachePath" -ForegroundColor Green
                                $script:fetched++
                                $success = $true
                            }
                            else {
                                Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
                            }
                        }
                        catch {
                            Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
                        }
                    }
                }
                catch {}
            }

            if (-not $success) {
                Write-Host "    FAIL  Could not download text for $itemId" -ForegroundColor Red
                $script:failed++
            }
        }

        { $_ -in "web", "concordia_archives" } {
            Write-Host "  FETCH $SourceId" -ForegroundColor Cyan
            Write-Host "    URL: $OriginUrl" -ForegroundColor DarkGray

            try {
                Invoke-WebRequest -Uri $OriginUrl -OutFile $fullPath -ErrorAction Stop
                $size = (Get-Item $fullPath).Length

                if ($size -gt 50) {
                    Write-Host "    OK    $size bytes -> $CachePath" -ForegroundColor Green
                    $script:fetched++
                }
                else {
                    Write-Host "    FAIL  Empty or too small response" -ForegroundColor Red
                    Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
                    $script:failed++
                }
            }
            catch {
                Write-Host "    FAIL  $($_.Exception.Message)" -ForegroundColor Red
                Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
                $script:failed++
            }
        }

        default {
            Write-Host "  SKIP  $SourceId (origin: $Origin - not auto-fetchable)" -ForegroundColor DarkGray
            $script:skipped++
        }
    }
}

# ── Main ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "================================================================" -ForegroundColor White
Write-Host "  Kanawana Source Sync" -ForegroundColor White
Write-Host "  Project: $ProjectRoot" -ForegroundColor White
if ($DryRun) {
    Write-Host "  Mode:    DRY RUN" -ForegroundColor Yellow
}
if ($Force) {
    Write-Host "  Mode:    FORCE (re-downloading all)" -ForegroundColor Yellow
}
Write-Host "================================================================" -ForegroundColor White
Write-Host ""

# Load sources
$sources = (Get-Content $SourcesJson -Raw | ConvertFrom-Json).sources
Write-Host "Found $($sources.Count) registered sources."
Write-Host ""

foreach ($source in $sources) {
    $sourceId = $source.source_id
    $origin = $source.origin
    $originUrl = $source.origin_url
    $cachePath = $source.cache_path
    $type = $source.type
    $title = $source.title

    # Skip if no URL
    if (-not $originUrl) {
        Write-Host "  SKIP  $sourceId (no origin_url)" -ForegroundColor DarkGray
        $noUrl++
        continue
    }

    # Skip catalog references without dedicated cache paths
    if ($type -eq "catalog_reference" -and $origin -eq "concordia_archives" -and -not $cachePath) {
        Write-Host "  SKIP  $sourceId (catalog reference)" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    # Generate cache_path if not set
    if (-not $cachePath) {
        $cachePath = Get-GeneratedCachePath $sourceId $origin $type
        Write-Host "  NOTE  Generated cache_path: $cachePath" -ForegroundColor DarkYellow
    }

    Fetch-Source $sourceId $origin $originUrl $cachePath $type $title
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor White
Write-Host "  Summary" -ForegroundColor White
Write-Host "  Fetched:   $fetched" -ForegroundColor Green
Write-Host "  Skipped:   $skipped" -ForegroundColor DarkGray
Write-Host "  Failed:    $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "DarkGray" })
Write-Host "  No URL:    $noUrl" -ForegroundColor DarkGray
Write-Host "================================================================" -ForegroundColor White

if ($fetched -gt 0 -and -not $DryRun) {
    Write-Host ""
    Write-Host "Next steps - commit cached sources to git:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  git add sources/cache/" -ForegroundColor White
    Write-Host "  git commit -m 'Add cached source texts from sync-sources'" -ForegroundColor White
    Write-Host "  git push" -ForegroundColor White
    Write-Host ""
}
