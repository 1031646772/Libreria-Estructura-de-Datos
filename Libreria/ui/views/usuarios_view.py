# ui/views/usuarios_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import COLORS, FONTS, PADDING


class UsuariosView(tk.Frame):
    
    """
        Vista encargada de la gestión de usuarios y préstamos.

        Funcionalidades principales:
        - Registrar nuevos usuarios.
        - Visualizar los usuarios registrados.
        - Realizar préstamos de libros.
        - Registrar devoluciones de libros.
        - Mostrar el listado de préstamos activos.

    """

    def __init__(self, parent, service, **kwargs):
        
        """
            Inicializa la vista de usuarios.

            Parámetros:
                parent (tk.Widget): Contenedor padre.
                service: Servicio que contiene la lógica de negocio.
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
            Construye la interfaz gráfica principal.

            La vista se divide en dos columnas:

            Columna izquierda:
            - Formulario de registro de usuarios.
            - Tabla de usuarios registrados.

            Columna derecha:
            - Formulario de préstamos y devoluciones.
            - Tabla de préstamos activos.
        """
        
        # Contenedor de dos columnas
        wrapper = tk.Frame(self, bg=COLORS["bg_main"])
        wrapper.pack(fill="both", expand=True,
                     padx=PADDING["section"], pady=16)
        wrapper.columnconfigure(0, weight=1)
        wrapper.columnconfigure(1, weight=1)

        left = tk.Frame(wrapper, bg=COLORS["bg_main"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        right = tk.Frame(wrapper, bg=COLORS["bg_main"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self._build_form_usuario(left)
        self._build_tabla_usuarios(left)
        self._build_form_prestamo(right)
        self._build_tabla_prestamos(right)

    # ── Formulario de usuario ────────────────────
    def _build_form_usuario(self, parent):
        
        """
            Construye el formulario para registrar usuarios.

            Permite capturar:
            - Cédula.
            - Nombre.
            - Correo electrónico.

            También incorpora controles para registrar
            y limpiar la información ingresada.
        """
        frame = tk.LabelFrame(
            parent, text="  👤  Ingresar Usuario  ",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"], fg=COLORS["accent_success"],
            bd=0, labelanchor="nw",
            padx=PADDING["card"], pady=PADDING["card"],
        )
        frame.pack(fill="x", pady=(0, 10))
        
        # Campos requeridos para el registro
        # de nuevos usuarios.

        campos = [("Cédula *", "cedula"), ("Nombre *", "nombre"), ("Email *", "email")]
        self._u_entries = {}

        # Campos requeridos para el registro
        # de nuevos usuarios.

        for etiqueta, clave in campos:
            tk.Label(frame, text=etiqueta, font=FONTS["body_sm"],
                     bg=COLORS["bg_panel"], fg=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
            entry = tk.Entry(
                frame, font=FONTS["body"],
                bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                insertbackground=COLORS["accent_success"],
                relief="flat", bd=6,
            )
            entry.pack(fill="x", ipady=4, pady=(0, 6))
            self._u_entries[clave] = entry
            

        btn_f = tk.Frame(frame, bg=COLORS["bg_panel"])
        btn_f.pack(fill="x", pady=(4, 0))
        
        # Ejecuta el proceso de registro
        # de un nuevo usuario.

        tk.Button(
            btn_f, text="✔  Registrar",
            font=FONTS["btn"],
            bg=COLORS["accent_success"], fg="#000000",
            activebackground="#5DE8A4",
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=self._registrar_usuario,
        ).pack(side="left")

        # Elimina el contenido de todos los campos
        # del formulario.

        tk.Button(
            btn_f, text="✖  Limpiar",
            font=FONTS["btn"],
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
            activebackground=COLORS["bg_hover"],
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=lambda: [e.delete(0, "end") for e in self._u_entries.values()],
        ).pack(side="left", padx=(6, 0))

        self._lbl_u_estado = tk.Label(btn_f, text="", font=FONTS["body_sm"],
                                       bg=COLORS["bg_panel"],
                                       fg=COLORS["accent_success"])
        self._lbl_u_estado.pack(side="left", padx=10)

    # ── Tabla de usuarios ────────────────────────
    def _build_tabla_usuarios(self, parent):
        
        """
            Construye la tabla que muestra los usuarios registrados.

            Información mostrada:
            - Cédula.
            - Nombre.
            - Correo electrónico.
            - Cantidad de préstamos activos.
        """
        frame = tk.LabelFrame(
            parent, text="  📋  Usuarios Registrados  ",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"], fg=COLORS["accent_success"],
            bd=0, labelanchor="nw",
            padx=PADDING["card"], pady=PADDING["card"],
        )
        frame.pack(fill="both", expand=True, pady=(0, 10))

        style = ttk.Style()
        style.configure("Usr.Treeview",
                        background=COLORS["bg_card"],
                        foreground=COLORS["text_primary"],
                        fieldbackground=COLORS["bg_card"],
                        rowheight=26, font=FONTS["body_sm"])
        style.configure("Usr.Treeview.Heading",
                        background=COLORS["bg_input"],
                        foreground=COLORS["accent_success"],
                        font=FONTS["btn"], relief="flat")
        style.map("Usr.Treeview",
                  background=[("selected", COLORS["accent_success"])],
                  foreground=[("selected", "#000000")])

        cols = ("cedula", "nombre", "email", "prestamos")
        self._tree_usr = ttk.Treeview(frame, columns=cols,
                                       show="headings", style="Usr.Treeview",
                                       height=6)
        headers = {"cedula": ("Cédula", 80), "nombre": ("Nombre", 140),
                   "email": ("Email", 160), "prestamos": ("Préstamos", 70)}
        for col, (txt, w) in headers.items():
            self._tree_usr.heading(col, text=txt)
            self._tree_usr.column(col, width=w, anchor="center")

        sc = ttk.Scrollbar(frame, orient="vertical",
                           command=self._tree_usr.yview)
        self._tree_usr.configure(yscrollcommand=sc.set)
        self._tree_usr.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        self._actualizar_tabla_usuarios()

    # ── Formulario de préstamo ───────────────────
    def _build_form_prestamo(self, parent):
        
        """
            Construye el formulario para gestionar
            préstamos y devoluciones de libros.

            Datos requeridos:
            - Cédula del usuario.
            - ISBN del libro.

            Permite registrar préstamos y devoluciones.
        """
        
        frame = tk.LabelFrame(
            parent, text="  🔖  Prestar / Devolver Libro  ",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"], fg=COLORS["accent_warn"],
            bd=0, labelanchor="nw",
            padx=PADDING["card"], pady=PADDING["card"],
        )
        frame.pack(fill="x", pady=(0, 10))

        campos = [("Cédula del usuario *", "p_cedula"),
                  ("ISBN del libro *",      "p_isbn")]
        self._p_entries = {}

        for etiqueta, clave in campos:
            tk.Label(frame, text=etiqueta, font=FONTS["body_sm"],
                     bg=COLORS["bg_panel"], fg=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
            entry = tk.Entry(
                frame, font=FONTS["body"],
                bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                insertbackground=COLORS["accent_warn"],
                relief="flat", bd=6,
            )
            entry.pack(fill="x", ipady=4, pady=(0, 6))
            self._p_entries[clave] = entry

        btn_f = tk.Frame(frame, bg=COLORS["bg_panel"])
        btn_f.pack(fill="x", pady=(4, 0))

        tk.Button(
            btn_f, text="📤  Prestar",
            font=FONTS["btn"],
            bg=COLORS["accent_warn"], fg="#000000",
            activebackground="#FFC870",
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=self._prestar,
        ).pack(side="left")

        tk.Button(
            btn_f, text="📥  Devolver",
            font=FONTS["btn"],
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
            activebackground=COLORS["bg_hover"],
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=self._devolver,
        ).pack(side="left", padx=(6, 0))

        self._lbl_p_estado = tk.Label(frame, text="", font=FONTS["body_sm"],
                                       bg=COLORS["bg_panel"],
                                       fg=COLORS["accent_warn"],
                                       wraplength=280, justify="left")
        self._lbl_p_estado.pack(fill="x", pady=(6, 0))

    # ── Tabla de préstamos ───────────────────────
    def _build_tabla_prestamos(self, parent):
        
        """
            Construye la tabla de préstamos activos.

            Información mostrada:
            - Cédula del usuario.
            - Nombre del usuario.
            - ISBN del libro.
            - Título del libro.
        """
        frame = tk.LabelFrame(
            parent, text="  📋  Préstamos Activos  ",
            font=FONTS["subtitle"],
            bg=COLORS["bg_panel"], fg=COLORS["accent_warn"],
            bd=0, labelanchor="nw",
            padx=PADDING["card"], pady=PADDING["card"],
        )
        frame.pack(fill="both", expand=True, pady=(0, 10))

        style = ttk.Style()
        style.configure("Pre.Treeview",
                        background=COLORS["bg_card"],
                        foreground=COLORS["text_primary"],
                        fieldbackground=COLORS["bg_card"],
                        rowheight=26, font=FONTS["body_sm"])
        style.configure("Pre.Treeview.Heading",
                        background=COLORS["bg_input"],
                        foreground=COLORS["accent_warn"],
                        font=FONTS["btn"], relief="flat")
        style.map("Pre.Treeview",
                  background=[("selected", COLORS["accent_warn"])],
                  foreground=[("selected", "#000000")])

        cols = ("usuario", "nombre", "isbn", "titulo")
        self._tree_pre = ttk.Treeview(frame, columns=cols,
                                       show="headings", style="Pre.Treeview",
                                       height=8)
        headers = {"usuario": ("Cédula", 80), "nombre": ("Usuario", 140),
                   "isbn": ("ISBN", 110), "titulo": ("Libro", 160)}
        for col, (txt, w) in headers.items():
            self._tree_pre.heading(col, text=txt)
            self._tree_pre.column(col, width=w, anchor="center" if col != "titulo" else "w")

        sc = ttk.Scrollbar(frame, orient="vertical",
                           command=self._tree_pre.yview)
        self._tree_pre.configure(yscrollcommand=sc.set)
        self._tree_pre.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        self._actualizar_tabla_prestamos()

    # ══════════════════════════════════════════════
    # LÓGICA DE LA VISTA
    # ══════════════════════════════════════════════

    def _registrar_usuario(self):
        
        """
            Obtiene los datos ingresados por el usuario
            y solicita al servicio registrar un nuevo usuario.

            Si la operación es exitosa:
            - Limpia los campos.
            - Actualiza la tabla de usuarios.

            En caso contrario:
            - Muestra un mensaje de error.
        """
        cedula = self._u_entries["cedula"].get().strip()
        nombre = self._u_entries["nombre"].get().strip()
        email = self._u_entries["email"].get().strip()

        ok, msg = self.service.ingresar_usuario(cedula, nombre, email)
        color = COLORS["accent_success"] if ok else COLORS["accent_danger"]
        self._lbl_u_estado.config(text=msg, fg=color)

        if ok:
            for e in self._u_entries.values():
                e.delete(0, "end")
            self._actualizar_tabla_usuarios()

    def _prestar(self):
        
        """
            Gestiona el préstamo de un libro.

            Obtiene la información ingresada,
            solicita la operación al servicio y
            actualiza las tablas correspondientes.
        """
        cedula = self._p_entries["p_cedula"].get().strip()
        isbn = self._p_entries["p_isbn"].get().strip()
        ok, msg = self.service.prestar_libro(cedula, isbn)
        color = COLORS["accent_success"] if ok else COLORS["accent_danger"]
        self._lbl_p_estado.config(text=msg, fg=color)
        if ok:
            self._actualizar_tabla_prestamos()
            self._actualizar_tabla_usuarios()

    def _devolver(self):
        
        """
            Gestiona la devolución de un libro.

            Actualiza la disponibilidad del libro
            y refresca la información visualizada.
        """
        cedula = self._p_entries["p_cedula"].get().strip()
        isbn = self._p_entries["p_isbn"].get().strip()
        ok, msg = self.service.devolver_libro(cedula, isbn)
        color = COLORS["accent_success"] if ok else COLORS["accent_danger"]
        self._lbl_p_estado.config(text=msg, fg=color)
        if ok:
            self._actualizar_tabla_prestamos()
            self._actualizar_tabla_usuarios()

    def _actualizar_tabla_usuarios(self):
        
        """
            Actualiza la información mostrada
            en la tabla de usuarios registrados.
        """
        for item in self._tree_usr.get_children():
            self._tree_usr.delete(item)
        for u in self.service.listar_usuarios():
            self._tree_usr.insert("", "end", values=(
                u.cedula, u.nombre, u.email, len(u.libros_prestados)
            ))

    def _actualizar_tabla_prestamos(self):
        
        """
            Actualiza la tabla de préstamos activos.

            Consulta la información de usuarios y libros
            para mostrar datos descriptivos junto con
            cada préstamo registrado.
        """
        for item in self._tree_pre.get_children():
            self._tree_pre.delete(item)
        for p in self.service.listar_prestamos():
            usuario = self.service.buscar_usuario(p["cedula"])
            libro = self.service.buscar_libro(p["isbn"])
            nombre = usuario.nombre if usuario else "?"
            titulo = libro.titulo if libro else "?"
            self._tree_pre.insert("", "end", values=(
                p["cedula"], nombre, p["isbn"], titulo
            ))

    def refrescar(self):
        """
            Método invocado por la aplicación principal
            cuando el usuario navega hacia esta vista.

            Garantiza que la información mostrada
            se encuentre actualizada.
        """
        self._actualizar_tabla_usuarios()
        self._actualizar_tabla_prestamos()
