import reflex as rx
from app.states.dashboard_state import DashboardState, AppData


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Approved",
            rx.el.span(
                status,
                class_name="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-600 border border-emerald-100",
            ),
        ),
        (
            "Pending",
            rx.el.span(
                status,
                class_name="px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-600 border border-blue-100",
            ),
        ),
        (
            "Under Review",
            rx.el.span(
                status,
                class_name="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-600 border border-amber-100",
            ),
        ),
        (
            "Rejected",
            rx.el.span(
                status,
                class_name="px-2.5 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-600 border border-red-100",
            ),
        ),
        rx.el.span(
            status,
            class_name="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-50 text-slate-600 border border-slate-100",
        ),
    )


def table_row(app: AppData) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(app["id"], class_name="font-mono text-xs text-slate-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=app["avatar"], class_name="w-8 h-8 rounded-full bg-slate-100"
                ),
                rx.el.div(
                    rx.el.p(
                        app["applicant"],
                        class_name="text-sm font-medium text-slate-900",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"${app['amount']:,.2f}",
                class_name="text-sm font-medium text-slate-900",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(app["date"], class_name="text-sm text-slate-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(status_badge(app["status"]), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.el.a(
                "View",
                href=f"/applications/{app['id']}",
                class_name="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="hover:bg-slate-50 transition-colors",
    )


def recent_applications_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Recent Applications", class_name="text-lg font-bold text-slate-900"
            ),
            rx.el.a(
                "View All",
                href="/applications",
                class_name="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors",
            ),
            class_name="flex items-center justify-between mb-6 p-6 pb-0",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "ID",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Applicant",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Amount",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Date",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Action",
                            class_name="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider",
                        ),
                        class_name="bg-slate-50 border-b border-slate-100",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(DashboardState.recent_apps, table_row),
                    class_name="divide-y divide-slate-100 bg-white",
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden",
    )