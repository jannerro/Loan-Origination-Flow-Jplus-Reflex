import reflex as rx
from app.states.application_state import ApplicationState


def form_field(
    label: str,
    placeholder: str,
    value_state: rx.Var,
    field_name: str,
    type_: str = "text",
    error: rx.Var = None,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-700 mb-1"),
        rx.el.input(
            type=type_,
            default_value=value_state,
            placeholder=placeholder,
            on_change=lambda v: ApplicationState.set_field(field_name, v),
            class_name=rx.cond(
                error,
                "w-full px-4 py-2 rounded-lg border border-red-300 focus:ring-2 focus:ring-red-200 focus:border-red-500 outline-none transition-all",
                "w-full px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all",
            ),
        ),
        rx.cond(error, rx.el.p(error, class_name="mt-1 text-xs text-red-500")),
        class_name="mb-4",
    )


def select_field(
    label: str, options: list[str], value_state: rx.Var, field_name: str
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-700 mb-1"),
        rx.el.select(
            rx.foreach(options, lambda opt: rx.el.option(opt, value=opt)),
            value=value_state,
            on_change=lambda v: ApplicationState.set_field(field_name, v),
            class_name="w-full px-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all",
        ),
        class_name="mb-4",
    )


def personal_info_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Personal Information", class_name="text-xl font-bold text-slate-900 mb-6"
        ),
        rx.el.div(
            form_field(
                "First Name",
                "John",
                ApplicationState.first_name,
                "first_name",
                error=ApplicationState.errors["first_name"],
            ),
            form_field(
                "Last Name",
                "Doe",
                ApplicationState.last_name,
                "last_name",
                error=ApplicationState.errors["last_name"],
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        rx.el.div(
            form_field(
                "Email Address",
                "john@example.com",
                ApplicationState.email,
                "email",
                type_="email",
                error=ApplicationState.errors["email"],
            ),
            form_field(
                "Phone Number",
                "(555) 123-4567",
                ApplicationState.phone,
                "phone",
                type_="tel",
                error=ApplicationState.errors["phone"],
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        rx.el.div(
            form_field("Date of Birth", "", ApplicationState.dob, "dob", type_="date"),
            form_field(
                "SSN",
                "XXX-XX-XXXX",
                ApplicationState.ssn,
                "ssn",
                error=ApplicationState.errors["ssn"],
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        form_field(
            "Street Address", "123 Main St", ApplicationState.address, "address"
        ),
        rx.el.div(
            form_field("City", "New York", ApplicationState.city, "city"),
            form_field("State", "NY", ApplicationState.state, "state"),
            form_field("ZIP Code", "10001", ApplicationState.zip_code, "zip_code"),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-500",
    )


def employment_info_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Employment & Income", class_name="text-xl font-bold text-slate-900 mb-6"
        ),
        form_field(
            "Current Employer",
            "Acme Corp",
            ApplicationState.employer,
            "employer",
            error=ApplicationState.errors["employer"],
        ),
        form_field(
            "Job Title",
            "Software Engineer",
            ApplicationState.job_title,
            "job_title",
            error=ApplicationState.errors["job_title"],
        ),
        rx.el.div(
            form_field(
                "Annual Income",
                "85000",
                ApplicationState.annual_income.to_string(),
                "annual_income",
                type_="number",
                error=ApplicationState.errors["annual_income"],
            ),
            select_field(
                "Employment Status",
                ["Full-time", "Part-time", "Self-employed", "Retired"],
                ApplicationState.employment_status,
                "employment_status",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        form_field(
            "Length of Employment",
            "2 years",
            ApplicationState.employment_length,
            "employment_length",
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-500",
    )


def loan_details_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Loan Details", class_name="text-xl font-bold text-slate-900 mb-6"),
        rx.el.div(
            rx.el.label(
                f"Loan Amount: ${ApplicationState.loan_amount.to_string()}",
                class_name="block text-sm font-medium text-slate-700 mb-4",
            ),
            rx.el.input(
                type="range",
                default_value=ApplicationState.loan_amount,
                key=ApplicationState.loan_amount.to_string(),
                min="1000",
                max="100000",
                step="1000",
                on_change=ApplicationState.set_amount.throttle(50),
                class_name="w-full mb-8 accent-blue-600 cursor-pointer",
            ),
            class_name="bg-slate-50 p-6 rounded-xl border border-slate-100 mb-6",
        ),
        rx.el.div(
            select_field(
                "Loan Term",
                ["12 Months", "24 Months", "36 Months", "48 Months", "60 Months"],
                ApplicationState.loan_term.to_string(),
                "loan_term",
            ),
            select_field(
                "Loan Purpose",
                [
                    "Home Improvement",
                    "Debt Consolidation",
                    "Business",
                    "Education",
                    "Other",
                ],
                ApplicationState.loan_purpose,
                "loan_purpose",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        select_field(
            "Loan Type",
            ["Personal Loan", "Business Loan", "Auto Loan"],
            ApplicationState.loan_type,
            "loan_type",
        ),
        rx.cond(
            ApplicationState.errors["loan_amount"],
            rx.el.p(
                ApplicationState.errors["loan_amount"],
                class_name="mt-2 text-sm text-red-500",
            ),
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-500",
    )


def documents_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Document Upload", class_name="text-xl font-bold text-slate-900 mb-6"),
        rx.el.div(
            rx.el.p(
                "Please upload recent pay stubs and a valid ID.",
                class_name="text-slate-500 mb-4",
            ),
            rx.upload.root(
                rx.el.div(
                    rx.icon("cloud_sun", size=48, class_name="text-blue-500 mb-4"),
                    rx.el.p(
                        "Drag and drop files here, or click to select",
                        class_name="text-slate-900 font-medium mb-1",
                    ),
                    rx.el.p(
                        "Supported formats: PDF, JPG, PNG",
                        class_name="text-sm text-slate-500",
                    ),
                    class_name="flex flex-col items-center justify-center p-12 border-2 border-dashed border-blue-200 rounded-xl bg-blue-50 hover:bg-blue-100 transition-colors cursor-pointer",
                ),
                on_drop=ApplicationState.handle_upload(
                    rx.upload_files(upload_id="docs")
                ),
                id="docs",
                border="0px",
            ),
        ),
        rx.el.div(
            rx.el.h3(
                "Uploaded Files",
                class_name="text-sm font-semibold text-slate-900 mb-3 mt-6",
            ),
            rx.cond(
                ApplicationState.uploaded_files.length() > 0,
                rx.foreach(
                    ApplicationState.uploaded_files,
                    lambda file: rx.el.div(
                        rx.el.div(
                            rx.icon("file-text", size=16, class_name="text-blue-600"),
                            rx.el.span(
                                file, class_name="text-sm text-slate-700 truncate"
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.button(
                            rx.icon("x", size=14),
                            on_click=lambda: ApplicationState.remove_file(file),
                            class_name="p-1 text-slate-400 hover:text-red-500 transition-colors",
                        ),
                        class_name="flex items-center justify-between p-3 bg-white border border-slate-100 rounded-lg shadow-sm",
                    ),
                ),
                rx.el.p(
                    "No files uploaded yet", class_name="text-sm text-slate-400 italic"
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-500",
    )


def summary_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-sm text-slate-500"),
        rx.el.span(value, class_name="text-sm font-medium text-slate-900"),
        class_name="flex justify-between py-2 border-b border-slate-100 last:border-0",
    )


def review_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Review & Submit", class_name="text-xl font-bold text-slate-900 mb-6"),
        rx.el.div(
            rx.el.h3(
                "Personal Information",
                class_name="text-sm font-bold text-blue-600 uppercase tracking-wider mb-4",
            ),
            rx.el.div(
                summary_row(
                    "Name",
                    f"{ApplicationState.first_name} {ApplicationState.last_name}",
                ),
                summary_row("Email", ApplicationState.email),
                summary_row("Phone", ApplicationState.phone),
                class_name="bg-slate-50 p-4 rounded-xl mb-6",
            ),
            rx.el.h3(
                "Loan Details",
                class_name="text-sm font-bold text-blue-600 uppercase tracking-wider mb-4",
            ),
            rx.el.div(
                summary_row("Amount", f"${ApplicationState.loan_amount}"),
                summary_row("Term", f"{ApplicationState.loan_term} months"),
                summary_row("Purpose", ApplicationState.loan_purpose),
                class_name="bg-slate-50 p-4 rounded-xl mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=ApplicationState.terms_accepted,
                        on_change=ApplicationState.set_terms_accepted,
                        class_name="mt-1 mr-3 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer",
                    ),
                    rx.el.span(
                        "I certify that the information provided is true and correct to the best of my knowledge.",
                        class_name="text-sm text-slate-600 cursor-pointer",
                    ),
                    class_name="flex items-start cursor-pointer",
                ),
                class_name="p-4 border border-blue-100 bg-blue-50/50 rounded-xl",
            ),
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-500",
    )