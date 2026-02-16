#!/usr/bin/env python3
"""
Cross-Form Field Mapper and Consistency Validator
BETA-2 Deliverable: Ensures data consistency across all 4 CAQ-related forms.

Forms covered:
- A-0506-CF: Demande de sélection temporaire (DST) - Main application
- A-2700-CF: Attestation de l'employeur - Employer attestation
- ME-0031: Engagement - Commitment form
- A-0591-A0: Annexe A - Schedule A (employer & employee versions)

Author: CAQ Form Completion Skill
Version: BETA-2
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum


class FormType(Enum):
    """Quebec immigration form types."""
    A_0506_CF = "A-0506-CF"      # Main DST application
    A_2700_CF = "A-2700-CF"      # Employer attestation
    ME_0031 = "ME-0031"          # Commitment form
    A_0591_A0 = "A-0591-A0"      # Schedule A


@dataclass
class FieldMapping:
    """Maps a data point across multiple forms."""
    data_point: str
    profile_path: Tuple[str, ...]
    form_fields: Dict[str, str]  # FormType.value -> field_id
    description: str
    validation_rule: Optional[str] = None


# Cross-form field reference mapping
# Maps shared data points to their field IDs in each form
# Field IDs are aligned with the actual form filler implementations
CROSS_FORM_FIELDS: List[FieldMapping] = [
    # ========== APPLICANT IDENTITY ==========
    FieldMapping(
        data_point="applicant_surname",
        profile_path=("personal_information", "surname"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 11046",
            FormType.A_2700_CF.value: "Champ de texte 2010",  # Worker surname in A-2700
            FormType.ME_0031.value: "Champ de texte 3001",
            FormType.A_0591_A0.value: "Champ de texte 4001",
        },
        description="Applicant family name / surname"
    ),
    FieldMapping(
        data_point="applicant_given_names",
        profile_path=("personal_information", "given_names"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 11019",
            FormType.A_2700_CF.value: "Champ de texte 2011",  # Worker given names in A-2700
            FormType.ME_0031.value: "Champ de texte 3002",
            FormType.A_0591_A0.value: "Champ de texte 4002",
        },
        description="Applicant given/first names"
    ),
    FieldMapping(
        data_point="applicant_dob",
        profile_path=("personal_information", "date_of_birth"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 1050",
            FormType.A_2700_CF.value: "Champ de texte 2012",  # Worker DOB in A-2700
            FormType.ME_0031.value: "Champ de texte 3003",
            FormType.A_0591_A0.value: "Champ de texte 4003",
        },
        description="Applicant date of birth",
        validation_rule="date_format:YYYY/MM/DD"
    ),

    # ========== EMPLOYER INFORMATION ==========
    FieldMapping(
        data_point="employer_name",
        profile_path=("employer", "company_name"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 101093",
            FormType.A_2700_CF.value: "Champ de texte 2001",  # Employer name (Section 1)
            FormType.ME_0031.value: "Champ de texte 3010",
            FormType.A_0591_A0.value: "Champ de texte 4010",
        },
        description="Quebec employer company name"
    ),
    FieldMapping(
        data_point="employer_neq",
        profile_path=("employer", "neq_number"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 101094",
            FormType.A_2700_CF.value: "Champ de texte 2002",  # NEQ in A-2700 Section 1
            FormType.ME_0031.value: "",  # May not appear on this form
            FormType.A_0591_A0.value: "Champ de texte 4011",
        },
        description="Employer NEQ (Quebec enterprise number)",
        validation_rule="neq_format:10_digits"
    ),

    # ========== JOB INFORMATION ==========
    FieldMapping(
        data_point="job_title",
        profile_path=("quebec_employment", "job_title"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 101048",
            FormType.A_2700_CF.value: "Champ de texte 2020",
            FormType.ME_0031.value: "Champ de texte 3020",
            FormType.A_0591_A0.value: "Champ de texte 4020",
        },
        description="Job title / position"
    ),
    FieldMapping(
        data_point="noc_code",
        profile_path=("quebec_employment", "noc_code"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 10113",
            FormType.A_2700_CF.value: "Champ de texte 2021",
            FormType.ME_0031.value: "",
            FormType.A_0591_A0.value: "Champ de texte 4021",
        },
        description="NOC (National Occupational Classification) code",
        validation_rule="noc_format:5_digits"
    ),
    FieldMapping(
        data_point="lmia_number",
        profile_path=("quebec_employment", "lmia_number"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 10111",
            FormType.A_2700_CF.value: "Champ de texte 2025",  # LMIA number in A-2700
            FormType.ME_0031.value: "",
            FormType.A_0591_A0.value: "Champ de texte 4022",
        },
        description="LMIA (Labour Market Impact Assessment) number"
    ),

    # ========== EMPLOYMENT DATES ==========
    FieldMapping(
        data_point="employment_start_date",
        profile_path=("quebec_employment", "start_date"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 1045",
            FormType.A_2700_CF.value: "Champ de texte 2030",
            FormType.ME_0031.value: "Champ de texte 3030",
            FormType.A_0591_A0.value: "Champ de texte 4030",
        },
        description="Employment start date",
        validation_rule="date_format:YYYY/MM/DD"
    ),
    FieldMapping(
        data_point="employment_end_date",
        profile_path=("quebec_employment", "end_date"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 1046",
            FormType.A_2700_CF.value: "Champ de texte 2031",
            FormType.ME_0031.value: "Champ de texte 3031",
            FormType.A_0591_A0.value: "Champ de texte 4031",
        },
        description="Employment end date",
        validation_rule="date_format:YYYY/MM/DD"
    ),

    # ========== WAGES ==========
    FieldMapping(
        data_point="hourly_wage",
        profile_path=("quebec_employment", "hourly_wage"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 101052",
            FormType.A_2700_CF.value: "Champ de texte 2040",
            FormType.ME_0031.value: "",
            FormType.A_0591_A0.value: "Champ de texte 4040",
        },
        description="Hourly wage offered",
        validation_rule="currency_format"
    ),

    # ========== WORK LOCATION ==========
    FieldMapping(
        data_point="work_location",
        profile_path=("quebec_employment", "work_location"),
        form_fields={
            FormType.A_0506_CF.value: "Champ de texte 101050",
            FormType.A_2700_CF.value: "Champ de texte 2023",  # Work location in A-2700
            FormType.ME_0031.value: "Champ de texte 3021",
            FormType.A_0591_A0.value: "Champ de texte 4023",
        },
        description="Work location in Quebec"
    ),
]


@dataclass
class ValidationIssue:
    """Represents a consistency issue between forms."""
    data_point: str
    description: str
    severity: str  # "error", "warning", "info"
    forms_affected: List[str]
    expected_value: str
    actual_values: Dict[str, str]


class CrossFormValidator:
    """
    Validates consistency of data across multiple CAQ form outputs.
    """

    def __init__(self, profile: Dict[str, Any]):
        """
        Initialize with source profile.

        Args:
            profile: Source client profile JSON
        """
        self.profile = profile
        self.form_outputs: Dict[str, List[Dict]] = {}
        self.issues: List[ValidationIssue] = []

    def load_form_output(self, form_type: FormType, output: List[Dict]) -> None:
        """
        Load generated field values for a form.

        Args:
            form_type: Type of form
            output: List of field value dictionaries
        """
        self.form_outputs[form_type.value] = output

    def _get_profile_value(self, path: Tuple[str, ...]) -> Any:
        """Get value from profile using path tuple."""
        current = self.profile
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    def _get_field_value(self, form_name: str, field_id: str) -> Optional[str]:
        """Get field value from form output."""
        if form_name not in self.form_outputs:
            return None

        for field in self.form_outputs[form_name]:
            if field.get("field_id") == field_id:
                return field.get("value")
        return None

    def validate_cross_form_consistency(self) -> List[ValidationIssue]:
        """
        Compare field values across forms to ensure consistency.

        Returns:
            List of ValidationIssue objects
        """
        self.issues = []

        for mapping in CROSS_FORM_FIELDS:
            expected = self._get_profile_value(mapping.profile_path)
            if expected is None:
                continue

            expected_str = str(expected)
            actual_values: Dict[str, str] = {}
            mismatched_forms: List[str] = []

            for form_name, field_id in mapping.form_fields.items():
                if not field_id:  # Skip empty mappings
                    continue
                if form_name not in self.form_outputs:
                    continue

                actual = self._get_field_value(form_name, field_id)
                if actual is not None:
                    actual_values[form_name] = actual
                    # Normalize comparison (dates, whitespace, case)
                    if not self._values_match(expected_str, actual, mapping.validation_rule):
                        mismatched_forms.append(form_name)

            if mismatched_forms:
                self.issues.append(ValidationIssue(
                    data_point=mapping.data_point,
                    description=f"{mapping.description} mismatch",
                    severity="error",
                    forms_affected=mismatched_forms,
                    expected_value=expected_str,
                    actual_values=actual_values
                ))

        return self.issues

    def _values_match(self, expected: str, actual: str, rule: Optional[str]) -> bool:
        """
        Compare values with optional validation rule.

        Args:
            expected: Expected value from profile
            actual: Actual value from form output
            rule: Optional validation rule

        Returns:
            True if values match
        """
        # Normalize strings
        exp_norm = expected.strip().upper()
        act_norm = actual.strip().upper()

        # Direct match
        if exp_norm == act_norm:
            return True

        # Date format variations (2025-04-01 vs 2025/04/01)
        if rule and "date_format" in rule:
            exp_clean = exp_norm.replace("-", "/")
            act_clean = act_norm.replace("-", "/")
            return exp_clean == act_clean

        return False

    def validate_required_fields(self, form_type: FormType) -> List[ValidationIssue]:
        """
        Check that all required fields are populated.

        Args:
            form_type: Form to validate

        Returns:
            List of issues for missing required fields
        """
        issues = []
        form_name = form_type.value

        if form_name not in self.form_outputs:
            issues.append(ValidationIssue(
                data_point="form_output",
                description=f"No output loaded for {form_name}",
                severity="error",
                forms_affected=[form_name],
                expected_value="populated",
                actual_values={form_name: "missing"}
            ))
            return issues

        # Check for empty values (except N/A which is valid)
        for field in self.form_outputs[form_name]:
            value = field.get("value", "")
            if value == "" and "N/A" not in field.get("description", ""):
                issues.append(ValidationIssue(
                    data_point=field.get("field_id", "unknown"),
                    description=f"Empty field: {field.get('description', 'Unknown')}",
                    severity="warning",
                    forms_affected=[form_name],
                    expected_value="populated",
                    actual_values={form_name: "empty"}
                ))

        return issues

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive validation report.

        Returns:
            Report dictionary
        """
        all_issues = self.validate_cross_form_consistency()

        # Add required field checks for each loaded form
        for form_name in self.form_outputs:
            form_type = FormType(form_name)
            all_issues.extend(self.validate_required_fields(form_type))

        # Summarize by severity
        summary = {
            "error": 0,
            "warning": 0,
            "info": 0
        }
        for issue in all_issues:
            summary[issue.severity] = summary.get(issue.severity, 0) + 1

        return {
            "forms_validated": list(self.form_outputs.keys()),
            "total_issues": len(all_issues),
            "summary": summary,
            "issues": [
                {
                    "data_point": i.data_point,
                    "description": i.description,
                    "severity": i.severity,
                    "forms_affected": i.forms_affected,
                    "expected": i.expected_value,
                    "actual": i.actual_values
                }
                for i in all_issues
            ]
        }


def update_field_mapping(form_type: FormType, field_inventory: Dict) -> None:
    """
    Update CROSS_FORM_FIELDS with extracted field IDs.

    This function should be called after extracting field IDs from a PDF
    to update the mapping with actual field identifiers.

    Args:
        form_type: Which form was extracted
        field_inventory: Extracted field inventory
    """
    # Implementation: Match fields by pattern/content to update mappings
    # This requires analyzing the extracted field names and matching them
    # to the data points they represent
    pass


def main():
    """Demo usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python cross_form_mapper.py <profile.json> [form_output.json ...]")
        print("\nThis module validates cross-form consistency.")
        print("\nExample:")
        print("  python cross_form_mapper.py profile.json a0506_output.json a2700_output.json")
        sys.exit(0)

    # Load profile
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        profile = json.load(f)

    validator = CrossFormValidator(profile)

    # Load form outputs
    for i, output_path in enumerate(sys.argv[2:]):
        with open(output_path, 'r', encoding='utf-8') as f:
            output = json.load(f)
        # Determine form type from filename
        if "0506" in output_path:
            validator.load_form_output(FormType.A_0506_CF, output)
        elif "2700" in output_path:
            validator.load_form_output(FormType.A_2700_CF, output)
        elif "0031" in output_path:
            validator.load_form_output(FormType.ME_0031, output)
        elif "0591" in output_path:
            validator.load_form_output(FormType.A_0591_A0, output)

    # Run validation
    report = validator.generate_report()

    print(json.dumps(report, indent=2, ensure_ascii=False))

    # Exit with error code if issues found
    if report["summary"]["error"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
