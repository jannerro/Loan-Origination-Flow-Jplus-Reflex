import reflex as rx
from app.states.dashboard_state import DashboardState


def action_item(
    icon: str, label: str, shortcut: str, color: str = "text-slate-500"
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(
                icon,
                size=20,
                class_name=f"{color} group-hover:scale-110 transition-transform",
            ),
            rx.el.span(
                label,
                class_name="font-medium text-slate-700 ml-3 group-hover:text-slate-900",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(
            shortcut,
            class_name="text-xs font-mono text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200",
        ),
        class_name="w-full flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 border border-transparent hover:border-slate-100 transition-all group",
    )


def quick_actions_panel() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("zap", size=24, class_name="text-white"),
            on_click=DashboardState.toggle_quick_actions,
            class_name="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full shadow-lg shadow-blue-500/30 flex items-center justify-center hover:scale-110 active:scale-95 transition-all z-50 cursor-pointer",
        ),
        rx.cond(
            DashboardState.quick_actions_open,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Quick Actions",
                            class_name="text-lg font-bold text-slate-900",
                        ),
                        rx.el.button(
                            rx.icon("x", size=20),
                            on_click=DashboardState.toggle_quick_actions,
                            class_name="text-slate-400 hover:text-slate-600",
                        ),
                        class_name="flex justify-between items-center mb-4 pb-4 border-b border-slate-100",
                    ),
                    rx.el.div(
                        action_item(
                            "circle_play", "New Application", "⌘+N", "text-blue-600"
                        ),
                        action_item(
                            "search", "Search Records", "⌘+K", "text-indigo-600"
                        ),
                        action_item(
                            "file-text", "Generate Report", "⌘+R", "text-emerald-600"
                        ),
                        action_item(
                            "users", "Browse Borrowers", "⌘+B", "text-amber-600"
                        ),
                        class_name="space-y-2",
                    ),
                    class_name="bg-white rounded-2xl shadow-2xl p-6 w-80 border border-slate-100 animate-in slide-in-from-bottom-5 fade-in duration-200",
                ),
                class_name="fixed bottom-24 right-8 z-40",
            ),
        ),
    )