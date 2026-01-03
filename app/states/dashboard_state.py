import reflex as rx
from typing import TypedDict
import random
from faker import Faker

fake = Faker()


class AppData(TypedDict):
    id: str
    applicant: str
    amount: float
    date: str
    status: str
    avatar: str


class MetricData(TypedDict):
    title: str
    value: str
    change: float
    is_positive: bool
    icon: str
    color: str


class ChartData(TypedDict):
    name: str
    value: int
    fill: str


class TrendData(TypedDict):
    name: str
    volume: int
    applications: int


class DashboardState(rx.State):
    metrics: list[MetricData] = [
        {
            "title": "Total Applications",
            "value": "1,234",
            "change": 12.5,
            "is_positive": True,
            "icon": "file-text",
            "color": "bg-blue-500",
        },
        {
            "title": "Approved Loans",
            "value": "856",
            "change": 8.2,
            "is_positive": True,
            "icon": "check-circle",
            "color": "bg-emerald-500",
        },
        {
            "title": "Pending Review",
            "value": "145",
            "change": -2.4,
            "is_positive": False,
            "icon": "clock",
            "color": "bg-amber-500",
        },
        {
            "title": "Total Disbursed",
            "value": "$42.5M",
            "change": 15.3,
            "is_positive": True,
            "icon": "dollar-sign",
            "color": "bg-violet-500",
        },
    ]
    pipeline_data: list[ChartData] = [
        {"name": "Approved", "value": 45, "fill": "#10B981"},
        {"name": "Under Review", "value": 25, "fill": "#F59E0B"},
        {"name": "Pending Info", "value": 20, "fill": "#3B82F6"},
        {"name": "Rejected", "value": 10, "fill": "#EF4444"},
    ]
    active_pipeline_name: str = "Total"
    active_pipeline_value: str = "100%"

    @rx.event
    def set_pipeline_hover(self, index: int):
        data = self.pipeline_data[index]
        self.active_pipeline_name = data["name"]
        self.active_pipeline_value = f"{data['value']}%"

    @rx.event
    def reset_pipeline_hover(self):
        self.active_pipeline_name = "Total"
        self.active_pipeline_value = "100%"

    trend_data: list[TrendData] = [
        {"name": "Jan", "volume": 2400, "applications": 120},
        {"name": "Feb", "volume": 1398, "applications": 98},
        {"name": "Mar", "volume": 9800, "applications": 150},
        {"name": "Apr", "volume": 3908, "applications": 110},
        {"name": "May", "volume": 4800, "applications": 130},
        {"name": "Jun", "volume": 3800, "applications": 115},
        {"name": "Jul", "volume": 4300, "applications": 140},
    ]
    recent_apps: list[AppData] = []

    @rx.event
    def load_recent_apps(self):
        from app.states.data_store import apps

        new_apps = []
        for app in apps[:7]:
            new_apps.append(
                {
                    "id": app["id"],
                    "applicant": app["applicant_name"],
                    "amount": app["amount"],
                    "date": app["created_at"],
                    "status": app["status"],
                    "avatar": app["applicant_avatar"],
                }
            )
        self.recent_apps = new_apps

    health_score: int = 85
    risk_factors: list[dict] = [
        {"name": "Credit Score", "value": 92, "color": "bg-emerald-500"},
        {"name": "Debt-to-Income", "value": 78, "color": "bg-blue-500"},
        {"name": "Loan-to-Value", "value": 65, "color": "bg-amber-500"},
        {"name": "Payment History", "value": 88, "color": "bg-emerald-500"},
    ]
    heatmap_data: list[dict] = []
    regional_data: list[dict] = [
        {"name": "California", "value": 450, "amount": "$12.5M", "trend": "+12%"},
        {"name": "Texas", "value": 320, "amount": "$8.2M", "trend": "+8%"},
        {"name": "Florida", "value": 280, "amount": "$6.8M", "trend": "+15%"},
        {"name": "New York", "value": 240, "amount": "$9.1M", "trend": "-2%"},
        {"name": "Illinois", "value": 190, "amount": "$4.5M", "trend": "+5%"},
    ]
    activities: list[dict] = []
    quick_actions_open: bool = False

    @rx.event
    def toggle_quick_actions(self):
        self.quick_actions_open = not self.quick_actions_open

    @rx.event
    def load_heatmap_data(self):
        data = []
        for i in range(84):
            val = random.randint(0, 4)
            color = "bg-slate-100"
            if val == 1:
                color = "bg-blue-200"
            elif val == 2:
                color = "bg-blue-400"
            elif val == 3:
                color = "bg-blue-600"
            elif val == 4:
                color = "bg-blue-800"
            data.append({"value": val, "color": color, "date": f"Day {i}"})
        self.heatmap_data = data

    @rx.event
    def load_activities(self):
        from app.states.data_store import apps

        acts = []
        recent_apps = apps[:15]
        time_offsets = [
            "2m ago",
            "5m ago",
            "12m ago",
            "28m ago",
            "45m ago",
            "1h ago",
            "2h ago",
            "3h ago",
            "5h ago",
            "1d ago",
            "1d ago",
            "2d ago",
            "3d ago",
            "3d ago",
            "4d ago",
        ]
        for i, app in enumerate(recent_apps):
            if i >= len(time_offsets):
                break
            status = app["status"]
            applicant = app["applicant_name"]
            app_id = app["id"]
            amount_str = f"${app['amount']:,}"
            if status == "Pending":
                acts.append(
                    {
                        "type": "new_app",
                        "title": f"{applicant} submitted {amount_str} {app['type']} application",
                        "time": time_offsets[i],
                        "user": applicant,
                    }
                )
            elif status == "Approved":
                if i % 3 == 0:
                    acts.append(
                        {
                            "type": "disbursement",
                            "title": f"{amount_str} disbursed to {applicant}",
                            "time": time_offsets[i],
                            "user": "Finance Team",
                        }
                    )
                else:
                    acts.append(
                        {
                            "type": "approval",
                            "title": f"{applicant}'s application {app_id} approved",
                            "time": time_offsets[i],
                            "user": "Underwriting Team",
                        }
                    )
            elif status == "Under Review":
                acts.append(
                    {
                        "type": "review",
                        "title": f"Application {app_id} is under review",
                        "time": time_offsets[i],
                        "user": "Loan Officer",
                    }
                )
            elif status == "Info Needed":
                acts.append(
                    {
                        "type": "document",
                        "title": f"Document request sent to {applicant}",
                        "time": time_offsets[i],
                        "user": "System",
                    }
                )
            elif status == "Rejected":
                acts.append(
                    {
                        "type": "review",
                        "title": f"Decision reached for application {app_id}",
                        "time": time_offsets[i],
                        "user": "Risk Team",
                    }
                )
            else:
                acts.append(
                    {
                        "type": "review",
                        "title": f"Status update for {app_id}: {status}",
                        "time": time_offsets[i],
                        "user": "System",
                    }
                )
        if len(acts) > 2:
            acts.insert(
                2,
                {
                    "type": "document",
                    "title": f"Pay stub verified for {recent_apps[2]['applicant_name']}",
                    "time": "15m ago",
                    "user": "Verification Team",
                },
            )
        if len(acts) > 5:
            acts.insert(
                5,
                {
                    "type": "payment",
                    "title": f"Payment received for loan {recent_apps[4]['id']}",
                    "time": "1h ago",
                    "user": "System",
                },
            )
        self.activities = acts

    @rx.event
    def on_load(self):
        self.load_recent_apps()
        self.load_heatmap_data()
        self.load_activities()