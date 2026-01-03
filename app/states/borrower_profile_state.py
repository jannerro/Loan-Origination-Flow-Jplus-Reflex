import reflex as rx
from typing import TypedDict
import random
from faker import Faker
import datetime

fake = Faker()


class LoanHistoryItem(TypedDict):
    id: str
    amount: int
    date: str
    status: str
    type: str


class DocumentItem(TypedDict):
    name: str
    type: str
    status: str
    date: str
    expiry: str
    icon: str


class MessageItem(TypedDict):
    id: int
    sender: str
    content: str
    timestamp: str
    is_staff: bool
    avatar: str


class AmortizationItem(TypedDict):
    month: str
    principal: float
    interest: float
    balance: float


class BorrowerProfile(TypedDict):
    id: str
    name: str
    email: str
    phone: str
    address: str
    employer: str
    job_title: str
    annual_income: int
    credit_score: int
    total_loans: int
    total_borrowed: int
    avatar: str
    relationship_score: int
    engagement_level: str


class BorrowerProfileState(rx.State):
    active_tab: str = "overview"
    profile: BorrowerProfile = {
        "id": "",
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "employer": "",
        "job_title": "",
        "annual_income": 0,
        "credit_score": 0,
        "total_loans": 0,
        "total_borrowed": 0,
        "avatar": "",
        "relationship_score": 0,
        "engagement_level": "",
    }
    history: list[LoanHistoryItem] = []
    documents: list[DocumentItem] = []
    messages: list[MessageItem] = []
    amortization_schedule: list[AmortizationItem] = []
    new_message: str = ""
    is_doc_request_open: bool = False
    doc_request_type: str = "Bank Statement"
    doc_request_note: str = ""
    doc_request_urgency: str = "Normal"
    doc_types: list[str] = [
        "Driver's License",
        "Pay Stub",
        "Bank Statement",
        "Tax Return",
        "W-2 Form",
        "Employment Letter",
        "Utility Bill",
        "Other",
    ]

    @rx.event
    def open_doc_request_modal(self):
        self.is_doc_request_open = True
        self.doc_request_type = "Bank Statement"
        self.doc_request_note = ""
        self.doc_request_urgency = "Normal"

    @rx.event
    def close_doc_request_modal(self):
        self.is_doc_request_open = False

    @rx.event
    def set_doc_request_type(self, value: str):
        self.doc_request_type = value

    @rx.event
    def set_doc_request_note(self, value: str):
        self.doc_request_note = value

    @rx.event
    def set_doc_request_urgency(self, value: str):
        self.doc_request_urgency = value

    @rx.event
    def send_doc_request(self):
        new_doc = {
            "name": self.doc_request_type,
            "type": "Requested",
            "status": "Pending",
            "date": datetime.datetime.now().strftime("%b %d, %Y"),
            "expiry": "None",
            "icon": "file-text",
        }
        self.documents.insert(0, new_doc)
        self.is_doc_request_open = False
        return rx.toast(f"Document request sent: {self.doc_request_type}")

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def set_new_message(self, val: str):
        self.new_message = val

    @rx.event
    def send_message(self):
        if not self.new_message:
            return
        self.messages.append(
            {
                "id": len(self.messages) + 1,
                "sender": "You",
                "content": self.new_message,
                "timestamp": "Just now",
                "is_staff": True,
                "avatar": "https://api.dicebear.com/9.x/avataaars/svg?seed=Felix",
            }
        )
        self.new_message = ""
        return rx.toast("Message sent")

    @rx.event
    def load_profile(self):
        from app.states.data_store import borrowers, apps

        b_id = self.router.page.params.get("id")
        found_borrower = None
        for b in borrowers:
            if b["id"] == b_id:
                found_borrower = b
                break
        if not found_borrower and borrowers:
            found_borrower = borrowers[0]
        if found_borrower:
            borrower_apps = [
                app for app in apps if app["applicant_id"] == found_borrower["id"]
            ]
            total_borrowed = sum([app["amount"] for app in borrower_apps])
            self.profile = {
                "id": found_borrower["id"],
                "name": found_borrower["name"],
                "email": found_borrower["email"],
                "phone": found_borrower["phone"],
                "address": found_borrower["address"],
                "employer": found_borrower["employer"],
                "job_title": found_borrower["job_title"],
                "annual_income": found_borrower["annual_income"],
                "credit_score": found_borrower["credit_score"],
                "total_loans": len(borrower_apps),
                "total_borrowed": total_borrowed,
                "avatar": found_borrower["avatar"],
                "relationship_score": found_borrower["relationship_score"],
                "engagement_level": found_borrower["engagement_level"],
            }
            self.history = []
            for app in borrower_apps:
                self.history.append(
                    {
                        "id": app["id"],
                        "amount": app["amount"],
                        "date": app["created_at"],
                        "status": app["status"],
                        "type": app["type"],
                    }
                )
            today = datetime.datetime.now()
            self.documents = [
                {
                    "name": "Driver's License",
                    "type": "Identification",
                    "status": "Verified",
                    "date": (today - datetime.timedelta(days=15)).strftime("%b %d, %Y"),
                    "expiry": (today + datetime.timedelta(days=700)).strftime(
                        "%b %d, %Y"
                    ),
                    "icon": "id-card",
                },
                {
                    "name": "Pay Stub (Recent)",
                    "type": "Income Proof",
                    "status": "Verified",
                    "date": (today - datetime.timedelta(days=5)).strftime("%b %d, %Y"),
                    "expiry": "None",
                    "icon": "file-text",
                },
                {
                    "name": "Bank Statement",
                    "type": "Financial",
                    "status": "Pending",
                    "date": (today - datetime.timedelta(days=2)).strftime("%b %d, %Y"),
                    "expiry": "None",
                    "icon": "landmark",
                },
            ]
            self.messages = [
                {
                    "id": 1,
                    "sender": found_borrower["name"],
                    "content": "Hi, I just uploaded the requested documents.",
                    "timestamp": "2 hours ago",
                    "is_staff": False,
                    "avatar": found_borrower["avatar"],
                },
                {
                    "id": 2,
                    "sender": "Alex Morgan",
                    "content": f"Thanks {found_borrower['name'].split()[0]}! I will review them shortly.",
                    "timestamp": "1 hour ago",
                    "is_staff": True,
                    "avatar": "https://api.dicebear.com/9.x/avataaars/svg?seed=Felix",
                },
            ]
            loan_amount = borrower_apps[0]["amount"] if borrower_apps else 25000
            rate = 0.075 / 12
            term = borrower_apps[0]["term"] if borrower_apps else 48
            payment = loan_amount * rate / (1 - (1 + rate) ** (-term))
            balance = loan_amount
            schedule = []
            for i in range(1, 13):
                interest = balance * rate
                principal = payment - interest
                balance -= principal
                schedule.append(
                    {
                        "month": f"M{i}",
                        "principal": round(principal, 2),
                        "interest": round(interest, 2),
                        "balance": round(balance, 2),
                    }
                )
            self.amortization_schedule = schedule