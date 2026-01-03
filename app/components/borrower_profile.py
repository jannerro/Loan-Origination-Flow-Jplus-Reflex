import reflex as rx
from app.states.borrower_profile_state import (
    BorrowerProfileState,
    LoanHistoryItem,
    DocumentItem,
    MessageItem,
)
from app.components.recent_apps import status_badge
from app.components.where_tooltip_props_are_defined import TOOLTIP_PROPS


def stat_box(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=20, class_name="text-blue-600"),
            class_name="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center mb-3",
        ),
        rx.el.p(label, class_name="text-sm text-slate-500 mb-1"),
        rx.el.p(value, class_name="text-xl font-bold text-slate-900"),
        class_name="bg-white p-4 rounded-xl border border-slate-100",
    )


def tab_button(text: str, tab_id: str) -> rx.Component:
    return rx.el.button(
        text,
        on_click=lambda: BorrowerProfileState.set_tab(tab_id),
        class_name=rx.cond(
            BorrowerProfileState.active_tab == tab_id,
            "px-4 py-2 text-sm font-medium text-blue-600 border-b-2 border-blue-600 transition-colors",
            "px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-700 transition-colors",
        ),
    )


def overview_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_box(
                "Credit Score",
                f"{BorrowerProfileState.profile['credit_score']}",
                "bar-chart-2",
            ),
            stat_box(
                "Annual Income",
                f"${BorrowerProfileState.profile['annual_income']:,}",
                "dollar-sign",
            ),
            stat_box(
                "Total Loans",
                f"{BorrowerProfileState.profile['total_loans']}",
                "file-text",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("heart-handshake", size=20, class_name="text-pink-600"),
                    class_name="w-10 h-10 rounded-full bg-pink-50 flex items-center justify-center mb-3",
                ),
                rx.el.div(
                    rx.el.p(
                        "Relationship Score", class_name="text-sm text-slate-500 mb-1"
                    ),
                    rx.el.div(
                        rx.el.p(
                            BorrowerProfileState.profile["relationship_score"],
                            class_name="text-xl font-bold text-slate-900",
                        ),
                        rx.el.span(
                            BorrowerProfileState.profile["engagement_level"],
                            class_name="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full ml-2",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="bg-white p-4 rounded-xl border border-slate-100",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Contact & Employment",
                class_name="text-lg font-bold text-slate-900 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Email",
                        class_name="text-xs text-slate-500 uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        BorrowerProfileState.profile["email"],
                        class_name="font-medium text-slate-900",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Phone",
                        class_name="text-xs text-slate-500 uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        BorrowerProfileState.profile["phone"],
                        class_name="font-medium text-slate-900",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Employer",
                        class_name="text-xs text-slate-500 uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        BorrowerProfileState.profile["employer"],
                        class_name="font-medium text-slate-900",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Job Title",
                        class_name="text-xs text-slate-500 uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        BorrowerProfileState.profile["job_title"],
                        class_name="font-medium text-slate-900",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            class_name="bg-white p-8 rounded-2xl shadow-sm border border-slate-100",
        ),
        class_name="animate-in fade-in slide-in-from-bottom-2 duration-300",
    )


def doc_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Verified",
            rx.el.span(
                "Verified",
                class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-600 border border-emerald-100",
            ),
        ),
        (
            "Pending",
            rx.el.span(
                "Pending Review",
                class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-600 border border-amber-100",
            ),
        ),
        (
            "Expired",
            rx.el.span(
                "Expired",
                class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-red-50 text-red-600 border border-red-100",
            ),
        ),
        rx.el.span(
            status,
            class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-slate-50 text-slate-600 border border-slate-100",
        ),
    )


def document_row(doc: DocumentItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(doc["icon"], size=20, class_name="text-blue-600"),
                class_name="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center mr-4",
            ),
            rx.el.div(
                rx.el.p(doc["name"], class_name="font-medium text-slate-900"),
                rx.el.p(doc["type"], class_name="text-xs text-slate-500"),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Uploaded: ", class_name="text-slate-400 text-xs"),
                rx.el.span(
                    doc["date"], class_name="text-slate-600 text-xs font-medium"
                ),
                class_name="mr-6",
            ),
            rx.el.div(
                rx.el.span("Expires: ", class_name="text-slate-400 text-xs"),
                rx.el.span(
                    doc["expiry"], class_name="text-slate-600 text-xs font-medium"
                ),
                class_name="mr-6",
            ),
            doc_badge(doc["status"]),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-4 bg-white border border-slate-100 rounded-xl hover:shadow-sm transition-shadow",
    )


def urgency_option(label: str, value: str, color_class: str) -> rx.Component:
    is_selected = BorrowerProfileState.doc_request_urgency == value
    return rx.el.button(
        label,
        on_click=lambda: BorrowerProfileState.set_doc_request_urgency(value),
        class_name=rx.cond(
            is_selected,
            f"px-3 py-1.5 rounded-lg text-sm font-medium border-2 {color_class}",
            "px-3 py-1.5 rounded-lg text-sm font-medium border border-slate-200 text-slate-600 hover:bg-slate-50",
        ),
    )


def document_request_modal() -> rx.Component:
    return rx.cond(
        BorrowerProfileState.is_doc_request_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 transition-opacity",
                on_click=BorrowerProfileState.close_doc_request_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Request Document",
                        class_name="text-lg font-bold text-slate-900",
                    ),
                    rx.el.button(
                        rx.icon("x", size=20),
                        on_click=BorrowerProfileState.close_doc_request_modal,
                        class_name="text-slate-400 hover:text-slate-600",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Document Type",
                        class_name="block text-sm font-medium text-slate-700 mb-1",
                    ),
                    rx.el.select(
                        rx.foreach(
                            BorrowerProfileState.doc_types,
                            lambda t: rx.el.option(t, value=t),
                        ),
                        value=BorrowerProfileState.doc_request_type,
                        on_change=BorrowerProfileState.set_doc_request_type,
                        class_name="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none text-sm mb-4 bg-white",
                    ),
                    rx.el.label(
                        "Urgency Level",
                        class_name="block text-sm font-medium text-slate-700 mb-2",
                    ),
                    rx.el.div(
                        urgency_option(
                            "Normal",
                            "Normal",
                            "border-blue-500 bg-blue-50 text-blue-700",
                        ),
                        urgency_option(
                            "High Priority",
                            "High",
                            "border-amber-500 bg-amber-50 text-amber-700",
                        ),
                        urgency_option(
                            "Urgent", "Urgent", "border-red-500 bg-red-50 text-red-700"
                        ),
                        class_name="flex gap-3 mb-4",
                    ),
                    rx.el.label(
                        "Note to Borrower",
                        class_name="block text-sm font-medium text-slate-700 mb-1",
                    ),
                    rx.el.textarea(
                        placeholder="Please explain why this document is needed...",
                        on_change=BorrowerProfileState.set_doc_request_note,
                        class_name="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none text-sm min-h-[100px] mb-6",
                        default_value=BorrowerProfileState.doc_request_note,
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=BorrowerProfileState.close_doc_request_modal,
                        class_name="px-4 py-2 text-slate-600 font-medium hover:bg-slate-50 rounded-lg transition-colors mr-2",
                    ),
                    rx.el.button(
                        "Send Request",
                        on_click=BorrowerProfileState.send_doc_request,
                        class_name="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm",
                    ),
                    class_name="flex justify-end pt-4 border-t border-slate-100",
                ),
                class_name="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 p-6 z-50 relative animate-in zoom-in-95 duration-200",
            ),
            class_name="fixed inset-0 flex items-center justify-center z-50 p-4",
        ),
    )


def documents_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Document Checklist", class_name="text-lg font-bold text-slate-900"
            ),
            rx.el.button(
                "Request Document",
                on_click=BorrowerProfileState.open_doc_request_modal,
                class_name="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(BorrowerProfileState.documents, document_row),
            class_name="space-y-3",
        ),
        document_request_modal(),
        class_name="animate-in fade-in slide-in-from-bottom-2 duration-300",
    )


def message_bubble(msg: MessageItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(src=msg["avatar"], class_name="w-8 h-8 rounded-full bg-slate-100"),
            class_name=rx.cond(msg["is_staff"], "order-2 ml-3", "order-1 mr-3"),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    msg["sender"],
                    class_name="text-xs font-bold text-slate-700 mb-1 block",
                ),
                rx.el.p(
                    msg["content"], class_name="text-sm text-slate-800 leading-relaxed"
                ),
                class_name=rx.cond(
                    msg["is_staff"],
                    "bg-blue-50 rounded-2xl rounded-tr-none p-4",
                    "bg-white border border-slate-200 rounded-2xl rounded-tl-none p-4 shadow-sm",
                ),
            ),
            rx.el.span(
                msg["timestamp"],
                class_name="text-[10px] text-slate-400 mt-1 block px-1",
            ),
            class_name=rx.cond(
                msg["is_staff"],
                "order-1 flex flex-col items-end",
                "order-2 flex flex-col items-start",
            ),
        ),
        class_name=rx.cond(
            msg["is_staff"],
            "flex items-start justify-end mb-6",
            "flex items-start mb-6",
        ),
    )


def communications_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(BorrowerProfileState.messages, message_bubble),
            class_name="flex-1 overflow-y-auto max-h-[500px] p-4",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Type a message...",
                on_change=BorrowerProfileState.set_new_message,
                class_name="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all",
                default_value=BorrowerProfileState.new_message,
            ),
            rx.el.button(
                rx.icon("send", size=18, class_name="text-white"),
                on_click=BorrowerProfileState.send_message,
                class_name="ml-2 p-3 bg-blue-600 rounded-xl hover:bg-blue-700 transition-colors shadow-sm",
            ),
            class_name="p-4 border-t border-slate-100 flex items-center",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-300",
    )


def history_row(item: LoanHistoryItem) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(item["id"], class_name="font-mono text-xs text-slate-500"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(item["type"], class_name="text-sm font-medium text-slate-900"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(f"${item['amount']:,}", class_name="text-sm text-slate-600"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(item["date"], class_name="text-sm text-slate-500"),
            class_name="px-6 py-4",
        ),
        rx.el.td(status_badge(item["status"]), class_name="px-6 py-4"),
        class_name="border-b border-slate-50 last:border-0 hover:bg-slate-50",
    )


def history_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Amortization Schedule (Projected)",
                class_name="text-lg font-bold text-slate-900 mb-6",
            ),
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, class_name="opacity-50"
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.x_axis(
                    data_key="month",
                    tick={"fontSize": 12},
                    axis_line=False,
                    tick_line=False,
                ),
                rx.recharts.y_axis(
                    tick={"fontSize": 12}, axis_line=False, tick_line=False
                ),
                rx.recharts.bar(
                    data_key="principal", stack_id="a", fill="#3B82F6", name="Principal"
                ),
                rx.recharts.bar(
                    data_key="interest", stack_id="a", fill="#93C5FD", name="Interest"
                ),
                data=BorrowerProfileState.amortization_schedule,
                width="100%",
                height=300,
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Loan History", class_name="text-lg font-bold text-slate-900 mb-6"
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "ID",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Type",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Amount",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Date",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(rx.foreach(BorrowerProfileState.history, history_row)),
                    class_name="w-full",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden",
            ),
            class_name="mt-8",
        ),
        class_name="animate-in fade-in slide-in-from-bottom-2 duration-300",
    )


def borrower_profile_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=BorrowerProfileState.profile["avatar"],
                class_name="w-24 h-24 rounded-full bg-slate-100 border-4 border-white shadow-lg mb-6",
            ),
            rx.el.div(
                rx.el.h1(
                    BorrowerProfileState.profile["name"],
                    class_name="text-3xl font-bold text-slate-900",
                ),
                rx.el.p(
                    f"ID: {BorrowerProfileState.profile['id']}",
                    class_name="text-slate-500",
                ),
                class_name="mb-8",
            ),
            class_name="flex flex-col items-center text-center max-w-4xl mx-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    tab_button("Overview", "overview"),
                    tab_button("Documents", "documents"),
                    tab_button("Communications", "messages"),
                    tab_button("History & Financials", "history"),
                    class_name="flex gap-2 border-b border-slate-200 mb-8",
                ),
                rx.match(
                    BorrowerProfileState.active_tab,
                    ("overview", overview_view()),
                    ("documents", documents_view()),
                    ("messages", communications_view()),
                    ("history", history_view()),
                    overview_view(),
                ),
                class_name="max-w-4xl mx-auto w-full",
            )
        ),
        class_name="w-full",
    )