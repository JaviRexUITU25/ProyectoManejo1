import json
import os
import shutil

_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(_CONFIG_DIR, "config.json")
BACKUP_FILE = os.path.join(_CONFIG_DIR, "config.bak")
TEMP_FILE = os.path.join(_CONFIG_DIR, "config.tmp")

DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "claro",       # "claro" | "oscuro"
    "idioma": "es-ES",              # "es-ES" | "en-US"
    "tamaño_fuente": 12,
    "color_menu": "#2C3E50",
    "color_letra": "#FFFFFF",
    "foto_perfil": "",  
}

REQUIRED_KEYS = set(DEFAULT_CONFIG.keys())

class ConfigResult:
    def __init__(self, data, status="ok", message=""):
        self.data = data
        self.status = status
        self.message = message
    @property
    def ok(self):
        return self.status == "ok"

    def __repr__(self):
        return f"ConfigResult(status={self.status!r}, message={self.message!r})"


def _validar_y_completar(data):
    if not isinstance(data, dict):
        raise ValueError("El contenido del archivo no es un objeto JSON valido")
    
    config = DEFAULT_CONFIG.copy()
    for key in REQUIRED_KEYS:
        if key in data:
            config[key] = data[key]

    try:
        config["tamaño_fuente"] = int(config["tamaño_fuente"])
        if config["tamaño_fuente"] <=0:
            raise ValueError
    except (ValueError, TypeError):
        config["tamaño_fuente"] = DEFAULT_CONFIG["tamaño_fuente"]

    if config.get("tema_intefaz") not in ("claro", "oscuro"):
        config["tema_interfaz"] = DEFAULT_CONFIG["tema_interfaz"]

    if config.get("idioma") not in ("es-ES", "en-US"):
        config["idioma"] = DEFAULT_CONFIG["idioma"]

    for clave_color in ("color_menu", "color_letra"):
        valor = config.get(clave_color)
        if not isinstance(valor, str) or not valor.startswith("#"):
            config[clave_color] = DEFAULT_CONFIG[clave_color]

    if not isinstance(config.get("foto_perfil"), str):
        config["foto_perfil"] = ""

    if not isinstance(config.get("nombre_usuario"), str) or not config["nombre_usuario"].strip():
        config["nombre_usuario"] = DEFAULT_CONFIG["nombre_usuario"]
    return config

def _intentar_cargar_backup():
    if not os.path.exists(BACKUP_FILE):
        return None
    try:
        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return _validar_y_completar(data)
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError, PermissionError):
        return None
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return ConfigResult(
            DEFAULT_CONFIG.copy(), "not_found",
            "No existe un archivo de configuracion previo."
        )
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            contenido = f.read()
        data = json.loads(contenido)
        config = _validar_y_completar(data)
        return ConfigResult(config, "ok")
    except PermissionError:
        return ConfigResult(
            DEFAULT_CONFIG.copy(), "permission_denied",
            f"Sin permisos de lectura sobre '{os.path.basename(CONFIG_FILE)}'."
        )
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
        recuperado = _intentar_cargar_backup()
        if recuperado is not None:
            return ConfigResult(
                recuperado, "corrupt_recovered",
                f"El archivo estaba dañado ({e}). "
                f"Se recupero la configuracion"
            )
        return ConfigResult(
            DEFAULT_CONFIG.copy(), "corrupt",
            f"El archivo estaba dañado ({e}) y no habia ningun"
            f"respaldo utilizable."
        )

def save_config(config):
    try:
        config_validado = _validar_y_completar(config)
    except ValueError as e:
        return ConfigResult(config, "error", f"Configuracion invalida")

    try:
        with open(TEMP_FILE, "w", encoding="utf-8") as f:
            json.dump(config_validado, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())

        if os.path.exists(CONFIG_FILE):
            try:
                shutil.copy2(CONFIG_FILE, BACKUP_FILE)
            except OSError:
                pass

        os.replace(TEMP_FILE, CONFIG_FILE)
        return ConfigResult(config_validado, "ok", "Configuracion guardada correctamente")

    except PermissionError:
        _limpiar_temporal()
        return ConfigResult(
            config_validado, "permission_denied",
            f"Sin permisos sobre '{os.path.basename(CONFIG_FILE)}'. "
            f"No se guardaron los cambios"
        )
    except OSError as e:
        _limpiar_temporal()
        return ConfigResult(config_validado, "error", f"Error al guardar la configuracion: {e}")

def _limpiar_temporal():
    try:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
    except OSError:
        pass

    