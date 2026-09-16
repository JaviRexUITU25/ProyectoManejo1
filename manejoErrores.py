import os
import stat
import json
import Config as cm

def _separador(titulo):
    print("\n" + "=" * 72)
    print(titulo)
    print("=" * 72)

def _limpiar():
    for ruta in (cm.CONFIG_FILE, cm.BACKUP_FILE, cm.TEMP_FILE):
        if os.path.exists(ruta):
            try:
                os.chmod(ruta, stat.S_IWRITE | stat.S_IREAD)
                os.remove(ruta)
            except OSError:
                pass

def archivo_ausente():
    _separador("Caso 1: archivo de configuracion ausente")
    _limpiar()
    resultado = cm.load_config()
    print(f"estado = {resultado.status}")
    print(f"Mensaje = {resultado.message}")
    print(f"datos = {resultado.data}")
    assert resultado.status == "not_found"
    print("Se cargaron valores por defecto")

def archivo_corrupto():
    _separador("Caso 2: archivo corrupto // formato invalido")
    _limpiar()
    with open(cm.CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write("Archivo JSON no valido")
    resultado = cm.load_config()
    print(f"Estado = {resultado.status}")
    print(f"Mensaje = {resultado.message}")
    print(f"Datos = {resultado.data}")
    assert resultado.status in ("corrupto", "corrupto recuperado")
    print("Archivo corrupto detectado")

def sin_permisos():
    _separador("Caso 3: archivo sin permisos de lectura")
    _limpiar()
    cm.save_config(cm.DEFAULT_CONFIG.copy())

    es_root = hasattr(os, "geteuid") and  os.geteuid() == 0

    try:
        os.chmod(cm.CONFIG_FILE, 0o000)
        resultado = cm.load_config()
        print(f"estado = {resultado.status}")
        print(f"Mensaje = {resultado.message}")
        print(f"Datos = {resultado.data}")

        if es_root:
            print("Se ejecuto como admin")
            print("Ejecuta este script con un usuario normal")
        elif os.name != "nt":
            assert resultado.status == "Permiso denegado"
            print("Sin permisos de lectura")

        else:
            print("En windows, chmod no revoca lectura real")
    finally:
        os.chmod(cm.CONFIG_FILE, stat.S_IWRITE | stat.S_IREAD)


def respaldo_y_escritura_segura():
    pass

if __name__ == "__main__":
    archivo_ausente()
    archivo_corrupto()
    sin_permisos()
    respaldo_y_escritura_segura()
    _separador("Pruebas finalizadas")
