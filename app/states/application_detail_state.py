import reflex as rx
from typing import TypedDict, Any
import datetime


class TimelineEvent(TypedDict):
    date: str
    title: str
    description: str
    icon: str
    color: str


class DetailedApp(TypedDict):
    id: str
    applicant: str
    applicant_id: str
    email: str
    phone: str
    address: str
    status: str
    amount: int
    term: int
    purpose: str
    type: str
    created_at: str
    credit_score: int
    risk_level: str
    debt_to_income: float
    notes: str
    avatar: str


class ApplicationDetailState(rx.State):
    app_data: DetailedApp = {
        "id": "",
        "applicant": "",
        "applicant_id": "",
        "email": "",
        "phone": "",
        "address": "",
        "status": "",
        "amount": 0,
        "term": 0,
        "purpose": "",
        "type": "",
        "created_at": "",
        "credit_score": 0,
        "risk_level": "",
        "debt_to_income": 0.0,
        "notes": "",
        "avatar": "",
    }
    timeline: list[TimelineEvent] = []
    new_note: str = ""

    @rx.var
    def risk_color(self) -> str:
        if self.app_data["risk_level"] == "Low":
            return "text-emerald-600 bg-emerald-50 border-emerald-100"
        elif self.app_data["risk_level"] == "Medium":
            return "text-amber-600 bg-amber-50 border-amber-100"
        else:
            return "text-red-600 bg-red-50 border-red-100"

    @rx.var
    def score_color(self) -> str:
        score = self.app_data["credit_score"]
        if score >= 750:
            return "text-emerald-500"
        if score >= 650:
            return "text-blue-500"
        if score >= 600:
            return "text-amber-500"
        return "text-red-500"

    @rx.event
    def load_application(self):
        from app.states.data_store import apps, borrowers

        app_id = self.router.page.params.get("id")
        found_app = None
        for app in apps:
            if app["id"] == app_id:
                found_app = app
                break
        if not found_app and apps:
            found_app = apps[0]
        if found_app:
            found_borrower = None
            for b in borrowers:
                if b["id"] == found_app["applicant_id"]:
                    found_borrower = b
                    break
            if found_borrower:
                risk_level = (
                    "Low"
                    if found_app["risk_score"] >= 700
                    else "Medium"
                    if found_app["risk_score"] >= 600
                    else "High"
                )
                self.app_data = {
                    "id": found_app["id"],
                    "applicant": found_app["applicant_name"],
                    "applicant_id": found_app["applicant_id"],
                    "email": found_app["applicant_email"],
                    "phone": found_borrower["phone"],
                    "address": found_borrower["address"],
                    "status": found_app["status"],
                    "amount": found_app["amount"],
                    "term": found_app["term"],
                    "purpose": found_app["purpose"],
                    "type": found_app["type"],
                    "created_at": found_app["created_at"],
                    "credit_score": found_app["risk_score"],
                    "risk_level": risk_level,
                    "debt_to_income": found_app["debt_to_income"],
                    "notes": found_app["notes"],
                    "avatar": found_app["applicant_avatar"],
                }
                base_date = datetime.datetime.strptime(
                    found_app["created_at"], "%Y-%m-%d"
                )
                self.timeline = [
                    {
                        "date": base_date.strftime("%b %d, %Y 10:30 AM"),
                        "title": "Application Submitted",
                        "description": "Applicant completed the online wizard.",
                        "icon": "file-text",
                        "color": "bg-blue-500",
                    },
                    {
                        "date": base_date.strftime("%b %d, %Y 10:35 AM"),
                        "title": "Credit Check Completed",
                        "description": "Credit report pulled successfully.",
                        "icon": "search",
                        "color": "bg-emerald-500",
                    },
                ]
                if found_app["status"] != "Pending":
                    self.timeline.insert(
                        0,
                        {
                            "date": (base_date + datetime.timedelta(days=1)).strftime(
                                "%b %d, %Y 09:15 AM"
                            ),
                            "title": "Underwriting Started",
                            "description": "Assigned to loan officer Alex Morgan.",
                            "icon": "user",
                            "color": "bg-amber-500",
                        },
                    )
                if found_app["status"] in ["Approved", "Rejected", "Info Needed"]:
                    status_color = (
                        "bg-emerald-500"
                        if found_app["status"] == "Approved"
                        else "bg-red-500"
                        if found_app["status"] == "Rejected"
                        else "bg-violet-500"
                    )
                    self.timeline.insert(
                        0,
                        {
                            "date": (base_date + datetime.timedelta(days=2)).strftime(
                                "%b %d, %Y 02:00 PM"
                            ),
                            "title": f"Status: {found_app['status']}",
                            "description": f"Application marked as {found_app['status']}.",
                            "icon": "check-circle",
                            "color": status_color,
                        },
                    )

    @rx.event
    def update_status(self, new_status: str):
        from app.states.data_store import apps

        self.app_data["status"] = new_status
        for app in apps:
            if app["id"] == self.app_data["id"]:
                app["status"] = new_status
                break
        self.timeline.insert(
            0,
            {
                "date": datetime.datetime.now().strftime("%b %d, %Y %I:%M %p"),
                "title": f"Status Changed to {new_status}",
                "description": f"Application marked as {new_status} by system user.",
                "icon": "refresh-cw",
                "color": "bg-violet-500",
            },
        )
        return rx.toast(f"Application marked as {new_status}")

    @rx.event
    def set_new_note(self, value: str):
        self.new_note = value

    @rx.event
    def add_note_entry(self):
        if not self.new_note:
            return
        self.timeline.insert(
            0,
            {
                "date": datetime.datetime.now().strftime("%b %d, %Y %I:%M %p"),
                "title": "Note Added",
                "description": self.new_note,
                "icon": "message-square",
                "color": "bg-slate-500",
            },
        )
        self.new_note = ""
        return rx.toast("Note added to timeline")

    @rx.event
    def export_pdf(self):
        import io
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import (
            SimpleDocTemplate,
            Table,
            TableStyle,
            Paragraph,
            Spacer,
        )
        from reportlab.lib.styles import getSampleStyleSheet

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        title_style.alignment = 1
        elements.append(Paragraph("Loan Application Report", title_style))
        elements.append(Spacer(1, 12))
        header_data = [
            ["Application ID:", self.app_data["id"]],
            ["Date Created:", self.app_data["created_at"]],
            ["Current Status:", self.app_data["status"]],
        ]
        t_header = Table(header_data, colWidths=[150, 300])
        t_header.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(t_header)
        elements.append(Spacer(1, 20))

        @rx.event
        def add_section_header(text):
            style = styles["Heading2"]
            style.textColor = colors.HexColor("#2563EB")
            elements.append(Paragraph(text, style))
            elements.append(Spacer(1, 10))

        add_section_header("Borrower Information")
        borrower_data = [
            ["Name:", self.app_data["applicant"]],
            ["Email:", self.app_data["email"]],
            ["Phone:", self.app_data["phone"]],
            ["Address:", self.app_data["address"]],
        ]
        t_borrower = Table(borrower_data, colWidths=[150, 350])
        t_borrower.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        elements.append(t_borrower)
        elements.append(Spacer(1, 20))
        add_section_header("Loan Details")
        loan_data = [
            ["Amount Requested:", f"${self.app_data['amount']:,}"],
            ["Term Length:", f"{self.app_data['term']} months"],
            ["Loan Type:", self.app_data["type"]],
            ["Purpose:", self.app_data["purpose"]],
        ]
        t_loan = Table(loan_data, colWidths=[150, 350])
        t_loan.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        elements.append(t_loan)
        elements.append(Spacer(1, 20))
        add_section_header("Credit Assessment")
        credit_data = [
            ["Credit Score:", str(self.app_data["credit_score"])],
            ["Risk Level:", self.app_data["risk_level"]],
            ["Debt-to-Income:", f"{self.app_data['debt_to_income']}%"],
        ]
        t_credit = Table(credit_data, colWidths=[150, 350])
        t_credit.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        elements.append(t_credit)
        elements.append(Spacer(1, 20))
        add_section_header("Activity Timeline")
        timeline_data = [["Date", "Event", "Description"]]
        for event in self.timeline:
            timeline_data.append(
                [
                    event["date"],
                    event["title"],
                    Paragraph(event["description"], styles["Normal"]),
                ]
            )
        t_timeline = Table(timeline_data, colWidths=[120, 150, 230])
        t_timeline.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ("PADDING", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        elements.append(t_timeline)
        doc.build(elements)
        pdf_data = buffer.getvalue()
        buffer.close()
        return rx.download(
            data=pdf_data, filename=f"Loan_Application_{self.app_data['id']}.pdf"
        )