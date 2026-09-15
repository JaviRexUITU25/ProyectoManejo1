import os
import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox

from i18n import t

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, config: dict, on_guardar):
        """
        Master: ventana principal
        config: dict con la configuracion actual
        on_guardar: nuevo_config: dict, es la que usa la ventana principal
        para aplicar nuevos cambios
        """
        super().__init__(master)
        self.config_actual = config.copy()
        self.on_guardar = on_guardar
        self.idioma = config.get("idioma", "es-ES")

        self.title(t(self.idoma, "settings_tittle"))
        self.geometry("480x660")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.color_menu_actual = self.config_actual.get("color_menu", "#2C3E50")
        self._color_letra_actual = self.config_actual.get("color_letra", "#FFFFFF")
        self._foto_actual = self.config_actual.get("foto_perfil", "")

        self._construir_ui()
def _construir_ui(self):
    pad_titulo = {"padx": 22, "pady": (14, 4)}

    contenedor = ctk.CTkScrollableFrame(self, corner_radius=12)
    contenedor.pack(fill="both", expand=True, padx=16, pady=(16,8))

    fuente_label = ctk.CTkFont(size=13, weight="bold")
    #Nombre de usuario
    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_nombre"),
                 anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    self.entry_nombre = ctk.CTkEntry(contenedor, placeholder_text="Usuario")
    self.entry_nombre.insert(0, self.config_actual.get("Nombre de usuario", ""))
    self.entry_nombre.pack(fill="x", padx=22, pady=(0,8))

    # Interfaz
    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_tema"),
                 anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    self.tema_var = ctk.StringVar(value=self.config_actual.get("tema_interfaz", "claro"))
    frame_tema = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_tema.pack(fill="x", padx=22, pady=(0,8))
    ctk.CTkRadioButton(frame_tema, text="Claro / Light", variable=self.tema_var,
                       value="claro").pack(side="left", padx=(0,24))
    ctk.CTkRadioButton(frame_tema, text="Oscuro / Dark", variable=self.tema_var,
                       value="oscuro").pack(side="left")

    # Idioma

    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_idioma"),
                    anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    self.idioma_var = ctk.StringVar(value=self.config_actual.get("idioma", "es-ES"))
    self.combo_idioma = ctk.CTkComboBox(contenedor, values=["es-ES", "en-US"],
                                            variable=self.idioma_var)
    self.combo_idioma.pack(fill="x", padx=22, pady=(0, 8))

    # Tmaaño de la fuente
    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_fuente"),
                 anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    frame_fuente = ctk.CTkEntry(frame_fuente, justify="center")
    self.entry_fuente.insert(0,str(self.config_actual.get("tamaño_fuente0", 12)))
    self.entry_fuente.pack(side="left", fill="x", expand=True, padx=6)
    ctk.CTkButton(frame_fuente, text="+", width=32,
                  command=lambda: self._ajustar_fuente(1)).pack(side="left")

    # Color del menu
    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_color_menu"),
                         anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    frame_cm = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_cm.pack(fill="x", padx=22, pady=(0, 8))
    self.preview_menu = ctk.CTkLabel(frame_cm, text="", width=44, height=26,
                                        corner_radius=6, fg_color=self._color_menu_actual)
    self.preview_menu.pack(side="left", padx=(0, 10))
    ctk.CTkButton(frame_cm, text=t(self.idioma, "settings_elegir_color"),
                    command=self._elegir_color_menu).pack(side="left")

    # --- color de letra ---
    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_color_letra"),
                    anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    frame_cl = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_cl.pack(fill="x", padx=22, pady=(0, 8))
    self.preview_letra = ctk.CTkLabel(frame_cl, text="", width=44, height=26,
                                        corner_radius=6, fg_color=self._color_letra_actual)
    self.preview_letra.pack(side="left", padx=(0, 10))
    ctk.CTkButton(frame_cl, text=t(self.idioma, "settings_elegir_color"),
                    command=self._elegir_color_letra).pack(side="left")

    # Foto De perfil
    ctk.CTkLabel(contenedor, text=t(self.idioma, "settings_foto"),
                         anchor="w", font=fuente_label).pack(fill="x", **pad_titulo)
    frame_foto = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_foto.pack(fill="x", padx=22, pady=(0, 14))
    self.lbl_foto = ctk.CTkLabel(frame_foto, text=self._nombre_archivo_foto(), anchor="w")
    self.lbl_foto.pack(side="left", fill="x", expand=True)
    ctk.CTkButton(frame_foto, text=t(self.idioma, "settings_elegir_foto"),
                    width=130, command=self._elegir_foto).pack(side="right", padx=(6, 0))

    # --- botones inferiores (fuera del scroll, siempre visibles) ---
    frame_botones = ctk.CTkFrame(self, fg_color="transparent")
    frame_botones.pack(fill="x", padx=22, pady=(0, 16))
    ctk.CTkButton(frame_botones, text=t(self.idioma, "settings_cancelar"),
                    fg_color="#7f8c8d", hover_color="#616a6b",
                    command=self.destroy).pack(side="right", padx=(8, 0))
    ctk.CTkButton(frame_botones, text=t(self.idioma, "settings_guardar"),
                    command=self._guardar).pack(side="right")

    def _nombre_archivo_foto(self):
        if self._foto_actual:
            return os.path.basename(self._foto_actual)
        return t(self.idioma, "sin foto")

    def _ajustar_fuente(self, delta):
        try:
            valor = int(self.entry_fuente.get().strip())
        except ValueError:
            valor = 12
            valor = max(6, min(72, valor + delta))
            self.entry_fuente.delete(0, "end")
            self.entry_fuente.insert(0, str(valor))

    def _elegir_color_menu(self):
        color = colorchooser.askcolor(color=self._color_letra_actual,
                                      tittle=t(self.idioma, "settings_color_letra"))
        if color and color[1]:
            self._color_letra_actual = color[1]
            self.preview_letra.configure(fg_color=self._color_letra_actual)

    def _elegir_foto(self):
        ruta = filedialog.askopenfilename(
            tittle=t(self.idioma, "settings_elegir_foto"),
            filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                       ("Todos los archivos", "*.*")]
        )
        if ruta:
            self._foto_actual = ruta
            self.lbl_foto.configure(text=self._nombre_archivo_foto())

    def _guardar(self):
        try:
            tamaño = int(self.entry_fuente.get().strip())
            if tamaño <=0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(t(self.idioma, "aviso_titulo"),
                                   t(self.idioma, "tamaño_invalido"))
            return
        nuevo_config = {
            "nombre_usuario": self.entry_nombre.get().strip() or "Usuario",
            "tema_interfaz": self.tema_var.get(),
            "idioma": self.idioma_var.get(),
            "tamaño_fuente": tamaño,
            "color_menu": self._color_menu_actual,
            "color_letra": self._color_letra_actual,
            "foto_perfil": self._foto_actual,
        }
        self.on_guardar(nuevo_config, self)
        