import os
import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox

from i18n import t

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, config: dict, on_guardar):
        