#!/usr/bin/env python3
"""
ME-0031 Form Filler
Generates field values for Quebec Commitment form.

Form: ME-0031 (Engagement)
Purpose: Worker's commitment to reside and work in Quebec

Author: CAQ Form Completion Skill
Version: BETA-2
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class ME0031FormFiller:
    """
    Fills ME-0031 (Engagement/Commitment) form fields from client profile.
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

    def fill_worker_identity(self) -> None:
        """Section 1: Worker Identification"""
        pi = self._get("personal_information", default={})

        self._add("Champ de texte 3001", pi.get("surname", ""), 1, "Worker surname")
        self._add("Champ de texte 3002", pi.get("given_names", ""), 1, "Worker given names")
        self._add("Champ de texte 3003", self._fmt_date(pi.get("date_of_birth", "")), 1, "Worker DOB")

        # Passport
        passport = self._get("passport", default={})
        self._add("Champ de texte 3004", passport.get("passport_number", ""), 1, "Passport number")
        self._add("Champ de texte 3005", pi.get("citizenship_country", ""), 1, "Country of citizenship")

    def fill_employer_info(self) -> None:
        """Section 2: Employer Information"""
        emp = self._get("employer", default={})

        self._add("Champ de texte 3010", emp.get("company_name", ""), 1, "Employer name")

        emp_addr = emp.get("address", {})
        if isinstance(emp_addr, dict):
            self._add("Champ de texte 3011", emp_addr.get("full_address", ""), 1, "Employer address")
        else:
            self._add("Champ de texte 3011", str(emp_addr), 1, "Employer address")

    def fill_employment_details(self) -> None:
        """Section 3: Employment Details"""
        job = self._get("quebec_employment", default={})

        self._add("Champ de texte 3020", job.get("job_title", ""), 1, "Job title")
        self._add("Champ de texte 3021", job.get("work_location", ""), 1, "Work location")

        # Employment period
        self._add("Champ de texte 3030", self._fmt_date(job.get("start_date", "")), 1, "Start date")
        self._add("Champ de texte 3031", self._fmt_date(job.get("end_date", "")), 1, "End date")

    def fill_commitments(self) -> None:
        """Section 4: Worker Commitments"""
        job = self._get("quebec_employment", default={})

        # Commitment to reside in Quebec
        commit_reside = job.get("commitment_to_reside", True)
        self._add("Case d'option 3001", self._yn(commit_reside), 2, "Commit to reside in Quebec")

        # Commitment to work for specified employer
        self._add("Case d'option 3002", self.YES, 2, "Commit to work for employer")

        # Commitment to notify of changes
        self._add("Case d'option 3003", self.YES, 2, "Commit to notify changes")

    def fill_declaration(self) -> None:
        """Section 5: Declaration and Signature"""
        decl = self._get("declaration", default={})
        pi = self._get("personal_information", default={})

        # Declaration checkbox
        self._add("Case d'option 3010", self.YES, 2, "Declaration acknowledgment")

        # Signature location
        self._add("Champ de texte 3040", decl.get("signature_city", ""), 2, "Signature city")
        self._add("Champ de texte 3041", decl.get("signature_country", "Canada"), 2, "Signature country")

        # Signature date
        today = datetime.now().strftime("%Y/%m/%d")
        self._add("Champ de texte 3042", today, 2, "Signature date")

        # Printed name
        full_name = f"{pi.get('surname', '')} {pi.get('given_names', '')}".strip()
        self._add("Champ de texte 3043", full_name, 2, "Printed name")

    def fill_all(self) -> List[Dict[str, Any]]:
        self.fields = []

        self.fill_worker_identity()
        self.fill_employer_info()
        self.fill_employment_details()
        self.fill_commitments()
        self.fill_declaration()

        return self.fields

    def save(self, path: str) -> int:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.fields, f, ensure_ascii=False, indent=2)
        return len(self.fields)


def main():
    if len(sys.argv) < 3:
        print("Usage: python form_filler_me0031.py <profile.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        profile = json.load(f)

    filler = ME0031FormFiller(profile)
    filler.fill_all()
    count = filler.save(sys.argv[2])

    print(f"Generated {count} field values for ME-0031")


if __name__ == "__main__":
    main()
