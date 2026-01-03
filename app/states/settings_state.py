import reflex as rx
from typing import TypedDict


class SettingsState(rx.State):
    full_name: str = "Alex Morgan"
    email: str = "alex.morgan@lender.com"
    role: str = "Loan Officer"
    email_notifs: bool = True
    push_notifs: bool = True
    marketing_emails: bool = False
    auto_approval_threshold: int = 750
    max_loan_amount: int = 100000
    require_manual_review: bool = True
    maintenance_mode: bool = False

    @rx.event
    def toggle_setting(self, setting: str):
        current = getattr(self, setting)
        setattr(self, setting, not current)
        rx.toast(f"Updated {setting}")

    @rx.event
    def save_profile(self):
        return rx.toast("Profile settings saved successfully")

    @rx.event
    def save_system_config(self):
        return rx.toast("System configuration updated")