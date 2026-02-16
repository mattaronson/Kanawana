#!/usr/bin/env python3
"""
CAQ Form Suite
Unified interface for filling all 4 CAQ-related forms with cross-form validation.

Forms:
- A-0506-CF: Main DST application
- A-2700-CF: Employer attestation
- ME-0031: Worker commitment
- A-0591-A0: Schedule A (supplemental details)

Author: CAQ Form Completion Skill
Version: BETA-2
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Import form fillers
from caq_form_filler_v6 import CAQFormFillerV6
from form_filler_a2700 import A2700FormFiller
from form_filler_me0031 import ME0031FormFiller
from form_filler_a0591 import A0591FormFiller
from cross_form_mapper import CrossFormValidator, FormType


@dataclass
class FormOutput:
    """Container for form fill output."""
    form_name: str
    form_type: FormType
    field_count: int
    fields: List[Dict[str, Any]]
    output_path: Optional[str] = None


class CAQFormSuite:
    """
    Unified form filling suite for CAQ applications.
    Fills all 4 forms from a single profile and validates consistency.
    """

    def __init__(self, profile: Dict[str, Any]):
        """
        Initialize with client profile.

        Args:
            profile: Complete client profile dictionary
        """
        self.profile = profile
        self.outputs: Dict[str, FormOutput] = {}
        self.validation_report: Optional[Dict] = None

    def fill_a0506(self) -> FormOutput:
        """Fill main DST application form."""
        filler = CAQFormFillerV6(self.profile)
        fields = filler.fill_all()

        output = FormOutput(
            form_name="A-0506-CF",
            form_type=FormType.A_0506_CF,
            field_count=len(fields),
            fields=fields
        )
        self.outputs[FormType.A_0506_CF.value] = output
        return output

    def fill_a2700(self) -> FormOutput:
        """Fill employer attestation form."""
        filler = A2700FormFiller(self.profile)
        fields = filler.fill_all()

        output = FormOutput(
            form_name="A-2700-CF",
            form_type=FormType.A_2700_CF,
            field_count=len(fields),
            fields=fields
        )
        self.outputs[FormType.A_2700_CF.value] = output
        return output

    def fill_me0031(self) -> FormOutput:
        """Fill commitment form."""
        filler = ME0031FormFiller(self.profile)
        fields = filler.fill_all()

        output = FormOutput(
            form_name="ME-0031",
            form_type=FormType.ME_0031,
            field_count=len(fields),
            fields=fields
        )
        self.outputs[FormType.ME_0031.value] = output
        return output

    def fill_a0591(self) -> FormOutput:
        """Fill Schedule A form."""
        filler = A0591FormFiller(self.profile)
        fields = filler.fill_all()

        output = FormOutput(
            form_name="A-0591-A0",
            form_type=FormType.A_0591_A0,
            field_count=len(fields),
            fields=fields
        )
        self.outputs[FormType.A_0591_A0.value] = output
        return output

    def fill_all_forms(self) -> Dict[str, FormOutput]:
        """
        Fill all 4 forms from the profile.

        Returns:
            Dictionary of form outputs keyed by form type
        """
        self.fill_a0506()
        self.fill_a2700()
        self.fill_me0031()
        self.fill_a0591()

        return self.outputs

    def validate_consistency(self) -> Dict[str, Any]:
        """
        Validate cross-form consistency.

        Returns:
            Validation report dictionary
        """
        validator = CrossFormValidator(self.profile)

        # Load all form outputs into validator
        for form_type_str, output in self.outputs.items():
            form_type = FormType(form_type_str)
            validator.load_form_output(form_type, output.fields)

        self.validation_report = validator.generate_report()
        return self.validation_report

    def save_outputs(self, output_dir: str) -> Dict[str, str]:
        """
        Save all form outputs to JSON files.

        Args:
            output_dir: Directory to save output files

        Returns:
            Dictionary of form type -> output file path
        """
        os.makedirs(output_dir, exist_ok=True)
        paths = {}

        for form_type_str, output in self.outputs.items():
            filename = f"{form_type_str.lower().replace('-', '_')}_fields.json"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output.fields, f, ensure_ascii=False, indent=2)

            output.output_path = filepath
            paths[form_type_str] = filepath

        return paths

    def save_validation_report(self, filepath: str) -> None:
        """
        Save validation report to JSON file.

        Args:
            filepath: Output file path
        """
        if self.validation_report is None:
            self.validate_consistency()

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.validation_report, f, ensure_ascii=False, indent=2)

    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary of all form fills.

        Returns:
            Summary dictionary
        """
        if self.validation_report is None:
            self.validate_consistency()

        total_fields = sum(o.field_count for o in self.outputs.values())

        summary = {
            "generated_at": datetime.now().isoformat(),
            "profile_name": f"{self.profile.get('personal_information', {}).get('surname', 'Unknown')}, "
                           f"{self.profile.get('personal_information', {}).get('given_names', 'Unknown')}",
            "forms_filled": len(self.outputs),
            "total_fields": total_fields,
            "form_details": {},
            "validation": {
                "status": "pass" if self.validation_report["summary"]["error"] == 0 else "fail",
                "errors": self.validation_report["summary"]["error"],
                "warnings": self.validation_report["summary"]["warning"]
            }
        }

        for form_type_str, output in self.outputs.items():
            summary["form_details"][form_type_str] = {
                "name": output.form_name,
                "fields": output.field_count,
                "output_path": output.output_path
            }

        return summary


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("CAQ Form Suite - Fill all 4 CAQ forms from a single profile")
        print()
        print("Usage: python caq_form_suite.py <profile.json> [output_dir]")
        print()
        print("Arguments:")
        print("  profile.json  Path to client profile JSON file")
        print("  output_dir    Directory for output files (default: ./output)")
        print()
        print("Output files:")
        print("  - a_0506_cf_fields.json   (Main DST application)")
        print("  - a_2700_cf_fields.json   (Employer attestation)")
        print("  - me_0031_fields.json     (Commitment form)")
        print("  - a_0591_a0_fields.json   (Schedule A)")
        print("  - validation_report.json  (Cross-form consistency)")
        print("  - summary.json            (Overall summary)")
        sys.exit(0)

    profile_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"

    # Load profile
    print(f"Loading profile from: {profile_path}")
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile = json.load(f)

    # Initialize suite
    suite = CAQFormSuite(profile)

    # Fill all forms
    print("\nFilling forms...")
    suite.fill_all_forms()

    for form_type, output in suite.outputs.items():
        print(f"  {output.form_name}: {output.field_count} fields")

    # Save outputs
    print(f"\nSaving outputs to: {output_dir}")
    paths = suite.save_outputs(output_dir)

    # Validate consistency
    print("\nValidating cross-form consistency...")
    report = suite.validate_consistency()

    print(f"  Errors: {report['summary']['error']}")
    print(f"  Warnings: {report['summary']['warning']}")

    # Save validation report
    report_path = os.path.join(output_dir, "validation_report.json")
    suite.save_validation_report(report_path)
    print(f"  Report saved: {report_path}")

    # Save summary
    summary = suite.generate_summary()
    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"  Summary saved: {summary_path}")

    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Profile: {summary['profile_name']}")
    print(f"Forms filled: {summary['forms_filled']}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Validation: {summary['validation']['status'].upper()}")

    if report['summary']['error'] > 0:
        print("\nConsistency issues found:")
        for issue in report['issues'][:5]:  # Show first 5
            print(f"  - {issue['description']}: {issue['data_point']}")
        if len(report['issues']) > 5:
            print(f"  ... and {len(report['issues']) - 5} more")
        sys.exit(1)
    else:
        print("\nAll forms filled successfully with consistent data!")
        sys.exit(0)


if __name__ == "__main__":
    main()
