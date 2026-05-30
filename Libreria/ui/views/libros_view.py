# ui/views/libros_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import COLORS, FONTS, PADDING


class LibrosView(tk.Frame):
    """
        Vista encargada de la gestión de libros del sistema.

        Funcionalidades principales:
        - Registrar nuevos libros.
        - Validar la información ingresada por el usuario.
        - Mostrar el listado de libros registrados.
        - Actualizar automáticamente la tabla cuando se agrega un libro.

    """

    def __init__(self, parent, service, **kwargs):
        
        """
            Inicializa la vista de libros.

            Parámetros:
                parent (tk.Widget): Contenedor padre.
                service: Servicio encargado de la lógica de negocio.
                **kwargs: Parámetros adicionales de Tkinter.
        """
        
        super().__init__(parent, bg=COLORS["bg_main"], **kwargs)
        self.service = service
        self._build()

    # ══════════════════════════════════════════════
    # CONSTRUCCIÓN DE LA UI
    # ══════════════════════════════════════════════

    def _build(self):
        
        """
            Construye todos los componentes visuales de la vista.

            Se divide en dos secciones principales:
            - Formulario para registrar libros.
            - Tabla para visualizar los libros almacenados.
        """
        self._build_form()
        self._build_tabla()

    # ── Formulario ──────────────────────────────────
    def _build_form(self):
        
        """
            Crea el formulario para el registro de libros.

            El formulario contiene los siguientes campos:
            - ISBN
            - Título
            - Autor
            - Año de publicación
            - Cantidad disponible

            También incluye botones para:
            - Registrar un libro.
            - Limpiar los campos del formulario.

            Finalmente muestra mensajes de estado para informar
            al usuario sobre el resultado de las operaciones.
        """
        
        form_frame = tk.LabelFrame(
            self,
            text="  ➕  Ingresar Nuevo Libro  ",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"],
            fg=COLORS["accent"],
            bd=0,
            labelanchor="nw",
            padx=PADDING["card"],
            pady=PADDING["card"],
        )
        form_frame.pack(fill="x", padx=PADDING["section"], pady=(20, 10))

        # Campos del formulario
        campos = [
            ("ISBN *",    "isbn"),
            ("Título *",  "titulo"),
            ("Autor *",   "autor"),
            ("Año",       "anio"),
            ("Cantidad",  "cantidad"),
        ]

        self._entries = {}
        grid = tk.Frame(form_frame, bg=COLORS["bg_panel"])
        grid.pack(fill="x")

        for col, (etiqueta, clave) in enumerate(campos):
            sub = tk.Frame(grid, bg=COLORS["bg_panel"])
            sub.grid(row=0, column=col, padx=8, sticky="ew")
            grid.columnconfigure(col, weight=1)

            tk.Label(sub, text=etiqueta, font=FONTS["body_sm"],
                     bg=COLORS["bg_panel"], fg=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")

            entry = tk.Entry(
                sub,
                font=FONTS["body"],
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"],
                insertbackground=COLORS["accent"],
                relief="flat",
                bd=6,
            )
            entry.pack(fill="x", ipady=4)
            self._entries[clave] = entry

        # Valores por defecto
        self._entries["anio"].insert(0, "2024")
        self._entries["cantidad"].insert(0, "1")

        # Botones
        btn_frame = tk.Frame(form_frame, bg=COLORS["bg_panel"])
        btn_frame.pack(fill="x", pady=(12, 0))

        self._btn_registrar = tk.Button(
            btn_frame,
            text="✔  Registrar Libro",
            font=FONTS["btn"],
            bg=COLORS["accent"],
            fg="#FFFFFF",
            activebackground=COLORS["accent_hover"],
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=20, pady=8,
            command=self._registrar_libro,
        )
        self._btn_registrar.pack(side="left")

        tk.Button(
            btn_frame,
            text="✖  Limpiar",
            font=FONTS["btn"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            cursor="hand2",
            padx=20, pady=8,
            command=self._limpiar,
        ).pack(side="left", padx=(8, 0))

        # Mensaje de estado
        self._lbl_estado = tk.Label(
            btn_frame, text="", font=FONTS["body_sm"],
            bg=COLORS["bg_panel"], fg=COLORS["accent_success"],
        )
        self._lbl_estado.pack(side="left", padx=16)

    # ── Tabla ────────────────────────────────────────
    def _build_tabla(self):
        
        """
            Construye la tabla donde se muestran los libros registrados.

            Utiliza el componente Treeview de ttk para presentar
            la información en formato tabular.

            Columnas mostradas:
            - ISBN
            - Título
            - Autor
            - Año
            - Cantidad disponible
            - Cantidad total
        """
        lista_frame = tk.LabelFrame(
            self,
            text="  📋  Libros Registrados  ",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"],
            fg=COLORS["accent"],
            bd=0,
            labelanchor="nw",
            padx=PADDING["card"],
            pady=PADDING["card"],
        )
        lista_frame.pack(fill="both", expand=True,
                         padx=PADDING["section"], pady=(0, 20))

        # Estilo ttk para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Lib.Treeview",
            background=COLORS["bg_card"],
            foreground=COLORS["text_primary"],
            fieldbackground=COLORS["bg_card"],
            rowheight=28,
            font=FONTS["body_sm"],
        )
        style.configure(
            "Lib.Treeview.Heading",
            background=COLORS["bg_input"],
            foreground=COLORS["accent"],
            font=FONTS["btn"],
            relief="flat",
        )
        style.map("Lib.Treeview",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", "#FFFFFF")])

        columnas = ("isbn", "titulo", "autor", "anio", "disponibles", "total")
        self._tree = ttk.Treeview(
            lista_frame,
            columns=columnas,
            show="headings",
            style="Lib.Treeview",
            selectmode="browse",
        )

        encabezados = {
            "isbn":        ("ISBN",         120),
            "titulo":      ("Título",       220),
            "autor":       ("Autor",        160),
            "anio":        ("Año",           60),
            "disponibles": ("Disponibles",   90),
            "total":       ("Total",          60),
        }
        for col, (texto, ancho) in encabezados.items():
            self._tree.heading(col, text=texto)
            self._tree.column(col, width=ancho, anchor="center" if col != "titulo" else "w")

        scroll = ttk.Scrollbar(lista_frame, orient="vertical",
                               command=self._tree.yview)
        self._tree.configure(yscrollcommand=scroll.set)

        self._tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._actualizar_tabla()

    # ══════════════════════════════════════════════
    # LÓGICA DE LA VISTA (conecta con el servicio)
    # ══════════════════════════════════════════════

    def _registrar_libro(self):
        
        """
            Obtiene los datos ingresados en el formulario,
            valida los campos numéricos y envía la información
            al servicio para registrar el libro.

            Si el registro es exitoso:
            - Limpia el formulario.
            - Actualiza la tabla de libros.

            Si ocurre un error:
            - Muestra un mensaje descriptivo al usuario.
        """
        datos = {k: e.get().strip() for k, e in self._entries.items()}

        try:
            anio = int(datos["anio"]) if datos["anio"] else 2024
            cantidad = int(datos["cantidad"]) if datos["cantidad"] else 1
        except ValueError:
            self._mostrar_estado("⚠ Año y cantidad deben ser números.", error=True)
            return

        ok, msg = self.service.ingresar_libro(
            datos["isbn"], datos["titulo"], datos["autor"], anio, cantidad
        )
        self._mostrar_estado(msg, error=not ok)
        if ok:
            self._limpiar()
            self._actualizar_tabla()

    def _limpiar(self):
        
        """
            Restablece los campos del formulario a sus
            valores iniciales y elimina cualquier mensaje
            de estado mostrado anteriormente.
        """
        
        for entry in self._entries.values():
            entry.delete(0, "end")
        self._entries["anio"].insert(0, "2024")
        self._entries["cantidad"].insert(0, "1")
        self._lbl_estado.config(text="")

    def _mostrar_estado(self, msg: str, error: bool = False):
        
        """
            Muestra mensajes informativos al usuario.

            Parámetros:
                msg (str): Texto que se mostrará.
                error (bool): Indica si el mensaje
                            corresponde a un error.
        """
        color = COLORS["accent_danger"] if error else COLORS["accent_success"]
        self._lbl_estado.config(text=msg, fg=color)

    def _actualizar_tabla(self):
        
        """
            Actualiza el contenido de la tabla de libros.

            Primero elimina todos los registros existentes
            y posteriormente consulta nuevamente la lista
            de libros desde el servicio.

            Los libros sin ejemplares disponibles son
            resaltados con un color de advertencia para
            facilitar su identificación.
        """
        for item in self._tree.get_children():
            self._tree.delete(item)
        for libro in self.service.listar_libros():
            tag = "agotado" if libro.disponibles == 0 else ""
            self._tree.insert("", "end", values=(
                libro.isbn, libro.titulo, libro.autor,
                libro.anio, libro.disponibles, libro.cantidad,
            ), tags=(tag,))
        self._tree.tag_configure("agotado", foreground=COLORS["accent_danger"])

    def refrescar(self):
        """Llamado desde la app principal al navegar a esta vista."""
        self._actualizar_tabla()

