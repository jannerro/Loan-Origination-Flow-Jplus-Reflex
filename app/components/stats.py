import reflex as rx
from app.states.dashboard_state import DashboardState, MetricData


def stat_card(metric: MetricData) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(tag=metric["icon"], size=24, class_name="text-white"),
                    class_name=f"w-12 h-12 rounded-xl flex items-center justify-center shadow-lg {metric['color']} bg-gradient-to-br from-opacity-80 to-opacity-100 backdrop-blur-sm",
                ),
                rx.el.div(
                    rx.cond(
                        metric["is_positive"],
                        rx.el.div(
                            rx.icon("trending-up", size=14, class_name="mr-1"),
                            f"{metric['change']}%",
                            class_name="flex items-center text-xs font-semibold text-emerald-600 bg-emerald-50/80 px-2 py-1 rounded-full w-fit border border-emerald-100",
                        ),
                        rx.el.div(
                            rx.icon("trending-down", size=14, class_name="mr-1"),
                            f"{metric['change']}%",
                            class_name="flex items-center text-xs font-semibold text-red-600 bg-red-50/80 px-2 py-1 rounded-full w-fit border border-red-100",
                        ),
                    ),
                    class_name="flex flex-col items-end",
                ),
                class_name="flex justify-between items-start mb-4",
            ),
            rx.el.div(
                rx.el.p(
                    metric["title"],
                    class_name="text-sm font-medium text-slate-500 mb-1",
                ),
                rx.el.h3(
                    metric["value"],
                    class_name="text-3xl font-bold text-slate-900 tracking-tight",
                ),
            ),
        ),
        class_name="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-sm border border-white/50 hover:shadow-xl hover:-translate-y-1 transition-all duration-300",
    )


def stats_grid() -> rx.Component:
    return rx.el.div(
        rx.foreach(DashboardState.metrics, stat_card),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
    )