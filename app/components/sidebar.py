import reflex as rx
from app.states.data_store import borrowers


def sidebar_item(
    text: str, icon: str, href: str = "#", match_path: str = None
) -> rx.Component:
    match_str = match_path if match_path else href
    is_active = rx.cond(
        match_str == "/",
        rx.State.router.page.path == "/",
        rx.State.router.page.path.contains(match_str),
    )
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon,
                size=20,
                class_name=rx.cond(
                    is_active,
                    "text-blue-600",
                    "text-slate-500 group-hover:text-blue-600 transition-colors",
                ),
            ),
            rx.el.span(
                text,
                class_name=rx.cond(
                    is_active,
                    "font-medium text-slate-900",
                    "font-medium text-slate-600 group-hover:text-slate-900",
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center px-3 py-2.5 rounded-lg bg-blue-50 border border-blue-100 shadow-sm shadow-blue-100/50 transition-all cursor-pointer group",
            "flex items-center px-3 py-2.5 rounded-lg hover:bg-slate-50 border border-transparent transition-all cursor-pointer group",
        ),
    )


def sidebar() -> rx.Component:
    new_app_active = rx.State.router.page.path == "/application/new"
    first_borrower_id = borrowers[0]["id"] if borrowers else "BOR-1000"
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("landmark", size=28, class_name="text-blue-600"),
                rx.el.span("Loan", class_name="text-xl font-bold text-slate-900"),
                rx.el.span("Flow", class_name="text-xl font-bold text-blue-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="h-16 flex items-center px-6 border-b border-slate-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "MAIN MENU",
                    class_name="text-xs font-semibold text-slate-400 mb-4 px-3",
                ),
                rx.el.nav(
                    sidebar_item("Dashboard", "layout-dashboard", "/"),
                    rx.el.a(
                        rx.el.div(
                            rx.icon("circle_play", size=20, class_name="text-blue-600"),
                            rx.el.span(
                                "New Application",
                                class_name="font-medium text-blue-600",
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        href="/application/new",
                        class_name=rx.cond(
                            new_app_active,
                            "flex items-center px-3 py-2.5 rounded-lg bg-blue-100 border border-blue-200 shadow-md mb-2 transition-all cursor-pointer",
                            "flex items-center px-3 py-2.5 rounded-lg bg-blue-50/50 border border-blue-100 mb-2 transition-all cursor-pointer hover:bg-blue-50 hover:shadow-sm",
                        ),
                    ),
                    sidebar_item("Applications", "file-text", "/applications"),
                    sidebar_item("Loan Products", "briefcase", "/products"),
                    sidebar_item(
                        "Borrowers",
                        "users",
                        f"/borrowers/{first_borrower_id}",
                        match_path="/borrowers",
                    ),
                    sidebar_item("Settings", "settings", "/settings"),
                    class_name="space-y-1",
                ),
                class_name="py-6 px-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src="https://api.dicebear.com/9.x/avataaars/svg?seed=Felix",
                            class_name="w-10 h-10 rounded-full bg-slate-100 ring-2 ring-white",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Alex Morgan",
                                class_name="text-sm font-semibold text-slate-900",
                            ),
                            rx.el.p(
                                "Loan Officer", class_name="text-xs text-slate-500"
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.icon(
                        "log-out",
                        size=18,
                        class_name="text-slate-400 hover:text-red-500 cursor-pointer transition-colors",
                    ),
                    class_name="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100",
                ),
                class_name="mt-auto p-4",
            ),
            class_name="flex flex-col h-[calc(100vh-64px)] overflow-y-auto",
        ),
        class_name="w-64 bg-white border-r border-slate-200 h-screen hidden lg:flex flex-col sticky top-0",
    )