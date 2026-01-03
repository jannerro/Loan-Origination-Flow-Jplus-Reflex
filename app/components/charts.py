import reflex as rx
from app.states.dashboard_state import DashboardState


def pipeline_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Loan Pipeline Status", class_name="text-lg font-bold text-slate-900"
            ),
            rx.el.button(
                rx.icon("funnel", size=20, class_name="text-slate-400"),
                class_name="p-1 hover:bg-slate-100 rounded-lg transition-colors",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        DashboardState.active_pipeline_value,
                        class_name="text-3xl font-bold text-slate-900",
                    ),
                    rx.el.p(
                        DashboardState.active_pipeline_name,
                        class_name="text-sm font-medium text-slate-500",
                    ),
                    class_name="absolute inset-0 flex flex-col items-center justify-center pointer-events-none",
                ),
                rx.recharts.pie_chart(
                    rx.recharts.pie(
                        rx.foreach(
                            DashboardState.pipeline_data,
                            lambda item, index: rx.recharts.cell(
                                fill=item["fill"],
                                on_mouse_enter=DashboardState.set_pipeline_hover(index),
                                on_mouse_leave=DashboardState.reset_pipeline_hover,
                                stroke="",
                            ),
                        ),
                        data=DashboardState.pipeline_data,
                        data_key="value",
                        name_key="name",
                        inner_radius=60,
                        outer_radius=80,
                        padding_angle=5,
                        corner_radius=4,
                        stroke="none",
                        stroke_width=0,
                    ),
                    width="100%",
                    height=250,
                ),
                class_name="relative h-[250px] w-full flex justify-center",
            ),
            rx.el.div(
                rx.foreach(
                    DashboardState.pipeline_data,
                    lambda item: rx.el.div(
                        rx.el.div(
                            class_name="w-3 h-3 rounded-full",
                            style={"backgroundColor": item["fill"]},
                        ),
                        rx.el.span(item["name"], class_name="text-sm text-slate-600"),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex flex-wrap justify-center gap-4 mt-6",
            ),
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
    )


def create_gradient(color: str, id: str) -> rx.Component:
    return rx.el.svg.linear_gradient(
        rx.el.svg.stop(offset="5%", stop_color=color, stop_opacity=0.3),
        rx.el.svg.stop(offset="95%", stop_color=color, stop_opacity=0),
        id=id,
        x1="0",
        y1="0",
        x2="0",
        y2="1",
    )


def trend_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Volume Trends", class_name="text-lg font-bold text-slate-900"),
            rx.el.select(
                rx.el.option("Last 6 Months", value="6m"),
                rx.el.option("Last Year", value="1y"),
                class_name="text-sm bg-slate-50 border-none rounded-lg px-3 py-1 text-slate-600 focus:ring-0 cursor-pointer",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.svg(
                rx.el.svg.defs(create_gradient("#3B82F6", "colorVolume")),
                class_name="absolute",
            ),
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, stroke="#E2E8F0"
                ),
                rx.recharts.graphing_tooltip(
                    content_style={
                        "backgroundColor": "#fff",
                        "borderRadius": "8px",
                        "border": "1px solid #e2e8f0",
                        "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                    },
                    item_style={"color": "#1e293b", "fontWeight": 500},
                    separator="",
                    cursor=False,
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    axis_line=False,
                    tick_line=False,
                    tick={"fill": "#64748B", "fontSize": 12},
                    dy=10,
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick={"fill": "#64748B", "fontSize": 12},
                ),
                rx.recharts.area(
                    type_="monotone",
                    data_key="volume",
                    stroke="#3B82F6",
                    stroke_width=2,
                    fill="url(#colorVolume)",
                    active_dot={"r": 6, "strokeWidth": 0},
                ),
                data=DashboardState.trend_data,
                width="100%",
                height=300,
            ),
            class_name="h-[300px] w-full",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
    )


from app.components.where_tooltip_props_are_defined import TOOLTIP_PROPS


def health_gauge() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Portfolio Health", class_name="text-lg font-bold text-slate-900"),
            rx.el.span(
                "High Performance",
                class_name="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full",
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{DashboardState.health_score}",
                        class_name="text-4xl font-bold text-slate-900",
                    ),
                    rx.el.span("/100", class_name="text-sm text-slate-400 font-medium"),
                    class_name="absolute inset-0 flex items-center justify-center pointer-events-none",
                ),
                rx.recharts.radial_bar_chart(
                    rx.recharts.radial_bar(
                        data_key="value",
                        corner_radius=10,
                        fill="#3B82F6",
                        background=True,
                    ),
                    data=[
                        {
                            "name": "Health",
                            "value": DashboardState.health_score,
                            "fill": "#3B82F6",
                        }
                    ],
                    start_angle=180,
                    end_angle=0,
                    inner_radius="70%",
                    outer_radius="100%",
                    bar_size=16,
                    width="100%",
                    height=200,
                ),
                class_name="relative h-[160px] flex justify-center -mb-8 overflow-hidden",
            ),
            rx.el.div(
                rx.foreach(
                    DashboardState.risk_factors,
                    lambda factor: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                factor["name"],
                                class_name="text-xs font-medium text-slate-500",
                            ),
                            rx.el.span(
                                f"{factor['value']}%",
                                class_name="text-xs font-bold text-slate-700",
                            ),
                            class_name="flex justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name=f"h-full rounded-full {factor['color']}",
                                style={"width": f"{factor['value']}%"},
                            ),
                            class_name="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden",
                        ),
                        class_name="mb-3",
                    ),
                ),
                class_name="mt-4",
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-sm border border-white/50",
    )


def regional_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Regional Distribution", class_name="text-lg font-bold text-slate-900 mb-6"
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    vertical=False,
                    horizontal=True,
                    stroke_dasharray="3 3",
                    class_name="opacity-50",
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.x_axis(
                    data_key="name",
                    axis_line=False,
                    tick_line=False,
                    tick={"fontSize": 11, "fill": "#64748B"},
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick={"fontSize": 11, "fill": "#64748B"},
                ),
                rx.recharts.bar(
                    data_key="value", fill="#3B82F6", radius=[4, 4, 0, 0], bar_size=30
                ),
                data=DashboardState.regional_data,
                width="100%",
                height=220,
            ),
            class_name="w-full h-[220px] mb-4",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.regional_data,
                lambda item: rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            item["name"], class_name="font-medium text-slate-700"
                        ),
                        rx.el.div(item["amount"], class_name="text-slate-500 text-xs"),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        item["trend"],
                        class_name="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full",
                    ),
                    class_name="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50/50 transition-colors",
                ),
            ),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-sm border border-white/50",
    )


def dashboard_charts() -> rx.Component:
    return rx.el.div(
        rx.el.div(trend_chart(), class_name="col-span-1 lg:col-span-2"),
        health_gauge(),
        pipeline_chart(),
        regional_chart(),
        class_name="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-6 mb-8",
    )