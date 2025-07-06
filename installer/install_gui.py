import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import openai
except ImportError:
    openai = None

REQUIREMENTS = ["openai", "streamlit", "faster-whisper", "pyyaml"]


def install_requirements() -> None:
    """Install required packages via pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", *REQUIREMENTS])


def validate_key(key: str) -> bool:
    """Check if the provided OpenAI key is valid."""
    if openai is None:
        return False
    openai.api_key = key
    try:
        openai.Model.list()
        return True
    except Exception:
        return False


def import_env(entry: tk.Entry) -> None:
    """Load OPENAI_API_KEY from a .env file."""
    path = filedialog.askopenfilename(title=".env Datei wählen", filetypes=[("env", "*.env"), ("Alle Dateien", "*.*")])
    if not path:
        return
    key = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY="):
                key = line.strip().split("=", 1)[1]
                break
    if key:
        entry.delete(0, tk.END)
        entry.insert(0, key)
    else:
        messagebox.showerror("Fehler", "OPENAI_API_KEY nicht gefunden")


def main() -> None:
    install_requirements()

    root = tk.Tk()
    root.title("LIFe Installer")

    tk.Label(root, text="OPENAI_API_KEY:").pack(padx=10, pady=5)
    entry = tk.Entry(root, width=50, show="*")
    entry.pack(padx=10, pady=5)

    def on_submit() -> None:
        key = entry.get().strip()
        if not key:
            messagebox.showerror("Fehler", "Bitte API Key eingeben")
            return
        if not validate_key(key):
            messagebox.showerror("Fehler", "Ungültiger API Key")
            return
        os.environ["OPENAI_API_KEY"] = key
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"OPENAI_API_KEY={key}\n")
        messagebox.showinfo("Erfolg", "API Key gespeichert. Die Anwendung kann nun gestartet werden.")
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Aus .env importieren", command=lambda: import_env(entry)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Bestätigen", command=on_submit).pack(side=tk.LEFT, padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()
