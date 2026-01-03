from typing import TypedDict
import random
from faker import Faker
import datetime

fake = Faker()


class Borrower(TypedDict):
    id: str
    name: str
    email: str
    phone: str
    address: str
    employer: str
    job_title: str
    annual_income: int
    credit_score: int
    avatar: str
    relationship_score: int
    engagement_level: str


class Application(TypedDict):
    id: str
    applicant_id: str
    applicant_name: str
    applicant_email: str
    applicant_avatar: str
    amount: int
    term: int
    purpose: str
    type: str
    status: str
    created_at: str
    risk_score: int
    debt_to_income: float
    notes: str


borrowers: list[Borrower] = []
apps: list[Application] = []


def _initialize_data():
    """Initialize mock data at module level"""
    global borrowers, apps
    for i in range(25):
        b_id = f"BOR-{1000 + i}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"
        borrowers.append(
            {
                "id": b_id,
                "name": name,
                "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
                "phone": fake.phone_number(),
                "address": fake.address(),
                "employer": fake.company(),
                "job_title": fake.job(),
                "annual_income": random.randint(40000, 180000),
                "credit_score": random.randint(580, 850),
                "avatar": f"https://api.dicebear.com/9.x/initials/svg?seed={first_name}",
                "relationship_score": random.randint(50, 100),
                "engagement_level": random.choice(["Low", "Medium", "High"]),
            }
        )
    statuses = [
        "Approved",
        "Pending",
        "Under Review",
        "Rejected",
        "Info Needed",
        "Paid Off",
    ]
    types = [
        "Personal Loan",
        "Home Improvement",
        "Debt Consolidation",
        "Business",
        "Auto Loan",
    ]
    purposes = [
        "Home Renovation",
        "Credit Card Refinance",
        "Business Expansion",
        "Car Purchase",
        "Medical Expenses",
    ]
    for i in range(60):
        borrower = random.choice(borrowers)
        app_id = f"APP-{5000 + i}"
        status = random.choice(statuses)
        created_date = fake.date_this_year()
        apps.append(
            {
                "id": app_id,
                "applicant_id": borrower["id"],
                "applicant_name": borrower["name"],
                "applicant_email": borrower["email"],
                "applicant_avatar": borrower["avatar"],
                "amount": random.randint(5000, 75000),
                "term": random.choice([12, 24, 36, 48, 60]),
                "purpose": random.choice(purposes),
                "type": random.choice(types),
                "status": status,
                "created_at": created_date.strftime("%Y-%m-%d"),
                "risk_score": borrower["credit_score"],
                "debt_to_income": round(random.uniform(10.0, 45.0), 1),
                "notes": fake.sentence(),
            }
        )

    def sort_key(x):
        return x["created_at"]

    apps.sort(key=sort_key, reverse=True)


_initialize_data()