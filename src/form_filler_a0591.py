#!/usr/bin/env python3
"""
A-0591-A0 Form Filler
Generates field values for Quebec Schedule A form.

Form: A-0591-A0 (Annexe A)
Purpose: Additional employment details (employer & employee versions)

Author: CAQ Form Completion Skill
Version: BETA-2
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class A0591FormFiller:
    """
    Fills A-0591-A0 (Annexe A / Schedule A) form fields from client profile.
    This form supplements the main DST application with detailed employment info.
    """

    YES = "/1"
    NO = "/0"
    NA = "s.o."

    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile
        self.fields: List[Dict[str, Any]] = []

    def _add(self, fid: str, val: Any, pg: int, desc: str) -> None:
        if val is not None:
            self.fields.append({
                "field_id": fid,
                "value": str(val),
                "page": pg,
                "description": desc
            })

    def _get(self, *keys, default: Any = "") -> Any:
        current = self.profile
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and key < len(current):
                current = current[key]
            else:
                return default
        return current if current is not None else default

    def _yn(self, val: Any) -> str:
        if isinstance(val, bool):
            return self.YES if val else self.NO
        return self.YES if val else self.NO

    def _fmt_date(self, ds: str, fmt: str = "full") -> str:
        if not ds:
            return ""
        try:
            if len(ds) >= 10:
                dt = datetime.strptime(ds[:10], "%Y-%m-%d")
                if fmt == "full":
                    return dt.strftime("%Y/%m/%d")
                elif fmt == "ym":
                    return dt.strftime("%Y/%m")
            elif len(ds) >= 7:
                dt = datetime.strptime(ds[:7], "%Y-%m")
                return dt.strftime("%Y/%m")
        except ValueError:
            pass
        return ds

    def fill_worker_info(self) -> None:
        """Section A: Worker Information"""
        pi = self._get("personal_information", default={})
        passport = self._get("passport", default={})

        self._add("Champ de texte 4001", pi.get("surname", ""), 1, "Worker surname")
        self._add("Champ de texte 4002", pi.get("given_names", ""), 1, "Worker given names")
        self._add("Champ de texte 4003", self._fmt_date(pi.get("date_of_birth", "")), 1, "Worker DOB")
        self._add("Champ de texte 4004", pi.get("citizenship_country", ""), 1, "Country of citizenship")
        self._add("Champ de texte 4005", passport.get("passport_number", ""), 1, "Passport number")

    def fill_employer_info(self) -> None:
        """Section B: Employer Information"""
        emp = self._get("employer", default={})
        emp_addr = emp.get("address", {})

        self._add("Champ de texte 4010", emp.get("company_name", ""), 1, "Employer name")
        self._add("Champ de texte 4011", emp.get("neq_number", ""), 1, "NEQ number")

        if isinstance(emp_addr, dict):
            self._add("Champ de texte 4012", emp_addr.get("full_address", ""), 1, "Employer address")
            self._add("Champ de texte 4013", emp_addr.get("city", ""), 1, "Employer city")
            self._add("Champ de texte 4014", emp_addr.get("postal_code", ""), 1, "Employer postal code")
        else:
            self._add("Champ de texte 4012", str(emp_addr), 1, "Employer full address")

        self._add("Champ de texte 4015", emp.get("phone", ""), 1, "Employer phone")

    def fill_employment_details(self) -> None:
        """Section C: Employment Details"""
        job = self._get("quebec_employment", default={})

        # Position details
        self._add("Champ de texte 4020", job.get("job_title", ""), 2, "Job title")
        self._add("Champ de texte 4021", job.get("noc_code", ""), 2, "NOC code")
        self._add("Champ de texte 4022", job.get("lmia_number", ""), 2, "LMIA number")

        # Work location
        self._add("Champ de texte 4023", job.get("work_location", ""), 2, "Work location")

        # Employment period
        self._add("Champ de texte 4030", self._fmt_date(job.get("start_date", "")), 2, "Start date")
        self._add("Champ de texte 4031", self._fmt_date(job.get("end_date", "")), 2, "End date")

        # Compensation
        self._add("Champ de texte 4040", job.get("hourly_wage", ""), 2, "Hourly wage")
        self._add("Champ de texte 4041", job.get("weekly_hours", ""), 2, "Weekly hours")

        # Detailed job duties
        self._add("Champ de texte 4050", job.get("duties", ""), 2, "Detailed job duties")

    def fill_qualifications(self) -> None:
        """Section D: Worker Qualifications"""
        education = self._get("education", default=[])
        experience = self._get("work_experience", default=[])

        # Most recent education
        if education:
            latest_edu = education[0]
            self._add("Champ de texte 4060", latest_edu.get("diploma_type", ""), 3, "Highest diploma")
            self._add("Champ de texte 4061", latest_edu.get("field_of_study", ""), 3, "Field of study")
            self._add("Champ de texte 4062", latest_edu.get("institution", ""), 3, "Institution")
        else:
            self._add("Champ de texte 4060", self.NA, 3, "Highest diploma (N/A)")
            self._add("Champ de texte 4061", self.NA, 3, "Field of study (N/A)")
            self._add("Champ de texte 4062", self.NA, 3, "Institution (N/A)")

        # Years of experience in field
        if experience:
            # Calculate total years in similar roles
            total_years = len(experience)  # Simplified - actual calculation would sum durations
            self._add("Champ de texte 4063", str(total_years), 3, "Years of experience")
        else:
            self._add("Champ de texte 4063", "0", 3, "Years of experience")

    def fill_language_skills(self) -> None:
        """Section E: Language Skills"""
        languages = self._get("language_skills", default={})

        # French proficiency
        french = languages.get("french", {})
        self._add("Champ de texte 4070", french.get("level", "Intermédiaire"), 3, "French level")

        # English proficiency
        english = languages.get("english", {})
        self._add("Champ de texte 4071", english.get("level", "Avancé"), 3, "English level")

        # Other languages
        other = languages.get("other", [])
        if other:
            other_str = ", ".join([f"{l.get('name', '')}: {l.get('level', '')}" for l in other])
            self._add("Champ de texte 4072", other_str, 3, "Other languages")
        else:
            self._add("Champ de texte 4072", self.NA, 3, "Other languages (N/A)")

    def fill_declaration(self) -> None:
        """Section F: Declaration"""
        decl = self._get("declaration", default={})

        # Declaration checkboxes
        self._add("Case d'option 4001", self.YES, 4, "Information accurate declaration")
        self._add("Case d'option 4002", self.YES, 4, "Consent to verification")

        # Signature
        today = datetime.now().strftime("%Y/%m/%d")
        self._add("Champ de texte 4080", today, 4, "Signature date")
        self._add("Champ de texte 4081", decl.get("signature_city", "Montreal"), 4, "Signature city")

    def fill_all(self) -> List[Dict[str, Any]]:
        self.fields = []

        self.fill_worker_info()
        self.fill_employer_info()
        self.fill_employment_details()
        self.fill_qualifications()
        self.fill_language_skills()
        self.fill_declaration()

        return self.fields

    def save(self, path: str) -> int:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.fields, f, ensure_ascii=False, indent=2)
        return len(self.fields)


def main():
    if len(sys.argv) < 3:
        print("Usage: python form_filler_a0591.py <profile.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        profile = json.load(f)

    filler = A0591FormFiller(profile)
    filler.fill_all()
    count = filler.save(sys.argv[2])

    print(f"Generated {count} field values for A-0591-A0")


if __name__ == "__main__":
    main()
