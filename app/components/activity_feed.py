import reflex as rx
from app.states.dashboard_state import DashboardState


def activity_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.match(
                item["type"],
                (
                    "new_app",
                    rx.el.div(
                        rx.icon("file-plus", size=16, class_name="text-blue-600"),
                        class_name="p-2 rounded-full bg-blue-100/50 border border-blue-200",
                    ),
                ),
                (
                    "approval",
                    rx.el.div(
                        rx.icon("check", size=16, class_name="text-emerald-600"),
                        class_name="p-2 rounded-full bg-emerald-100/50 border border-emerald-200",
                    ),
                ),
                (
                    "disbursement",
                    rx.el.div(
                        rx.icon("dollar-sign", size=16, class_name="text-violet-600"),
                        class_name="p-2 rounded-full bg-violet-100/50 border border-violet-200",
                    ),
                ),
                (
                    "payment",
                    rx.el.div(
                        rx.icon("credit-card", size=16, class_name="text-amber-600"),
                        class_name="p-2 rounded-full bg-amber-100/50 border border-amber-200",
                    ),
                ),
                (
                    "document",
                    rx.el.div(
                        rx.icon("file-text", size=16, class_name="text-indigo-600"),
                        class_name="p-2 rounded-full bg-indigo-100/50 border border-indigo-200",
                    ),
                ),
                (
                    "review",
                    rx.el.div(
                        rx.icon("search", size=16, class_name="text-orange-600"),
                        class_name="p-2 rounded-full bg-orange-100/50 border border-orange-200",
                    ),
                ),
                rx.el.div(
                    rx.icon("bell", size=16, class_name="text-slate-600"),
                    class_name="p-2 rounded-full bg-slate-100/50 border border-slate-200",
                ),
            ),
            rx.el.div(
                class_name="absolute top-10 left-4 bottom-0 w-0.5 bg-slate-100 -z-10 group-last:hidden"
            ),
            class_name="relative mr-4",
        ),
        rx.el.div(
            rx.el.p(item["title"], class_name="text-sm font-medium text-slate-900"),
            rx.el.div(
                rx.el.span(item["user"], class_name="font-semibold text-slate-700"),
                rx.el.span(" • ", class_name="text-slate-300"),
                rx.el.span(item["time"], class_name="text-slate-400"),
                class_name="text-xs mt-0.5 flex items-center",
            ),
            class_name="flex-1 pb-6 border-b border-slate-50 group-last:border-0",
        ),
        class_name="flex items-start group",
    )


def activity_feed() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Live Activity", class_name="text-lg font-bold text-slate-900"),
            rx.el.div(
                rx.el.span(class_name="relative flex h-2.5 w-2.5 mr-2"),
                rx.el.span(
                    class_name="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"
                ),
                rx.el.span(
                    "Live", class_name="text-xs font-bold text-emerald-600 ml-1"
                ),
                class_name="flex items-center bg-emerald-50 px-2 py-1 rounded-full border border-emerald-100",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.foreach(DashboardState.activities, activity_item),
            class_name="overflow-y-auto max-h-[350px] pr-2 custom-scrollbar",
        ),
        class_name="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-sm border border-white/50 h-full",
    )