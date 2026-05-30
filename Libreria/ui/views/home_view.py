# ui/views/home_view.py

import tkinter as tk
from ui.styles import COLORS, FONTS, PADDING


class HomeView(tk.Frame):
    """Pantalla de bienvenida con estadísticas rápidas."""

    def __init__(self, parent, service, **kwargs):
        super().__init__(parent, bg=COLORS["bg_main"], **kwargs)
        self.service = service
        self._build()

    def _build(self):
        # ── Encabezado ──────────────────────────────
        header = tk.Frame(self, bg=COLORS["bg_panel"], pady=32)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📚  Sistema de Librería",
            font=FONTS["title"],
            bg=COLORS["bg_panel"],
            fg=COLORS["accent"],
        ).pack()

        tk.Label(
            header,
            text="Gestión de libros, usuarios y préstamos con Listas Lineales",
            font=FONTS["body"],
            bg=COLORS["bg_panel"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(4, 0))

        # ── Tarjetas de estadísticas ─────────────────
        cards_frame = tk.Frame(self, bg=COLORS["bg_main"])
        cards_frame.pack(pady=32, padx=PADDING["section"])

        self._stat_card(cards_frame, "📖", "Libros\nRegistrados",
                        len(self.service.listar_libros()), COLORS["accent"])
        self._stat_card(cards_frame, "👤", "Usuarios\nRegistrados",
                        len(self.service.listar_usuarios()), COLORS["accent_success"])
        self._stat_card(cards_frame, "🔖", "Préstamos\nActivos",
                        len(self.service.listar_prestamos()), COLORS["accent_warn"])

        # ── Tip ─────────────────────────────────────
        tip = tk.Frame(self, bg=COLORS["bg_card"], pady=16, padx=24)
        tip.pack(fill="x", padx=PADDING["section"], pady=(0, 20))

        tk.Label(
            tip,
            text="💡  Usa el menú lateral para navegar entre las secciones.",
            font=FONTS["body"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            justify="left",
        ).pack(anchor="w")

    def _stat_card(self, parent, icon, label, value, color):
        card = tk.Frame(
            parent,
            bg=COLORS["bg_card"],
            padx=28, pady=20,
            relief="flat",
        )
        card.pack(side="left", expand=True, fill="both", padx=12)

        tk.Label(card, text=icon, font=("Segoe UI", 26),
                 bg=COLORS["bg_card"], fg=color).pack()
        tk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"),
                 bg=COLORS["bg_card"], fg=color).pack()
        tk.Label(card, text=label, font=FONTS["body_sm"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 justify="center").pack()

