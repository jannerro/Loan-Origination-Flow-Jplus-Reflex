import reflex as rx
from app.states.application_list_state import ApplicationListState, ApplicationListItem
from app.components.recent_apps import status_badge


def filter_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    size=18,
                    class_name="text-slate-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search by name or ID...",
                    on_change=ApplicationListState.set_search_query,
                    class_name="pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 w-64",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        ApplicationListState.statuses,
                        lambda s: rx.el.option(s, value=s),
                    ),
                    on_change=ApplicationListState.set_status_filter,
                    class_name="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-600 focus:outline-none focus:border-blue-500 cursor-pointer",
                ),
                rx.el.select(
                    rx.foreach(
                        ApplicationListState.types, lambda t: rx.el.option(t, value=t)
                    ),
                    on_change=ApplicationListState.set_type_filter,
                    class_name="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-600 focus:outline-none focus:border-blue-500 cursor-pointer",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
        ),
        class_name="w-full",
    )


def app_table_row(app: ApplicationListItem) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.a(
                rx.el.span(
                    app["id"],
                    class_name="font-mono text-xs text-blue-600 font-medium hover:underline",
                ),
                href=f"/applications/{app['id']}",
            ),
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
                    rx.el.p(
                        app["applicant_email"], class_name="text-xs text-slate-500"
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(app["type"], class_name="text-sm text-slate-600"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"${app['amount']:,}", class_name="text-sm font-medium text-slate-900"
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
                rx.icon(
                    "chevron-right",
                    size=18,
                    class_name="text-slate-400 hover:text-blue-600",
                ),
                href=f"/applications/{app['id']}",
                class_name="flex justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="hover:bg-slate-50 transition-colors border-b border-slate-50 last:border-0",
    )


def applications_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Applications", class_name="text-2xl font-bold text-slate-900 mb-6"
            ),
            filter_bar(),
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
                                "Loan Type",
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
                                "",
                                class_name="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider",
                            ),
                            class_name="bg-slate-50 border-b border-slate-100",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ApplicationListState.filtered_apps, app_table_row),
                        class_name="divide-y divide-slate-100 bg-white",
                    ),
                    class_name="min-w-full",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden overflow-x-auto",
            ),
            class_name="max-w-7xl mx-auto",
        ),
        class_name="w-full",
    )