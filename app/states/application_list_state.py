import reflex as rx
from typing import TypedDict
import random
from faker import Faker

fake = Faker()


class ApplicationListItem(TypedDict):
    id: str
    applicant: str
    applicant_email: str
    amount: int
    date: str
    status: str
    type: str
    risk_score: int
    avatar: str


class ApplicationListState(rx.State):
    apps: list[ApplicationListItem] = []
    filtered_apps: list[ApplicationListItem] = []
    status_filter: str = "All"
    type_filter: str = "All"
    search_query: str = ""
    statuses: list[str] = [
        "All",
        "Approved",
        "Pending",
        "Under Review",
        "Rejected",
        "Info Needed",
    ]
    types: list[str] = [
        "All",
        "Personal Loan",
        "Home Improvement",
        "Debt Consolidation",
        "Business",
    ]

    @rx.event
    def load_data(self):
        from app.states.data_store import apps

        mapped_apps = []
        for app in apps:
            mapped_apps.append(
                {
                    "id": app["id"],
                    "applicant": app["applicant_name"],
                    "applicant_email": app["applicant_email"],
                    "amount": app["amount"],
                    "date": app["created_at"],
                    "status": app["status"],
                    "type": app["type"],
                    "risk_score": app["risk_score"],
                    "avatar": app["applicant_avatar"],
                }
            )
        self.apps = mapped_apps
        self.filter_apps()

    @rx.event
    def set_status_filter(self, value: str):
        self.status_filter = value
        self.filter_apps()

    @rx.event
    def set_type_filter(self, value: str):
        self.type_filter = value
        self.filter_apps()

    @rx.event
    def set_search_query(self, value: str):
        self.search_query = value
        self.filter_apps()

    @rx.event
    def filter_apps(self):
        filtered = self.apps
        if self.status_filter != "All":
            filtered = [app for app in filtered if app["status"] == self.status_filter]
        if self.type_filter != "All":
            filtered = [app for app in filtered if app["type"] == self.type_filter]
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                app
                for app in filtered
                if query in app["applicant"].lower() or query in app["id"].lower()
            ]
        self.filtered_apps = filtered