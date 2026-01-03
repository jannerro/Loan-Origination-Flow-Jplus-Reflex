import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.application_list_state import ApplicationListState
from app.states.application_detail_state import ApplicationDetailState
from app.states.borrower_profile_state import BorrowerProfileState
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.components.stats import stats_grid
from app.components.charts import dashboard_charts
from app.components.recent_apps import recent_applications_table
from app.components.application.wizard import application_wizard
from app.components.application.list import applications_table
from app.components.application.detail_views import application_detail_view
from app.components.loan_products import products_grid
from app.components.borrower_profile import borrower_profile_view
from app.components.heatmap import disbursement_heatmap
from app.components.activity_feed import activity_feed
from app.components.quick_actions import quick_actions_panel
from app.components.settings import settings_view


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    content,
                    class_name="flex-1 overflow-y-auto bg-slate-50/50 p-4 md:p-8 relative",
                ),
                rx.el.div(
                    class_name="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100/40 via-transparent to-transparent pointer-events-none -z-10"
                ),
                class_name="flex flex-col flex-1 h-screen overflow-hidden relative",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden",
        ),
        quick_actions_panel(),
        class_name="flex h-screen w-screen bg-slate-50 font-['Inter']",
    )


def index() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Dashboard Overview",
                    class_name="text-2xl font-bold text-slate-900 mb-2",
                ),
                rx.el.p(
                    "Welcome back, here's what's happening today.",
                    class_name="text-slate-500",
                ),
                class_name="mb-8",
            ),
            stats_grid(),
            dashboard_charts(),
            rx.el.div(
                rx.el.div(
                    recent_applications_table(), class_name="col-span-1 lg:col-span-2"
                ),
                rx.el.div(
                    disbursement_heatmap(),
                    activity_feed(),
                    class_name="grid grid-cols-1 gap-6",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
            ),
            class_name="max-w-7xl mx-auto pb-20",
        )
    )


def new_application() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "New Loan Application",
                    class_name="text-2xl font-bold text-slate-900 mb-2",
                ),
                rx.el.p(
                    "Complete the steps below to submit a new loan request.",
                    class_name="text-slate-500",
                ),
                class_name="mb-8",
            ),
            application_wizard(),
            class_name="max-w-7xl mx-auto",
        )
    )


def applications_list_page() -> rx.Component:
    return layout(applications_table())


def application_detail_page() -> rx.Component:
    return layout(application_detail_view())


def products_page() -> rx.Component:
    return layout(rx.el.div(products_grid(), class_name="max-w-7xl mx-auto"))


def borrower_profile_page() -> rx.Component:
    return layout(borrower_profile_view())


def settings_page() -> rx.Component:
    return layout(settings_view())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=DashboardState.on_load)
app.add_page(new_application, route="/application/new")
app.add_page(
    applications_list_page,
    route="/applications",
    on_load=ApplicationListState.load_data,
)
app.add_page(
    application_detail_page,
    route="/applications/[id]",
    on_load=ApplicationDetailState.load_application,
)
app.add_page(products_page, route="/products")
app.add_page(
    borrower_profile_page,
    route="/borrowers/[id]",
    on_load=BorrowerProfileState.load_profile,
)
app.add_page(settings_page, route="/settings")