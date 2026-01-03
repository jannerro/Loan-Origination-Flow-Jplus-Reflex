import reflex as rx
from app.states.application_state import ApplicationState
from app.components.application.step_indicator import step_indicator
from app.components.application.steps import (
    personal_info_step,
    employment_info_step,
    loan_details_step,
    documents_step,
    review_step,
)


def wizard_actions() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Back",
            on_click=ApplicationState.prev_step,
            disabled=ApplicationState.current_step == 0,
            class_name="px-6 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-medium hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all",
        ),
        rx.cond(
            ApplicationState.current_step == 4,
            rx.el.button(
                "Submit Application",
                on_click=ApplicationState.submit_application,
                disabled=~ApplicationState.terms_accepted,
                class_name=rx.cond(
                    ApplicationState.terms_accepted,
                    "px-6 py-2.5 rounded-xl bg-emerald-600 text-white font-medium hover:bg-emerald-700 shadow-lg shadow-emerald-200 transition-all cursor-pointer",
                    "px-6 py-2.5 rounded-xl bg-slate-300 text-slate-500 font-medium cursor-not-allowed transition-all",
                ),
            ),
            rx.el.button(
                "Continue",
                on_click=ApplicationState.next_step,
                class_name="px-6 py-2.5 rounded-xl bg-blue-600 text-white font-medium hover:bg-blue-700 shadow-lg shadow-blue-200 transition-all",
            ),
        ),
        class_name="flex justify-between items-center mt-8 pt-6 border-t border-slate-100",
    )


def application_wizard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            step_indicator(),
            rx.match(
                ApplicationState.current_step,
                (0, personal_info_step()),
                (1, employment_info_step()),
                (2, loan_details_step()),
                (3, documents_step()),
                (4, review_step()),
                personal_info_step(),
            ),
            wizard_actions(),
            class_name="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 max-w-3xl mx-auto",
        ),
        class_name="w-full",
    )