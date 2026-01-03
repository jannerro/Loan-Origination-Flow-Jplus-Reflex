import reflex as rx
from app.states.application_state import ApplicationState


def step_item(step: str, index: int) -> rx.Component:
    is_completed = ApplicationState.current_step > index
    is_current = ApplicationState.current_step == index
    return rx.el.div(
        rx.cond(
            index != 0,
            rx.el.div(
                class_name=rx.cond(
                    is_completed | is_current,
                    "absolute top-4 -left-[50%] w-full h-0.5 bg-blue-600 transition-colors duration-500",
                    "absolute top-4 -left-[50%] w-full h-0.5 bg-slate-200 transition-colors duration-500",
                )
            ),
        ),
        rx.el.div(
            rx.cond(
                is_completed,
                rx.icon("check", size=16, class_name="text-white"),
                rx.el.span(
                    f"{index + 1}",
                    class_name=rx.cond(is_current, "text-blue-600", "text-slate-500"),
                ),
            ),
            class_name=rx.cond(
                is_completed,
                "w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center z-10 relative transition-all duration-300",
                rx.cond(
                    is_current,
                    "w-8 h-8 rounded-full bg-white border-2 border-blue-600 flex items-center justify-center font-bold z-10 relative shadow-md transition-all duration-300",
                    "w-8 h-8 rounded-full bg-slate-100 border-2 border-slate-200 flex items-center justify-center text-sm font-medium z-10 relative transition-all duration-300",
                ),
            ),
        ),
        rx.el.span(
            step,
            class_name=rx.cond(
                is_current,
                "absolute top-10 text-xs font-bold text-blue-600 whitespace-nowrap",
                rx.cond(
                    is_completed,
                    "absolute top-10 text-xs font-medium text-slate-900 whitespace-nowrap",
                    "absolute top-10 text-xs font-medium text-slate-400 whitespace-nowrap",
                ),
            ),
        ),
        class_name="relative flex flex-col items-center flex-1",
    )


def step_indicator() -> rx.Component:
    return rx.el.div(
        rx.foreach(ApplicationState.steps, lambda step, index: step_item(step, index)),
        class_name="flex items-center justify-between w-full px-4 mb-12",
    )