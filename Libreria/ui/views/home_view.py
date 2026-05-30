# ui/views/home_view.py

import tkinter as tk
from ui.styles import COLORS, FONTS, PADDING


class HomeView(tk.Frame):
    """
    
        Vista principal o pantalla de inicio del sistema de librería.

        Esta interfaz muestra información general del sistema mediante
        tarjetas de estadísticas, incluyendo:
        - Cantidad de libros registrados.
        - Cantidad de usuarios registrados.
        - Cantidad de préstamos activos.

        Además, muestra un mensaje de bienvenida y una guía rápida
        para la navegación del usuario.
    
    """

    def __init__(self, parent, service, **kwargs):
        
        """
            Constructor de la vista principal.

            Parámetros:
                parent (tk.Widget): Contenedor padre donde se mostrará la vista.
                service: Servicio que proporciona acceso a los datos
                        de libros, usuarios y préstamos.
                **kwargs: Parámetros adicionales de Tkinter.
        """
        
        super().__init__(parent, bg=COLORS["bg_main"], **kwargs)
        self.service = service
        self._build()

    def _build(self):
        
        """
        Construye la interfaz gráfica de la pantalla principal.

        Se encarga de crear:
        - Encabezado de bienvenida.
        - Tarjetas de estadísticas.
        - Mensaje informativo para el usuario.
        """
        
        # Encabezado principal
        header = tk.Frame(self, bg=COLORS["bg_panel"], pady=32)
        header.pack(fill="x")
        
        # Título principal del sistema

        tk.Label(
            header,
            text="📚  Sistema de Librería",
            font=FONTS["title"],
            bg=COLORS["bg_panel"],
            fg=COLORS["accent"],
        ).pack()
        
        # Descripción breve del sistema

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
        # Mensaje informativo
        
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
        
        """
            Crea una tarjeta de estadística para mostrar información resumida.

            Parámetros:
                parent (tk.Widget): Contenedor donde se agregará la tarjeta.
                icon (str): Icono representativo de la estadística.
                label (str): Texto descriptivo de la estadística.
                value (int): Valor numérico a mostrar.
                color (str): Color utilizado para destacar la información.
        """
        
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

