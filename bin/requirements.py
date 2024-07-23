import subprocess
import sys

# Liste der notwendigen Pakete
required_packages = [
    "pandas",
    "re",      # Standard-Bibliothek, daher keine Installation erforderlich
    "datetime", # Standard-Bibliothek, daher keine Installation erforderlich
    "py",
    "tkinter"  # Standard-Bibliothek, daher keine Installation erforderlich
]

# Überprüfen und installieren der fehlenden Pakete
for package in required_packages:
    try:
        if package not in sys.modules and package != "re" and package != "datetime":
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Installation des Pakets {package}: {e}")

print("Alle notwendigen Pakete sind installiert.")
