import reflex as rx
from typing import Any
import datetime
import random


class ApplicationState(rx.State):
    current_step: int = 0
    steps: list[str] = [
        "Personal Info",
        "Employment",
        "Loan Details",
        "Documents",
        "Review",
    ]
    completed_steps: list[int] = []
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    dob: str = ""
    ssn: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    employer: str = ""
    job_title: str = ""
    annual_income: float = 0.0
    employment_length: str = ""
    employment_status: str = "Full-time"
    loan_amount: int = 25000
    loan_term: int = 36
    loan_purpose: str = "Home Improvement"
    loan_type: str = "Personal Loan"
    uploaded_files: list[str] = []
    errors: dict[str, str] = {}
    terms_accepted: bool = False

    @rx.var
    def progress(self) -> int:
        return int(self.current_step / (len(self.steps) - 1) * 100)

    @rx.event
    def validate_step(self) -> bool:
        self.errors = {}
        is_valid = True
        if self.current_step == 0:
            if not self.first_name:
                self.errors["first_name"] = "First name is required"
                is_valid = False
            if not self.last_name:
                self.errors["last_name"] = "Last name is required"
                is_valid = False
            if not self.email:
                self.errors["email"] = "Email is required"
                is_valid = False
            if "@" not in self.email:
                self.errors["email"] = "Invalid email format"
                is_valid = False
            if not self.phone:
                self.errors["phone"] = "Phone is required"
                is_valid = False
            if not self.ssn:
                self.errors["ssn"] = "SSN is required"
                is_valid = False
        elif self.current_step == 1:
            if not self.employer:
                self.errors["employer"] = "Employer is required"
                is_valid = False
            if not self.job_title:
                self.errors["job_title"] = "Job title is required"
                is_valid = False
            if self.annual_income <= 0:
                self.errors["annual_income"] = "Valid income is required"
                is_valid = False
        elif self.current_step == 2:
            if self.loan_amount < 1000:
                self.errors["loan_amount"] = "Minimum loan amount is $1,000"
                is_valid = False
            if self.loan_amount > 100000:
                self.errors["loan_amount"] = "Maximum loan amount is $100,000"
                is_valid = False
        return is_valid

    @rx.event
    def next_step(self):
        if self.validate_step():
            if self.current_step < len(self.steps) - 1:
                if self.current_step not in self.completed_steps:
                    self.completed_steps.append(self.current_step)
                self.current_step += 1

    @rx.event
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1

    @rx.event
    def set_field(self, field: str, value: Any):
        setattr(self, field, value)
        if field in self.errors:
            del self.errors[field]

    @rx.event
    def set_amount(self, value: str):
        self.loan_amount = int(value)

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as f:
                f.write(upload_data)
            self.uploaded_files.append(file.filename)

    @rx.event
    def set_terms_accepted(self, value: bool):
        self.terms_accepted = value

    @rx.event
    def reset_form(self):
        self.current_step = 0
        self.completed_steps = []
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.dob = ""
        self.ssn = ""
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""
        self.employer = ""
        self.job_title = ""
        self.annual_income = 0.0
        self.employment_length = ""
        self.employment_status = "Full-time"
        self.loan_amount = 25000
        self.loan_term = 36
        self.loan_purpose = "Home Improvement"
        self.loan_type = "Personal Loan"
        self.uploaded_files = []
        self.errors = {}
        self.terms_accepted = False

    @rx.event
    async def submit_application(self):
        if not self.terms_accepted:
            return rx.toast(
                "Please accept the terms and conditions to proceed.", duration=3000
            )
        from app.states.data_store import apps, borrowers

        borrower_id = ""
        existing_borrower = next(
            (b for b in borrowers if b["email"] == self.email), None
        )
        if existing_borrower:
            borrower_id = existing_borrower["id"]
        else:
            borrower_id = f"BOR-{random.randint(2000, 9999)}"
            new_borrower = {
                "id": borrower_id,
                "name": f"{self.first_name} {self.last_name}",
                "email": self.email,
                "phone": self.phone,
                "address": f"{self.address}, {self.city}, {self.state} {self.zip_code}",
                "employer": self.employer,
                "job_title": self.job_title,
                "annual_income": int(self.annual_income),
                "credit_score": random.randint(600, 750),
                "avatar": f"https://api.dicebear.com/9.x/initials/svg?seed={self.first_name}",
                "relationship_score": 0,
                "engagement_level": "New",
            }
            borrowers.append(new_borrower)
        app_id = f"APP-{random.randint(6000, 9999)}"
        new_app = {
            "id": app_id,
            "applicant_id": borrower_id,
            "applicant_name": f"{self.first_name} {self.last_name}",
            "applicant_email": self.email,
            "applicant_avatar": f"https://api.dicebear.com/9.x/initials/svg?seed={self.first_name}",
            "amount": self.loan_amount,
            "term": self.loan_term,
            "purpose": self.loan_purpose,
            "type": self.loan_type,
            "status": "Pending",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
            "risk_score": random.randint(600, 800),
            "debt_to_income": round(random.uniform(10.0, 45.0), 1),
            "notes": "Application submitted via online portal.",
        }
        apps.insert(0, new_app)
        self.reset_form()
        return [
            rx.toast(f"Application {app_id} submitted successfully!", duration=3000),
            rx.redirect("/applications"),
        ]

    @rx.event
    def remove_file(self, filename: str):
        self.uploaded_files = [f for f in self.uploaded_files if f != filename]