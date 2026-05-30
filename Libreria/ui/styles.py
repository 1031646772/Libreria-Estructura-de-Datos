# ui/styles.py
# Paleta de colores y fuentes globales para toda la aplicación.

COLORS = {
    # Fondos
    "bg_main":        "#0F1117",
    "bg_panel":       "#1A1D27",
    "bg_card":        "#22263A",
    "bg_input":       "#2A2E42",
    "bg_hover":       "#2F3348",

    # Acentos
    "accent":         "#6C63FF",
    "accent_hover":   "#8A83FF",
    "accent_success": "#3DD68C",
    "accent_danger":  "#FF6B6B",
    "accent_warn":    "#FFB347",

    # Texto
    "text_primary":   "#EAEDF5",
    "text_secondary": "#8B90A7",
    "text_muted":     "#555A72",

    # Bordes
    "border":         "#2E3248",
    "border_focus":   "#6C63FF",
}

FONTS = {
    "title":    ("Segoe UI", 22, "bold"),
    "subtitle": ("Segoe UI", 13, "bold"),
    "body":     ("Segoe UI", 11),
    "body_sm":  ("Segoe UI", 10),
    "mono":     ("Consolas", 10),
    "btn":      ("Segoe UI", 10, "bold"),
    "nav":      ("Segoe UI", 10, "bold"),
}

PADDING = {
    "section": 24,
    "card":    16,
    "btn":     (8, 20),
}
