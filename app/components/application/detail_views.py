import reflex as rx
from app.states.application_detail_state import ApplicationDetailState, TimelineEvent
from app.components.recent_apps import status_badge


def detail_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Application {ApplicationDetailState.app_data['id']}",
                    class_name="text-2xl font-bold text-slate-900 mr-4",
                ),
                status_badge(ApplicationDetailState.app_data["status"]),
                class_name="flex items-center mb-1",
            ),
            rx.el.p(
                f"Submitted on {ApplicationDetailState.app_data['created_at']} via Online Portal",
                class_name="text-sm text-slate-500",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.button(
                "Export PDF",
                on_click=ApplicationDetailState.export_pdf,
                class_name="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 mr-3",
            ),
            rx.el.button(
                "Message Borrower",
                class_name="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 shadow-sm",
            ),
            class_name="flex items-center mt-4 md:mt-0",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between mb-8",
    )


def info_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-sm text-slate-500"),
        rx.el.span(value, class_name="text-sm font-medium text-slate-900 text-right"),
        class_name="flex justify-between py-3 border-b border-slate-50 last:border-0",
    )


def borrower_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Borrower Profile", class_name="text-lg font-bold text-slate-900"),
            rx.el.a(
                "View Full Profile",
                href=f"/borrowers/{ApplicationDetailState.app_data['applicant_id']}",
                class_name="text-sm font-medium text-blue-600 hover:underline",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.image(
                src=ApplicationDetailState.app_data["avatar"],
                class_name="w-16 h-16 rounded-full bg-slate-100 mb-4",
            ),
            rx.el.h4(
                ApplicationDetailState.app_data["applicant"],
                class_name="text-lg font-bold text-slate-900",
            ),
            rx.el.p(
                ApplicationDetailState.app_data["applicant_id"],
                class_name="text-sm text-slate-500 mb-6",
            ),
            class_name="flex flex-col items-center",
        ),
        rx.el.div(
            info_row("Email", ApplicationDetailState.app_data["email"]),
            info_row("Phone", ApplicationDetailState.app_data["phone"]),
            info_row("Address", ApplicationDetailState.app_data["address"]),
            class_name="space-y-1",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
    )


def loan_info_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Loan Details", class_name="text-lg font-bold text-slate-900 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.p("Requested Amount", class_name="text-sm text-slate-500 mb-1"),
                rx.el.p(
                    f"${ApplicationDetailState.app_data['amount']:,}",
                    class_name="text-3xl font-bold text-slate-900",
                ),
                class_name="mb-6 p-4 bg-slate-50 rounded-xl",
            ),
            info_row("Loan Type", ApplicationDetailState.app_data["type"]),
            info_row(
                "Term Length", f"{ApplicationDetailState.app_data['term']} months"
            ),
            info_row("Purpose", ApplicationDetailState.app_data["purpose"]),
            info_row("Monthly Payment (Est)", "$845.20"),
            class_name="space-y-1",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
    )


def credit_analysis_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Credit Assessment", class_name="text-lg font-bold text-slate-900 mb-6"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{ApplicationDetailState.app_data['credit_score']}",
                        class_name=f"text-4xl font-bold {ApplicationDetailState.score_color}",
                    ),
                    rx.el.span(
                        "Credit Score",
                        class_name="text-xs text-slate-500 uppercase mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center w-32 h-32 rounded-full border-4 border-slate-100 mb-4",
                ),
                class_name="flex justify-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Risk Level", class_name="text-sm text-slate-500"),
                    rx.el.span(
                        ApplicationDetailState.app_data["risk_level"],
                        class_name=f"px-2 py-0.5 rounded text-xs font-bold uppercase {ApplicationDetailState.risk_color}",
                    ),
                    class_name="flex justify-between items-center mb-2",
                ),
                rx.el.div(
                    rx.el.span("Debt-to-Income", class_name="text-sm text-slate-500"),
                    rx.el.span(
                        f"{ApplicationDetailState.app_data['debt_to_income']}%",
                        class_name="text-sm font-bold text-slate-900",
                    ),
                    class_name="flex justify-between items-center",
                ),
                class_name="bg-slate-50 p-4 rounded-xl",
            ),
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
    )


def timeline_item(event: TimelineEvent) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(event["icon"], size=16, class_name="text-white"),
            class_name=f"absolute left-0 p-1.5 rounded-full ring-4 ring-white {event['color']}",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(event["title"], class_name="text-sm font-bold text-slate-900"),
                rx.el.p(event["date"], class_name="text-xs text-slate-400"),
                class_name="flex justify-between items-start mb-0.5",
            ),
            rx.el.p(event["description"], class_name="text-sm text-slate-600"),
            class_name="ml-10 pb-6 border-l-2 border-slate-100 pl-6",
        ),
        class_name="relative",
    )


def workflow_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Workflow Actions", class_name="text-lg font-bold text-slate-900 mb-6"
        ),
        rx.el.div(
            rx.el.button(
                "Approve Application",
                on_click=lambda: ApplicationDetailState.update_status("Approved"),
                class_name="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium shadow-sm transition-colors mb-3",
            ),
            rx.el.button(
                "Request Information",
                on_click=lambda: ApplicationDetailState.update_status("Info Needed"),
                class_name="w-full py-2 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg font-medium transition-colors mb-3",
            ),
            rx.el.button(
                "Reject Application",
                on_click=lambda: ApplicationDetailState.update_status("Rejected"),
                class_name="w-full py-2 bg-white border border-red-200 text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.h4("Add Note", class_name="text-sm font-bold text-slate-900 mb-2"),
            rx.el.textarea(
                placeholder="Enter internal note...",
                on_change=ApplicationDetailState.set_new_note,
                class_name="w-full p-3 border border-slate-200 rounded-lg text-sm mb-3 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none min-h-[100px]",
                default_value=ApplicationDetailState.new_note,
            ),
            rx.el.button(
                "Post Note",
                on_click=ApplicationDetailState.add_note_entry,
                class_name="px-4 py-2 bg-slate-900 text-white text-sm font-medium rounded-lg hover:bg-slate-800 transition-colors",
            ),
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
    )


def application_detail_view() -> rx.Component:
    return rx.el.div(
        detail_header(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    borrower_card(),
                    loan_info_card(),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Activity Timeline",
                        class_name="text-lg font-bold text-slate-900 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(ApplicationDetailState.timeline, timeline_item),
                        class_name="pl-2",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
                ),
                class_name="col-span-1 lg:col-span-2 space-y-6",
            ),
            rx.el.div(
                credit_analysis_card(),
                workflow_card(),
                class_name="col-span-1 space-y-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
        class_name="w-full max-w-7xl mx-auto",
    )