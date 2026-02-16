#!/usr/bin/env python3
"""
CAQ Form Filler v6.0
Generates field values for Quebec CAQ application forms from structured JSON profiles.

Primary Form: A-0506-CF (Demande de sélection temporaire - PTET)
Version: December 2025 form layout

Author: Immigration Automation Project
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional


class CAQFormFillerV6:
    """
    Fills A-0506-CF form fields from a structured client profile.
    Outputs a list of field value dictionaries for PDF population.
    """

    # Constants for radio button values
    YES = "/1"           # Radio button yes (second option)
    NO = "/0"            # Radio button no (first option)
    NA = "s.o."          # "sans objet" for non-applicable fields

    # PTET stream radio button values
    PTET_STREAMS = {
        "global_talents": "/0",
        "home_care": "/1",
        "agricultural_low_wage": "/2",
        "high_wage": "/3",
        "low_wage": "/4",
        "other": "/5"
    }

    # Gender dropdown values (French)
    GENDER_VALUES = {
        "M": "Masculin",
        "F": "Féminin",
        "X": "Autre identité de genre"
    }

    # Representative type radio button values
    REP_TYPES = {
        "barreau": "/0",      # Lawyer
        "notaire": "/1",       # Notary
        "consultant": "/2",    # Immigration consultant
        "other": "/3"
    }

    # Relationship translations
    RELATIONSHIPS = {
        "spouse": "Époux/Épouse",
        "common_law": "Conjoint de fait",
        "child": "Enfant",
        "parent": "Père/Mère",
        "sibling": "Frère/Sœur"
    }

    def __init__(self, profile: Dict[str, Any]):
        """
        Initialize filler with client profile.

        Args:
            profile: Dictionary containing client data
        """
        self.profile = profile
        self.fields: List[Dict[str, Any]] = []

    def _add(self, fid: str, val: Any, pg: int, desc: str) -> None:
        """
        Add a field value to the output list.

        Args:
            fid: PDF field ID
            val: Value to populate
            pg: Page number
            desc: Human-readable description
        """
        if val is not None:
            self.fields.append({
                "field_id": fid,
                "value": str(val),
                "page": pg,
                "description": desc
            })

    def _get(self, *keys, default: Any = "") -> Any:
        """
        Safely retrieve nested value from profile.

        Args:
            *keys: Path of keys to traverse
            default: Default value if path not found

        Returns:
            Value at path or default
        """
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
        """
        Convert value to Yes/No radio button value.

        Args:
            val: Boolean or truthy value

        Returns:
            YES or NO constant
        """
        if isinstance(val, bool):
            return self.YES if val else self.NO
        if isinstance(val, str):
            return self.YES if val.lower() in ('yes', 'oui', 'true', '1') else self.NO
        return self.YES if val else self.NO

    def _fmt_date(self, ds: str, fmt: str = "full") -> str:
        """
        Format date string.

        Args:
            ds: Date string (YYYY-MM-DD or YYYY-MM)
            fmt: "full" for YYYY/MM/DD, "ym" for YYYY/MM

        Returns:
            Formatted date string or empty string if invalid
        """
        if not ds:
            return ""

        try:
            # Handle full date
            if len(ds) >= 10:
                dt = datetime.strptime(ds[:10], "%Y-%m-%d")
                if fmt == "full":
                    return dt.strftime("%Y/%m/%d")
                elif fmt == "ym":
                    return dt.strftime("%Y/%m")
            # Handle year-month only
            elif len(ds) >= 7:
                dt = datetime.strptime(ds[:7], "%Y-%m")
                return dt.strftime("%Y/%m")
        except ValueError:
            pass

        return ds  # Return original if parsing fails

    def fill_section_1(self) -> None:
        """
        Section 1: Previous DST Application (Page 4)
        Radio button asking if applicant has previously applied for DST.
        """
        prev_app = self._get("caq_application", "previous_dst_application", default=False)
        self._add("Case d'option 01", self._yn(prev_app), 4, "Previous DST application")

        # If yes, provide file number
        if prev_app:
            file_num = self._get("caq_application", "previous_file_number", default="")
            self._add("Champ de texte 1001", file_num, 4, "Previous file number")

    def fill_section_2(self) -> None:
        """
        Section 2: PTET Stream Selection (Page 4)
        Radio button group for selecting program stream.
        """
        stream = self._get("caq_application", "ptet_stream", default="high_wage")
        stream_val = self.PTET_STREAMS.get(stream, self.PTET_STREAMS["high_wage"])
        self._add("Case d'option 02", stream_val, 4, "PTET stream selection")

        # Simplified processing eligibility
        simplified = self._get("caq_application", "simplified_processing_eligible", default=False)
        self._add("Case d'option 03", self._yn(simplified), 4, "Simplified processing eligible")

    def fill_section_3(self) -> None:
        """
        Section 3: Identity Information (Pages 4-5)
        Personal information including name, DOB, citizenship, passport.
        """
        pi = self._get("personal_information", default={})
        passport = self._get("passport", default={})

        # Surname and given names
        self._add("Champ de texte 11046", pi.get("surname", ""), 4, "Surname")
        self._add("Champ de texte 11019", pi.get("given_names", ""), 4, "Given names")

        # Gender (dropdown)
        gender = pi.get("gender", "")
        gender_val = self.GENDER_VALUES.get(gender, "")
        self._add("Liste déroulante 7", gender_val, 4, "Gender")

        # Date of birth
        dob = self._fmt_date(pi.get("date_of_birth", ""))
        self._add("Champ de texte 1050", dob, 4, "Date of birth")

        # Citizenship status and country
        self._add("Champ de texte 1051", pi.get("citizenship", ""), 4, "Citizenship status")
        self._add("Champ de texte 1052", pi.get("citizenship_country", ""), 4, "Country of citizenship")

        # Birth location
        self._add("Champ de texte 1053", pi.get("birth_city", ""), 5, "City of birth")
        self._add("Champ de texte 1054", pi.get("birth_province", ""), 5, "Province/State of birth")
        self._add("Champ de texte 1055", pi.get("birth_country", ""), 5, "Country of birth")

        # Passport information
        self._add("Champ de texte 1056", passport.get("passport_number", ""), 5, "Passport number")
        self._add("Champ de texte 1057", self._fmt_date(passport.get("issue_date", "")), 5, "Passport issue date")
        self._add("Champ de texte 1058", self._fmt_date(passport.get("expiry_date", "")), 5, "Passport expiry date")

        # Current address
        addr = self._get("current_address", default={})
        self._add("Champ de texte 1059", addr.get("street_number", ""), 5, "Street number")
        self._add("Champ de texte 1060", addr.get("street_name", ""), 5, "Street name")
        self._add("Champ de texte 1061", addr.get("apartment", ""), 5, "Apartment/Unit")
        self._add("Champ de texte 1062", addr.get("city", ""), 5, "City")
        self._add("Champ de texte 1063", addr.get("province", ""), 5, "Province/State")
        self._add("Champ de texte 1064", addr.get("country", ""), 5, "Country")
        self._add("Champ de texte 1065", addr.get("postal_code", ""), 5, "Postal code")
        self._add("Champ de texte 1066", addr.get("phone", ""), 5, "Phone number")
        self._add("Champ de texte 1067", addr.get("email", ""), 5, "Email address")

        # Currently in Quebec
        in_qc = addr.get("in_quebec", False)
        self._add("Case d'option 04", self._yn(in_qc), 5, "Currently in Quebec")

    def fill_section_4(self) -> None:
        """
        Section 4: Correspondence Address (Page 5)
        Different address for receiving correspondence.
        """
        corr = self._get("correspondence_address", default={})
        different = corr.get("different_from_current", False)

        self._add("Case d'option 05", self._yn(different), 5, "Different correspondence address")

        if different:
            self._add("Champ de texte 1070", corr.get("street_number", ""), 5, "Corr. street number")
            self._add("Champ de texte 1071", corr.get("street_name", ""), 5, "Corr. street name")
            self._add("Champ de texte 1072", corr.get("apartment", ""), 5, "Corr. apartment")
            self._add("Champ de texte 1073", corr.get("city", ""), 5, "Corr. city")
            self._add("Champ de texte 1074", corr.get("province", ""), 5, "Corr. province")
            self._add("Champ de texte 1075", corr.get("country", ""), 5, "Corr. country")
            self._add("Champ de texte 1076", corr.get("postal_code", ""), 5, "Corr. postal code")
        else:
            # Fill with N/A if not different
            for fid in ["Champ de texte 1070", "Champ de texte 1071", "Champ de texte 1072",
                        "Champ de texte 1073", "Champ de texte 1074", "Champ de texte 1075",
                        "Champ de texte 1076"]:
                self._add(fid, self.NA, 5, "Corr. address (N/A)")

    def fill_section_5(self) -> None:
        """
        Section 5: Family Members (Page 5)
        Table with 6 rows for family members accompanying.
        Empty rows must be filled with s.o.
        """
        members = self._get("family_members", default=[])

        # Family member field patterns (6 rows)
        for i in range(6):
            row_base = 1080 + (i * 5)  # Fields increment by 5 per row

            if i < len(members):
                member = members[i]
                self._add(f"Champ de texte {row_base}", member.get("surname", ""), 5, f"Family member {i+1} surname")
                self._add(f"Champ de texte {row_base + 1}", member.get("given_names", ""), 5, f"Family member {i+1} given names")
                self._add(f"Champ de texte {row_base + 2}", self._fmt_date(member.get("date_of_birth", "")), 5, f"Family member {i+1} DOB")
                self._add(f"Champ de texte {row_base + 3}", member.get("relationship", ""), 5, f"Family member {i+1} relationship")
                accompanying = member.get("accompanying", False)
                self._add(f"Case d'option {10 + i}", self._yn(accompanying), 5, f"Family member {i+1} accompanying")
            else:
                # Fill empty row with N/A
                self._add(f"Champ de texte {row_base}", self.NA, 5, f"Family member {i+1} surname (N/A)")
                self._add(f"Champ de texte {row_base + 1}", self.NA, 5, f"Family member {i+1} given names (N/A)")
                self._add(f"Champ de texte {row_base + 2}", self.NA, 5, f"Family member {i+1} DOB (N/A)")
                self._add(f"Champ de texte {row_base + 3}", self.NA, 5, f"Family member {i+1} relationship (N/A)")
                self._add(f"Case d'option {10 + i}", self.NO, 5, f"Family member {i+1} accompanying (N/A)")

    def fill_section_6(self) -> None:
        """
        Section 6: Employer Information (Pages 5-6)
        Quebec employer details.
        """
        emp = self._get("employer", default={})
        emp_addr = emp.get("address", {})

        self._add("Champ de texte 101093", emp.get("company_name", ""), 5, "Employer name")
        self._add("Champ de texte 101094", emp.get("neq_number", ""), 5, "NEQ number")

        # Employer address
        if isinstance(emp_addr, dict):
            self._add("Champ de texte 101095", emp_addr.get("full_address", ""), 6, "Employer full address")
        else:
            self._add("Champ de texte 101095", str(emp_addr), 6, "Employer full address")

        # Applicant has control/ownership
        has_control = emp.get("applicant_has_control", False)
        self._add("Case d'option 20", self._yn(has_control), 6, "Applicant has control of employer")

    def fill_section_7(self) -> None:
        """
        Section 7: Job Details (Pages 6-7)
        Employment offer information including NOC, wages, dates.
        """
        job = self._get("quebec_employment", default={})

        self._add("Champ de texte 101048", job.get("job_title", ""), 6, "Job title")
        self._add("Champ de texte 101049", job.get("noc_profession_name", ""), 6, "NOC profession name")
        self._add("Champ de texte 10113", job.get("noc_code", ""), 6, "NOC code")
        self._add("Champ de texte 101050", job.get("work_location", ""), 6, "Work location")

        # Job duties (may be multi-line)
        duties = job.get("duties", "")
        self._add("Champ de texte 101051", duties, 7, "Job duties")

        # LMIA information
        self._add("Champ de texte 10111", job.get("lmia_number", ""), 7, "LMIA number")

        # Employment dates
        self._add("Champ de texte 1045", self._fmt_date(job.get("start_date", "")), 7, "Employment start date")
        self._add("Champ de texte 1046", self._fmt_date(job.get("end_date", "")), 7, "Employment end date")

        # Wage information
        self._add("Champ de texte 101052", job.get("hourly_wage", ""), 7, "Hourly wage")
        self._add("Champ de texte 101053", job.get("weekly_hours", ""), 7, "Weekly hours")

        # Commitment to reside in Quebec
        commit = job.get("commitment_to_reside", True)
        self._add("Case d'option 21", self._yn(commit), 7, "Commitment to reside in Quebec")

    def fill_section_8(self) -> None:
        """
        Section 8: Education History (Pages 7-8)
        Table with 5 entries for educational background.
        Empty rows must be filled with s.o.
        """
        education = self._get("education", default=[])

        for i in range(5):
            row_base = 1100 + (i * 5)

            if i < len(education):
                edu = education[i]
                self._add(f"Champ de texte {row_base}", edu.get("institution", ""), 8, f"Education {i+1} institution")
                self._add(f"Champ de texte {row_base + 1}", edu.get("diploma_type", ""), 8, f"Education {i+1} diploma")
                self._add(f"Champ de texte {row_base + 2}", edu.get("field_of_study", ""), 8, f"Education {i+1} field")
                self._add(f"Champ de texte {row_base + 3}", self._fmt_date(edu.get("start_date", ""), "ym"), 8, f"Education {i+1} start")
                self._add(f"Champ de texte {row_base + 4}", self._fmt_date(edu.get("end_date", ""), "ym"), 8, f"Education {i+1} end")
            else:
                # Fill empty row with N/A
                for j in range(5):
                    self._add(f"Champ de texte {row_base + j}", self.NA, 8, f"Education {i+1} field {j+1} (N/A)")

    def fill_section_9(self) -> None:
        """
        Section 9: Work Experience (Pages 9-10)
        Table with 4 entries for professional experience.
        Empty rows must be filled with s.o.
        """
        experience = self._get("work_experience", default=[])

        for i in range(4):
            row_base = 1130 + (i * 7)

            if i < len(experience):
                exp = experience[i]
                self._add(f"Champ de texte {row_base}", exp.get("employer_name", ""), 9, f"Work exp {i+1} employer")
                self._add(f"Champ de texte {row_base + 1}", exp.get("job_title", ""), 9, f"Work exp {i+1} title")
                self._add(f"Champ de texte {row_base + 2}", exp.get("country", ""), 9, f"Work exp {i+1} country")
                self._add(f"Champ de texte {row_base + 3}", exp.get("duties", ""), 9, f"Work exp {i+1} duties")
                self._add(f"Champ de texte {row_base + 4}", self._fmt_date(exp.get("start_date", "")), 10, f"Work exp {i+1} start")
                self._add(f"Champ de texte {row_base + 5}", self._fmt_date(exp.get("end_date", "")), 10, f"Work exp {i+1} end")
                self._add(f"Champ de texte {row_base + 6}", exp.get("description", ""), 10, f"Work exp {i+1} description")
            else:
                # Fill empty row with N/A
                for j in range(7):
                    self._add(f"Champ de texte {row_base + j}", self.NA, 9 if j < 4 else 10, f"Work exp {i+1} field {j+1} (N/A)")

    def fill_section_10(self) -> None:
        """
        Section 10: Previous Quebec Stays (Page 10)
        Table with 6 rows for previous stays in Quebec.
        Empty rows must be filled with s.o.
        """
        stays = self._get("quebec_stays", default=[])

        for i in range(6):
            row_base = 1160 + (i * 4)

            if i < len(stays):
                stay = stays[i]
                self._add(f"Champ de texte {row_base}", self._fmt_date(stay.get("start_date", "")), 10, f"Stay {i+1} start")
                self._add(f"Champ de texte {row_base + 1}", self._fmt_date(stay.get("end_date", "")), 10, f"Stay {i+1} end")
                self._add(f"Champ de texte {row_base + 2}", stay.get("purpose", ""), 10, f"Stay {i+1} purpose")
                self._add(f"Champ de texte {row_base + 3}", stay.get("reason", ""), 10, f"Stay {i+1} reason")
            else:
                # Fill empty row with N/A
                for j in range(4):
                    self._add(f"Champ de texte {row_base + j}", self.NA, 10, f"Stay {i+1} field {j+1} (N/A)")

    def fill_section_11(self) -> None:
        """
        Section 11: Paid Representative (Page 11)
        Information about immigration representative.
        """
        rep = self._get("paid_representative", default={})
        has_rep = rep.get("has_representative", False)

        self._add("Case d'option 30", self._yn(has_rep), 11, "Has paid representative")

        if has_rep:
            # Representative type
            rep_type = rep.get("representative_type", "barreau")
            rep_type_val = self.REP_TYPES.get(rep_type, self.REP_TYPES["barreau"])
            self._add("Case d'option 31", rep_type_val, 11, "Representative type")

            # Representative details
            self._add("Champ de texte 1200", rep.get("surname", ""), 11, "Rep surname")
            self._add("Champ de texte 1201", rep.get("given_names", ""), 11, "Rep given names")
            self._add("Champ de texte 1202", rep.get("license_number", ""), 11, "Rep license number")
            self._add("Champ de texte 1203", rep.get("organization", ""), 11, "Rep organization")
            self._add("Champ de texte 1204", rep.get("phone", ""), 11, "Rep phone")
            self._add("Champ de texte 1205", rep.get("email", ""), 11, "Rep email")
            self._add("Champ de texte 1206", rep.get("address", ""), 11, "Rep address")
            self._add("Champ de texte 1207", rep.get("postal_code", ""), 11, "Rep postal code")
        else:
            # Fill with N/A
            self._add("Case d'option 31", self.NO, 11, "Representative type (N/A)")
            for fid in range(1200, 1208):
                self._add(f"Champ de texte {fid}", self.NA, 11, f"Rep field (N/A)")

    def fill_section_14(self) -> None:
        """
        Section 14: Declaration and Signature (Pages 14-15)
        Applicant declaration and signature location.
        """
        decl = self._get("declaration", default={})
        pi = self._get("personal_information", default={})

        # Signature location
        self._add("Champ de texte 1300", decl.get("signature_city", ""), 14, "Signature city")
        self._add("Champ de texte 1301", decl.get("signature_country", ""), 14, "Signature country")

        # Signature date (today's date)
        today = datetime.now().strftime("%Y/%m/%d")
        self._add("Champ de texte 1302", today, 14, "Signature date")

        # Applicant name for signature
        full_name = f"{pi.get('surname', '')} {pi.get('given_names', '')}".strip()
        self._add("Champ de texte 1303", full_name, 15, "Applicant printed name")

    def fill_all(self) -> List[Dict[str, Any]]:
        """
        Execute all section fillers.

        Returns:
            List of field value dictionaries
        """
        self.fields = []  # Reset

        self.fill_section_1()
        self.fill_section_2()
        self.fill_section_3()
        self.fill_section_4()
        self.fill_section_5()
        self.fill_section_6()
        self.fill_section_7()
        self.fill_section_8()
        self.fill_section_9()
        self.fill_section_10()
        self.fill_section_11()
        self.fill_section_14()

        return self.fields

    def save(self, path: str) -> int:
        """
        Save field values to JSON file.

        Args:
            path: Output file path

        Returns:
            Number of fields written
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.fields, f, ensure_ascii=False, indent=2)
        return len(self.fields)


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python caq_form_filler_v6.py <profile.json> <output.json>")
        sys.exit(1)

    profile_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(profile_path, 'r', encoding='utf-8') as f:
        profile = json.load(f)

    filler = CAQFormFillerV6(profile)
    filler.fill_all()
    count = filler.save(output_path)

    print(f"Generated {count} field values")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
