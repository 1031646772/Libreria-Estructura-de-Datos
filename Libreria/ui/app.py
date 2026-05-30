# ui/app.py
# Ventana principal con barra de navegación lateral.

import tkinter as tk
from ui.styles import COLORS, FONTS
from ui.views.home_view import HomeView
from ui.views.libros_view import LibrosView
from ui.views.usuarios_view import UsuariosView


class App(tk.Tk):
    """Ventana raíz de la aplicación."""

    def __init__(self, service):
        super().__init__()
        self.service = service
        self.title("Sistema de Librería")
        self.geometry("1100x680")
        self.minsize(900, 580)
        self.configure(bg=COLORS["bg_main"])
        self._vista_activa = None
        self._build()

    # ══════════════════════════════════════════════
    # CONSTRUCCIÓN
    # ══════════════════════════════════════════════

    def _build(self):
        # ── Sidebar ──────────────────────────────
        self._sidebar = tk.Frame(self, bg=COLORS["bg_panel"], width=180)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # Logo
        tk.Label(
            self._sidebar,
            text="📚",
            font=("Segoe UI", 28),
            bg=COLORS["bg_panel"],
            fg=COLORS["accent"],
        ).pack(pady=(24, 4))

        tk.Label(
            self._sidebar,
            text="Librería",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"],
            fg=COLORS["text_primary"],
        ).pack()

        tk.Frame(self._sidebar, bg=COLORS["border"], height=1).pack(
            fill="x", padx=16, pady=16
        )

        # Botones de navegación
        self._nav_btns = {}
        nav_items = [
            ("🏠  Inicio",   "home"),
            ("📖  Libros",   "libros"),
            ("👥  Usuarios", "usuarios"),
        ]
        for texto, clave in nav_items:
            btn = tk.Button(
                self._sidebar,
                text=texto,
                font=FONTS["nav"],
                bg=COLORS["bg_panel"],
                fg=COLORS["text_secondary"],
                activebackground=COLORS["bg_hover"],
                activeforeground=COLORS["text_primary"],
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=20, pady=10,
                command=lambda k=clave: self._navegar(k),
            )
            btn.pack(fill="x", pady=1)
            self._nav_btns[clave] = btn

        # Separador inferior
        tk.Frame(self._sidebar, bg=COLORS["bg_main"]).pack(expand=True, fill="y")
        tk.Label(
            self._sidebar,
            text="Listas Lineales\nEstructura de Datos",
            font=("Segoe UI", 8),
            bg=COLORS["bg_panel"],
            fg=COLORS["text_muted"],
            justify="center",
        ).pack(pady=16)

        # ── Área de contenido ────────────────────
        self._content = tk.Frame(self, bg=COLORS["bg_main"])
        self._content.pack(side="left", fill="both", expand=True)

        # ── Crear vistas ─────────────────────────
        self._vistas = {
            "home":     HomeView(self._content, self.service),
            "libros":   LibrosView(self._content, self.service),
            "usuarios": UsuariosView(self._content, self.service),
        }

        # Ir al inicio
        self._navegar("home")

    # ══════════════════════════════════════════════
    # NAVEGACIÓN
    # ══════════════════════════════════════════════

    def _navegar(self, clave: str) -> None:
        # Ocultar vista actual
        if self._vista_activa:
            self._vistas[self._vista_activa].pack_forget()

        # Actualizar estilos de nav
        for k, btn in self._nav_btns.items():
            if k == clave:
                btn.configure(
                    bg=COLORS["accent"],
                    fg="#FFFFFF",
                )
            else:
                btn.configure(
                    bg=COLORS["bg_panel"],
                    fg=COLORS["text_secondary"],
                )

        # Mostrar nueva vista
        self._vista_activa = clave
        vista = self._vistas[clave]
        vista.pack(fill="both", expand=True)

        # Refrescar si la vista lo soporta
        if hasattr(vista, "refrescar"):
            vista.refrescar()

