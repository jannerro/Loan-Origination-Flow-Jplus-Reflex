import reflex as rx


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", size=20, class_name="text-slate-600"),
                    rx.el.span(
                        class_name="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full ring-2 ring-white"
                    ),
                    class_name="relative p-2 rounded-lg hover:bg-slate-100 transition-colors",
                ),
                rx.el.button(
                    rx.icon("settings", size=20, class_name="text-slate-600"),
                    class_name="p-2 rounded-lg hover:bg-slate-100 transition-colors",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="h-full flex items-center justify-end px-6",
        ),
        class_name="h-16 bg-white border-b border-slate-200 sticky top-0 z-10",
    )