import reflex as rx
from app.states.dashboard_state import DashboardState


def heatmap_cell(item: dict) -> rx.Component:
    return rx.recharts.graphing_tooltip(
        rx.el.div(
            class_name=f"w-3 h-3 rounded-sm {item['color']} hover:ring-2 ring-offset-1 ring-blue-300 transition-all cursor-default",
            title=f"Disbursements: {item['value']} ({item['date']})",
        )
    )


def disbursement_heatmap() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Disbursement Intensity", class_name="text-lg font-bold text-slate-900"
            ),
            rx.el.div(
                rx.el.span("Less", class_name="text-xs text-slate-400 mr-2"),
                rx.el.div(class_name="w-2 h-2 rounded-sm bg-blue-200"),
                rx.el.div(class_name="w-2 h-2 rounded-sm bg-blue-400"),
                rx.el.div(class_name="w-2 h-2 rounded-sm bg-blue-600"),
                rx.el.div(class_name="w-2 h-2 rounded-sm bg-blue-800"),
                rx.el.span("More", class_name="text-xs text-slate-400 ml-2"),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.foreach(DashboardState.heatmap_data, heatmap_cell),
            class_name="grid grid-cols-12 gap-1.5 w-full",
        ),
        class_name="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-sm border border-white/50 h-full",
    )