import reflex as rx
from app.states.settings_state import SettingsState


def section_header(title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.h2(title, class_name="text-lg font-bold text-slate-900"),
        rx.el.p(description, class_name="text-sm text-slate-500 mb-6"),
        class_name="mb-4",
    )


def toggle_row(
    label: str, description: str, checked: rx.Var, setting_key: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-slate-900"),
            rx.el.p(description, class_name="text-xs text-slate-500"),
            class_name="flex flex-col",
        ),
        rx.el.button(
            rx.el.div(
                class_name=rx.cond(
                    checked,
                    "w-5 h-5 bg-white rounded-full shadow transform translate-x-5 transition-transform",
                    "w-5 h-5 bg-white rounded-full shadow transform translate-x-1 transition-transform",
                )
            ),
            on_click=lambda: SettingsState.toggle_setting(setting_key),
            class_name=rx.cond(
                checked,
                "w-11 h-6 bg-blue-600 rounded-full transition-colors",
                "w-11 h-6 bg-slate-200 rounded-full transition-colors",
            ),
        ),
        class_name="flex items-center justify-between py-4 border-b border-slate-50 last:border-0",
    )


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Settings", class_name="text-2xl font-bold text-slate-900 mb-2"),
            rx.el.p(
                "Manage your preferences and system configuration.",
                class_name="text-slate-500 mb-8",
            ),
            class_name="max-w-4xl mx-auto",
        ),
        rx.el.div(
            rx.el.div(
                section_header(
                    "Profile Information", "Update your personal details and role."
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.input(
                            default_value=SettingsState.full_name,
                            class_name="w-full px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.input(
                            default_value=SettingsState.email,
                            class_name="w-full px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Role",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Loan Officer", value="Loan Officer"),
                            rx.el.option("Underwriter", value="Underwriter"),
                            rx.el.option("Administrator", value="Administrator"),
                            default_value=SettingsState.role,
                            class_name="w-full px-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Save Changes",
                        on_click=SettingsState.save_profile,
                        class_name="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors",
                    ),
                    class_name="max-w-xl",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 mb-6",
            ),
            rx.el.div(
                section_header("Notifications", "Control how you receive alerts."),
                toggle_row(
                    "Email Notifications",
                    "Receive daily summaries and alerts via email.",
                    SettingsState.email_notifs,
                    "email_notifs",
                ),
                toggle_row(
                    "Push Notifications",
                    "Real-time alerts on your dashboard.",
                    SettingsState.push_notifs,
                    "push_notifs",
                ),
                toggle_row(
                    "Marketing Emails",
                    "Receive updates about new features and products.",
                    SettingsState.marketing_emails,
                    "marketing_emails",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 mb-6",
            ),
            rx.el.div(
                section_header(
                    "System Configuration",
                    "Global settings for loan processing (Admin only).",
                ),
                toggle_row(
                    "Require Manual Review",
                    "Flag all applications for manual underwriting review.",
                    SettingsState.require_manual_review,
                    "require_manual_review",
                ),
                toggle_row(
                    "Maintenance Mode",
                    "Suspend new applications temporarily.",
                    SettingsState.maintenance_mode,
                    "maintenance_mode",
                ),
                rx.el.div(
                    rx.el.label(
                        "Auto-Approval Credit Score Threshold",
                        class_name="block text-sm font-medium text-slate-700 mb-1 mt-4",
                    ),
                    rx.el.input(
                        type="number",
                        default_value=SettingsState.auto_approval_threshold.to_string(),
                        class_name="w-32 px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none",
                    ),
                    class_name="mt-2",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 mb-6",
            ),
            class_name="max-w-4xl mx-auto",
        ),
        class_name="w-full",
    )