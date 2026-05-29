from tkinter import ttk


# ================= THEME CONFIG =================
THEME = {
    "bg": "#1a1a1a",
    "fg": "#ffffff",
    "entry_bg": "#2a2a2a",
    "button_bg": "#2a2a2a",
    "button_hover": "#3a3a3a",
    "grid_bg": "#2a2a2a"
}

FONTS = {
    "title": ("Arial", 20, "bold"),
    "label": ("Arial", 11),
    "button": ("Arial", 10, "bold"),
    "grid": ("Consolas", 11)
}


# ================= ttk STYLE =================
def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Dark.TFrame",
        background=THEME["bg"]
    )

    style.configure(
        "Dark.TLabel",
        background=THEME["bg"],
        foreground=THEME["fg"],
        font=FONTS["label"]
    )

    style.configure(
        "Dark.TButton",
        background=THEME["button_bg"],
        foreground=THEME["fg"],
        font=FONTS["button"]
    )


# ================= STYLE GETTER =================
def get_style():
    return THEME


def get_fonts():
    return FONTS


# ================= WIDGET HELPERS =================
def style_entry(entry):
    entry.configure(
        bg=THEME["entry_bg"],
        fg=THEME["fg"],
        insertbackground=THEME["fg"]
    )


def style_button(btn):
    btn.configure(
        bg=THEME["button_bg"],
        fg=THEME["fg"],
        activebackground=THEME["button_hover"],
        font=FONTS["button"],
        relief="flat",
        cursor="hand2"
    )


def style_label(lbl):
    lbl.configure(
        bg=THEME["bg"],
        fg=THEME["fg"],
        font=FONTS["label"]
    )