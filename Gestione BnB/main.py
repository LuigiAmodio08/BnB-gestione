# main.py
from app import BnBApp
from bnb import BnB  # Importa il modulo bnb contenente la classe BnB
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()          # Crea la finestra principale
    bnb = BnB()             # Crea l'istanza del BnB
    app = BnBApp(root, bnb) # Avvia l'app
    root.mainloop()         # Avvia il ciclo dell'interfaccia grafica
