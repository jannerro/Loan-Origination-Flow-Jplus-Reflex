import reflex as rx
from app.states.loan_products_state import LoanProductsState, LoanProduct


def product_card(product: LoanProduct) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(product["icon"], size=24, class_name="text-white"),
                class_name=f"w-12 h-12 rounded-xl flex items-center justify-center shadow-md mb-4 {product['color']}",
            ),
            rx.el.h3(
                product["name"], class_name="text-lg font-bold text-slate-900 mb-2"
            ),
            rx.el.p(
                product["description"], class_name="text-sm text-slate-500 mb-6 h-10"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Interest Rate",
                        class_name="text-xs text-slate-400 uppercase tracking-wider font-semibold",
                    ),
                    rx.el.p(
                        f"{product['interest_rate']}%",
                        class_name="text-lg font-bold text-slate-900",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        "Max Amount",
                        class_name="text-xs text-slate-400 uppercase tracking-wider font-semibold",
                    ),
                    rx.el.p(
                        f"${product['max_amount']:,}",
                        class_name="text-lg font-bold text-slate-900",
                    ),
                    class_name="flex flex-col items-end",
                ),
                class_name="flex justify-between items-center pt-4 border-t border-slate-100 mb-4",
            ),
            rx.el.div(
                rx.el.span(
                    f"Terms: {product['term_min']} - {product['term_max']} months",
                    class_name="text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1 rounded-full",
                ),
                class_name="flex mb-6",
            ),
            rx.el.button(
                "Configure Product",
                on_click=lambda: LoanProductsState.open_edit_modal(product),
                class_name="w-full py-2 rounded-lg border border-slate-200 text-slate-600 font-medium hover:bg-slate-50 hover:text-slate-900 transition-colors",
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow",
    )


def form_input(
    label: str, value: rx.Var, on_change: rx.EventHandler, type_: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-700 mb-1"),
        rx.el.input(
            on_change=on_change,
            type=type_,
            class_name="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none text-sm",
            default_value=value,
        ),
        class_name="mb-4",
    )


def product_modal() -> rx.Component:
    return rx.cond(
        LoanProductsState.is_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 transition-opacity",
                on_click=LoanProductsState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            LoanProductsState.current_product_id == "",
                            "Add New Product",
                            "Edit Product",
                        ),
                        class_name="text-lg font-bold text-slate-900",
                    ),
                    rx.el.button(
                        rx.icon("x", size=20),
                        on_click=LoanProductsState.close_modal,
                        class_name="text-slate-400 hover:text-slate-600",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    form_input(
                        "Product Name",
                        LoanProductsState.form_name,
                        LoanProductsState.set_form_name,
                    ),
                    form_input(
                        "Description",
                        LoanProductsState.form_description,
                        LoanProductsState.set_form_description,
                    ),
                    rx.el.div(
                        form_input(
                            "Interest Rate (%)",
                            LoanProductsState.form_interest_rate.to_string(),
                            LoanProductsState.set_form_interest_rate,
                            "number",
                        ),
                        form_input(
                            "Min Amount ($)",
                            LoanProductsState.form_min_amount.to_string(),
                            LoanProductsState.set_form_min_amount,
                            "number",
                        ),
                        form_input(
                            "Max Amount ($)",
                            LoanProductsState.form_max_amount.to_string(),
                            LoanProductsState.set_form_max_amount,
                            "number",
                        ),
                        class_name="grid grid-cols-3 gap-4",
                    ),
                    rx.el.div(
                        form_input(
                            "Min Term (Months)",
                            LoanProductsState.form_term_min.to_string(),
                            LoanProductsState.set_form_term_min,
                            "number",
                        ),
                        form_input(
                            "Max Term (Months)",
                            LoanProductsState.form_term_max.to_string(),
                            LoanProductsState.set_form_term_max,
                            "number",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    class_name="mb-6 overflow-y-auto max-h-[60vh] pr-2",
                ),
                rx.el.div(
                    rx.cond(
                        LoanProductsState.current_product_id != "",
                        rx.el.button(
                            "Delete",
                            on_click=LoanProductsState.delete_product,
                            class_name="px-4 py-2 text-red-600 font-medium hover:bg-red-50 rounded-lg transition-colors mr-auto",
                        ),
                    ),
                    rx.el.button(
                        "Cancel",
                        on_click=LoanProductsState.close_modal,
                        class_name="px-4 py-2 text-slate-600 font-medium hover:bg-slate-50 rounded-lg transition-colors mr-2",
                    ),
                    rx.el.button(
                        "Save Product",
                        on_click=LoanProductsState.save_product,
                        class_name="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm",
                    ),
                    class_name="flex justify-end items-center pt-4 border-t border-slate-100",
                ),
                class_name="bg-white rounded-xl shadow-xl w-full max-w-2xl mx-4 p-6 z-50 relative animate-in zoom-in-95 duration-200",
            ),
            class_name="fixed inset-0 flex items-center justify-center z-50 p-4",
        ),
    )


def products_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Loan Products", class_name="text-2xl font-bold text-slate-900"),
            rx.el.button(
                rx.el.div(
                    rx.icon("plus", size=18, class_name="mr-2"),
                    "Add New Product",
                    class_name="flex items-center",
                ),
                on_click=LoanProductsState.open_add_modal,
                class_name="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm shadow-blue-200",
            ),
            class_name="flex justify-between items-center mb-8",
        ),
        rx.el.div(
            rx.foreach(LoanProductsState.products, product_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        product_modal(),
    )