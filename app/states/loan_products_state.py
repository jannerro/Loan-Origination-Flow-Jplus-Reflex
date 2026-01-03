import reflex as rx
from typing import TypedDict


class LoanProduct(TypedDict):
    id: str
    name: str
    description: str
    min_amount: int
    max_amount: int
    interest_rate: float
    term_min: int
    term_max: int
    icon: str
    color: str


class LoanProductsState(rx.State):
    products: list[LoanProduct] = [
        {
            "id": "LP-001",
            "name": "Personal Standard",
            "description": "Unsecured personal loan for general purposes.",
            "min_amount": 1000,
            "max_amount": 50000,
            "interest_rate": 8.5,
            "term_min": 12,
            "term_max": 60,
            "icon": "user",
            "color": "bg-blue-500",
        },
        {
            "id": "LP-002",
            "name": "Home Improvement",
            "description": "Funds specifically for home renovation projects.",
            "min_amount": 5000,
            "max_amount": 100000,
            "interest_rate": 6.2,
            "term_min": 24,
            "term_max": 120,
            "icon": "home",
            "color": "bg-emerald-500",
        },
        {
            "id": "LP-003",
            "name": "Debt Consolidation",
            "description": "Combine multiple debts into a single payment.",
            "min_amount": 2500,
            "max_amount": 75000,
            "interest_rate": 7.8,
            "term_min": 12,
            "term_max": 48,
            "icon": "credit-card",
            "color": "bg-violet-500",
        },
        {
            "id": "LP-004",
            "name": "Small Business Starter",
            "description": "Capital for new business ventures.",
            "min_amount": 10000,
            "max_amount": 250000,
            "interest_rate": 5.5,
            "term_min": 36,
            "term_max": 84,
            "icon": "briefcase",
            "color": "bg-amber-500",
        },
    ]
    is_modal_open: bool = False
    current_product_id: str = ""
    form_name: str = ""
    form_description: str = ""
    form_min_amount: int = 0
    form_max_amount: int = 0
    form_interest_rate: float = 0.0
    form_term_min: int = 0
    form_term_max: int = 0
    form_icon: str = "user"
    form_color: str = "bg-blue-500"

    @rx.event
    def open_add_modal(self):
        self.current_product_id = ""
        self.form_name = ""
        self.form_description = ""
        self.form_min_amount = 5000
        self.form_max_amount = 50000
        self.form_interest_rate = 5.0
        self.form_term_min = 12
        self.form_term_max = 60
        self.form_icon = "briefcase"
        self.form_color = "bg-blue-500"
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, product: LoanProduct):
        self.current_product_id = product["id"]
        self.form_name = product["name"]
        self.form_description = product["description"]
        self.form_min_amount = product["min_amount"]
        self.form_max_amount = product["max_amount"]
        self.form_interest_rate = product["interest_rate"]
        self.form_term_min = product["term_min"]
        self.form_term_max = product["term_max"]
        self.form_icon = product["icon"]
        self.form_color = product["color"]
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def save_product(self):
        new_product = {
            "id": self.current_product_id or f"LP-{len(self.products) + 1:03d}",
            "name": self.form_name,
            "description": self.form_description,
            "min_amount": self.form_min_amount,
            "max_amount": self.form_max_amount,
            "interest_rate": self.form_interest_rate,
            "term_min": self.form_term_min,
            "term_max": self.form_term_max,
            "icon": self.form_icon,
            "color": self.form_color,
        }
        if self.current_product_id:
            self.products = [
                new_product if p["id"] == self.current_product_id else p
                for p in self.products
            ]
            rx.toast("Product updated successfully")
        else:
            self.products.append(new_product)
            rx.toast("Product created successfully")
        self.is_modal_open = False

    @rx.event
    def delete_product(self):
        if self.current_product_id:
            self.products = [
                p for p in self.products if p["id"] != self.current_product_id
            ]
            rx.toast("Product deleted")
            self.is_modal_open = False

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_min_amount(self, value: str):
        if value:
            self.form_min_amount = int(value)

    @rx.event
    def set_form_max_amount(self, value: str):
        if value:
            self.form_max_amount = int(value)

    @rx.event
    def set_form_interest_rate(self, value: str):
        if value:
            self.form_interest_rate = float(value)

    @rx.event
    def set_form_term_min(self, value: str):
        if value:
            self.form_term_min = int(value)

    @rx.event
    def set_form_term_max(self, value: str):
        if value:
            self.form_term_max = int(value)