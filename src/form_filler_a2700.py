#!/usr/bin/env python3
"""
A-2700-CF Form Filler
Generates field values for Quebec Employer Attestation form.

Form: A-2700-CF (Attestation de l'employeur)
Purpose: Employer certifies employment offer details

Author: CAQ Form Completion Skill
Version: BETA-2
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class A2700FormFiller:
    """
    Fills A-2700-CF (Employer Attestation) form fields from client profile.
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
        if isinstance(val, str):
            return self.YES if val.lower() in ('yes', 'oui', 'true', '1') else self.NO
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

    def fill_employer_section(self) -> None:
        """Section 1: Employer Information"""
        emp = self._get("employer", default={})
        emp_addr = emp.get("address", {})

        # Employer identification
        self._add("Champ de texte 2001", emp.get("company_name", ""), 1, "Employer name")
        self._add("Champ de texte 2002", emp.get("neq_number", ""), 1, "NEQ number")

        # Address
        if isinstance(emp_addr, dict):
            self._add("Champ de texte 2003", emp_addr.get("full_address", ""), 1, "Employer address")
            self._add("Champ de texte 2004", emp_addr.get("city", ""), 1, "Employer city")
            self._add("Champ de texte 2005", emp_addr.get("postal_code", ""), 1, "Employer postal code")
        else:
            self._add("Champ de texte 2003", str(emp_addr), 1, "Employer full address")

        # Contact
        self._add("Champ de texte 2006", emp.get("phone", ""), 1, "Employer phone")
        self._add("Champ de texte 2007", emp.get("email", ""), 1, "Employer email")

        # Employer representative
        emp_rep = emp.get("contact_person", {})
        self._add("Champ de texte 2008", emp_rep.get("name", ""), 1, "Contact person name")
        self._add("Champ de texte 2009", emp_rep.get("title", ""), 1, "Contact person title")

    def fill_worker_section(self) -> None:
        """Section 2: Worker Information"""
        pi = self._get("personal_information", default={})

        self._add("Champ de texte 2010", pi.get("surname", ""), 2, "Worker surname")
        self._add("Champ de texte 2011", pi.get("given_names", ""), 2, "Worker given names")
        self._add("Champ de texte 2012", self._fmt_date(pi.get("date_of_birth", "")), 2, "Worker DOB")
        self._add("Champ de texte 2013", pi.get("citizenship_country", ""), 2, "Worker nationality")

    def fill_employment_section(self) -> None:
        """Section 3: Employment Offer Details"""
        job = self._get("quebec_employment", default={})

        # Job details
        self._add("Champ de texte 2020", job.get("job_title", ""), 2, "Job title")
        self._add("Champ de texte 2021", job.get("noc_code", ""), 2, "NOC code")
        self._add("Champ de texte 2022", job.get("noc_profession_name", ""), 2, "NOC profession")
        self._add("Champ de texte 2023", job.get("work_location", ""), 2, "Work location")

        # Duties
        self._add("Champ de texte 2024", job.get("duties", ""), 3, "Job duties")

        # LMIA
        self._add("Champ de texte 2025", job.get("lmia_number", ""), 3, "LMIA number")
        self._add("Champ de texte 2026", self._fmt_date(job.get("lmia_date", "")), 3, "LMIA date")

        # Employment period
        self._add("Champ de texte 2030", self._fmt_date(job.get("start_date", "")), 3, "Start date")
        self._add("Champ de texte 2031", self._fmt_date(job.get("end_date", "")), 3, "End date")

        # Compensation
        self._add("Champ de texte 2040", job.get("hourly_wage", ""), 3, "Hourly wage")
        self._add("Champ de texte 2041", job.get("weekly_hours", ""), 3, "Weekly hours")

        # Benefits
        has_benefits = job.get("has_benefits", False)
        self._add("Case d'option 2001", self._yn(has_benefits), 3, "Benefits provided")

    def fill_declaration_section(self) -> None:
        """Section 4: Employer Declaration"""
        emp = self._get("employer", default={})

        # Certification
        self._add("Case d'option 2010", self.YES, 4, "Employer certification")

        # Signature info
        today = datetime.now().strftime("%Y/%m/%d")
        self._add("Champ de texte 2050", today, 4, "Signature date")
        self._add("Champ de texte 2051", emp.get("signature_city", "Montreal"), 4, "Signature city")

    def fill_all(self) -> List[Dict[str, Any]]:
        self.fields = []

        self.fill_employer_section()
        self.fill_worker_section()
        self.fill_employment_section()
        self.fill_declaration_section()

        return self.fields

    def save(self, path: str) -> int:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.fields, f, ensure_ascii=False, indent=2)
        return len(self.fields)


def main():
    if len(sys.argv) < 3:
        print("Usage: python form_filler_a2700.py <profile.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        profile = json.load(f)

    filler = A2700FormFiller(profile)
    filler.fill_all()
    count = filler.save(sys.argv[2])

    print(f"Generated {count} field values for A-2700-CF")


if __name__ == "__main__":
    main()
