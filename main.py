import os
import sys
import customtkinter as ctk
from tkinter import Menu, messagebox

import Config
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
        resultado_carga = Config.load_config()
        self.config = resultado_carga.data
        self.idioma = self.config.get("idioma", "es-ES")
        self._imagen_perfil_ctk = None

        self.title(t(self.idioma, "app_title"))
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
        def _abrir_settings(self):
            self._settings_win = SettingsWin(self, self.config, on_guardar=self._guardar)

        def _guardar(self, nuevo_config, ventana):
            resultado = config_manager.save_config(nuevo_config)

            if resultado.ok:
                self.config = resultado.data
                self.idioma = self.config.get("idioma", "es-ES")
                self._aplicar_configuraciion()
                self._reconstruir_textos_menu()
                messagebox.showinfo(t(self.idioma, "aviso_titulo"),
                                    t(self.idioma, "settings_guardado"))
                ventana.destroy()
            else:
                # Por si no guarda ijjijia
                messagebox.showerror(t(self.idioma, "aviso_titulo"),
                                     t(self.idioma, "settings_guardado_error",
                                       detalle=resultado.message))

    # Contenido principal
    def _consrtuir_contenido(self):
        self.frame_contenido = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_contenido.pack(fill="both", expand=True, padx=30, pady=26)

        self.lbl_avatar = ctk.CTkLabel(self.frame_contenido, text="", width=112, height=112)
        self.lbl_avatar.pack(pady=(6,14))

        self.lbl_bienvenida = ctk.CTkLabel(self.frame_contenido, text="")
        self.lbl_bienvenida.pack(pady=(0,20))

        self.tarjeta = ctk.CTkFrame(self.frame_contenido, corner_radius = 14)
        self.tarjeta.pack(fill="x", padx=60)

        self.lbl_resumen_titulo = ctk.CTkLabel(self.tarjeta, text="",
                                               font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_resumen_titulo.pack(anchor="w", padx=22, pady=(18,8))

        self.filas_resumen = {}
        claves_resumen = ("resumen_tema", "resumen_idioma", "resumen_fuente",
                          "resumen_color_menu", "resumen_color_letra")
        for clave in claves_resumen:
            fila = ctk.CTkLabel(self.tarjeta, text="", anchor="w", justify="left")
            fila.pack(anchor="w", padx=22, pady=3)
            self.filas_resumen[clave] = fila
        ctk.CTkLabel(self.tarjeta, text= "").pack(pady=8)

    def _recontruir_textos_menu(self):
        for clave, btn in self.botones_menu.items():
            btn.configure(text=t(self.idioma, clave))
        self.tittle(t(self.idioma, "titulo_app"))

    def _actualizar_resumen(self):
        nombre = self.config.get("nombre_usuario", "")
        self.lbl_bienvenida.configure(text=t(self.idioma, "binevenida", nombre=nombre))
        self.lbl_resumen_titulo.configure(text=t(self.idioma, "resumen_titulo"))

        tema = self.config.get("tema_interfaz", "claro")
        idioma_cfg = self.config.get("idioma", "es-ES")
        fuente = self.config.get("tamaño_fuente", 12)
        color_menu = self.config.get("color_menu", "#2C3E50")
        color_letra = self.config.get("color_letra", "#FFFFFF")

        self.filas_resumen["resumen_tema"].configure(
            text=f"{t(self.idioma, 'resumen_tema')}: {tema.capitalize()}")
        self.filas_resumen["resumen_idioma"].configure(
            text=f"{t(self.idioma, 'resumen_idioma')}: {idioma_cfg}")
        self.filas_resumen["resumen_fuente"].configure(
            text=f"{t(self.idioma, 'resumen_fuente')}: {fuente} pt")
        self.filas_resumen["resumen_color_menu"].configure(
            text=f"{t(self.idioma, 'resumen_color_menu')}: {color_menu}")
        self.filas_resumen["resumen_color_letra"].configure(
            text=f"{t(self.idioma, 'resumen_color_letra')}: {color_letra}")

    def _cargar_avatar(self):
        ruta = self.config.get("foto_perfil", "")
        if ruta and os.path.isfile(ruta) and PIL_DISPONIBLE:
            try:
                img = Image.open(ruta).convert("RGB")
                img.thumbnail((112,112))
                self._imagen_perfil_ctk = ctk.CTkImage(light_image=img, dar_image=img, size=img.size)
                self.lbl_avatar.configure(image=self._imagen_perfil_ctk,text="")
                return
            except Exception:
                pass
        self._imagen_perfil_ctk = None
        self.lbl_avatar.configure(image=None, text="👤", font=ctk.CTkFont(size=52))



#Aplicar la configuracion a la interfaz

    def _aplicar_configuracion(self):
        modo = "Dark" if self.config.get("tema_interfaz") == "oscuro" else "Light"
        ctk.set_appearence_mode(modo)

        color_menu = self.config.get("color_menu", "#2C3E50")
        color_letra = self.config.get("color_letra", "#FFFFFF")
        tamaño = self.config.get("tamaño_fuente", 12)

        self.frame_menu.configure(fg_color=color_menu)
        for btn in self.botones_menu.values():
            btn.configure(text_color=color_letra, font=ctk.CTkFont(size=max(tamaño - 1,8)))

        self.lbl_bienvenida.configure(font=ctk.CTkFont(size=tamaño + 8, weight="bold"))
        for fila in self.filas_resumen.values():
            fila.configure(font=ctk.CTkFont(size=tamaño))

        self._cargar_avatar()
        self._actualizar_resumen()

def main():
    try:
        app = Aplicacion()
        app.mainloop()
    except Exception as e:
        try:
            messagebox.showerror("Error: ", f"Ocurrio un error inesperado: \n{e}")
        except Exception:
            print(f"Error ocurrido: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()