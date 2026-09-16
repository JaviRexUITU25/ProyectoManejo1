import os
import sys
import customtkinter as ctk
from tkinter import Menu, messagebox

import config_manager
from settingWin import SettingsWin
from i18n import t

try:
    from PIL import Image
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

ctk.set_default_color_theme("blue")

class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ----------------------------
        # Carga inicial: si el archivo no existe o esta corrupto
        # config_manager agrega valores por defecto automaticamente
        # ----------------------------
        resultado_carga = config_manager.load_config()
        self.config = resultado_carga.data
        self.idioma = self.config.get("idioma", "es-ES")
        self._imagen_perfil_ctk = None

        self.tittle(t(self.idioma, "app_titulo"))
        self.geometry("900x580")
        self.minsize(700, 480)

        self._construir_barra_menu()
        self._construir_contenido()
        self._aplicar_configuracion()

        # Si pasa algun error o no hay archivo
        if resultado_carga.status not in ("not_found"):
            self.after(300, lambda: messagebox.showwarning(
                t(self.idioma, "aviso_titulo"), resultado_carga.message))

        # MENU PRINCIPAL ------------------------------------------------------------
        def _construir_barra_menu(self):
            self.frame_memu = ctk.CTkFrame(self, height =44, corner_radius = 0)
            self.frame_menu.pack(side="top", fill="x")
            self.frame_menu.pack_propagate(False)

            self.botones_menu = {}
            especificaciones = [
                ("menu_archivo", self._abrir_menu_archivo),
                ("menu_edicion", self._abrir_menu_edicion),
                ("menu_ver", self._abrir_menu_ver),
                ("menu_settings", self._abrir_settings),
            ]
            for i, (clave, comando) in enumerate(especificaciones):
                btn = ctk.CTkButton(self.frame_menu, text=t(self.idioma,clave),
                                    width = 95, corner_radius=6,
                                    fg_color = "transparent", command=comando)
                btn.pack(side="left", padx=(14 if i == 0 else 4,4),pady=7)
                self.botones_menu[clave] = btn

        def _popup_simulado(self, opciones):
            menu = Menu(self, tearoff=0)
            for etiqueta, comando_real in opciones:
                menu.add_command(label=etiqueta, command=comando_real or self._mostrar_aviso_simulado)
                return menu

        def _abrir_menu_archivo(self):
            opciones = [
                (t(self.idioma, "archivo_nuevo"), None),
                (t(self.idioma, "archivo_abrir"), None),
                (t(self.idioma, "archivo_guardar"), None),
                (t(self.idioma, "archivo_guardar_como"), None),
                (t(self.idioma, "archivo_salir"), self._salir),
            ]
            self._mostrar_popup(self.botones_menu["menu_archivo"], opciones)

        def _abrir_menu_edicion(self):
            opciones = [
                (t(self.idioma, "edicion_deshacer"), None),
                (t(self.idioma, "edicion_rehacer"), None),
                (t(self.idioma, "edicion_cortar"), None),
                (t(self.idioma, "edicion_copiar"), None),
                (t(self.idioma, "edicion_pegar"), None),
            ]
            self._mostrar_popup(self.botones_menu["menu_edicion"], opciones)

        def _abrir_menu_ver(self):
            opciones = [
            (t(self.idioma, "ver_pantalla_completa"), None),
            (t(self.idioma, "ver_zoom_mas"), None),
            (t(self.idioma, "ver_zoom_menos"), None),
            (t(self.idioma, "ver_barra_estado"), None),
            ]
            self._mostrar_popup(self.botones_menu["menu_ver"], opciones)

        def _mostrar_popup(self,boton,opciones):
            menu = self._popup_simulado(opciones)
            x = boton.winfo_rootx()
            y = boton.winfo_rooty() + boton.winfo_height()
            try:
                menu.tk_popup(x.y)
            finally:
                menu.grab_release()
        def _mostrar_aviso(self):
            messagebox.showinfo(t(self.idioma, "titulo_simulado"), t(self.idioma, "msg_simulado"))

        def _salir(self):
            self.destroy()

        # SETTINGS (ESTO DEBE SER FUNCIONAL)

        
