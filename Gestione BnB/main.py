# main.py
from app import BnBApp
from bnb import BnB  
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()         
    bnb = BnB()            
    app = BnBApp(root, bnb)
    root.mainloop()         
