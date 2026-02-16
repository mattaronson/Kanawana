#!/usr/bin/env python3
"""
PDF Field Extractor
Extracts form field IDs and metadata from Quebec immigration PDF forms.

Usage: python pdf_field_extractor.py <form.pdf> <output.json>
"""

import json
import sys
from typing import Dict, List, Any, Optional

try:
    from PyPDF2 import PdfReader
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


def extract_fields_pypdf2(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract form fields using PyPDF2."""
    reader = PdfReader(pdf_path)
    fields = []

    if reader.get_fields() is None:
        print(f"No form fields found in {pdf_path}")
        return fields

    for name, field in reader.get_fields().items():
        field_info = {
            "field_id": name,
            "field_type": str(field.get("/FT", "Unknown")),
            "value": str(field.get("/V", "")) if field.get("/V") else "",
            "options": []
        }

        # Get field type
        ft = field.get("/FT")
        if ft:
            field_info["field_type"] = {
                "/Tx": "text",
                "/Btn": "button",
                "/Ch": "choice",
                "/Sig": "signature"
            }.get(str(ft), str(ft))

        # Get radio button options
        if field.get("/Opt"):
            field_info["options"] = [str(opt) for opt in field.get("/Opt")]

        fields.append(field_info)

    return sorted(fields, key=lambda x: x["field_id"])


def extract_fields(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract form fields from PDF."""
    if HAS_PYPDF2:
        return extract_fields_pypdf2(pdf_path)
    else:
        print("Error: PyPDF2 not installed. Run: pip install pypdf2")
        return []


def save_inventory(fields: List[Dict], output_path: str, form_name: str) -> None:
    """Save field inventory to JSON file."""
    inventory = {
        "form_name": form_name,
        "field_count": len(fields),
        "field_types": {},
        "fields": fields
    }

    # Count by type
    for f in fields:
        ft = f.get("field_type", "unknown")
        inventory["field_types"][ft] = inventory["field_types"].get(ft, 0) + 1

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(fields)} fields from {form_name}")
    print(f"Field types: {inventory['field_types']}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python pdf_field_extractor.py <form.pdf> <output.json>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    form_name = pdf_path.split("/")[-1].replace(".pdf", "")

    fields = extract_fields(pdf_path)
    save_inventory(fields, output_path, form_name)


if __name__ == "__main__":
    main()
