import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime

class BnBApp:
    def __init__(self, root, bnb):  # Corretto __init__ (non _init_)
        self.bnb = bnb
        self.root = root
        self.root.title("Gestione Prenotazioni BnB")
        self.root.geometry("900x700")
        self.root.configure(bg="#e4f1f6")
        self.schermata_iniziale()

    def schermata_iniziale(self):
        self.frame_iniziale = tk.Frame(self.root, bg="#4f9d7f", bd=10, relief="solid")
        self.frame_iniziale.pack(fill="both", expand=True)

        tk.Label(
            self.frame_iniziale,
            text="Benvenuti a Orsi Coraggiosi",
            font=("Arial", 28, "bold"),
            bg="#4f9d7f",
            fg="white"
        ).pack(pady=40)

        tk.Label(
            self.frame_iniziale,
            text="Un'esperienza unica nella splendida Costiera Amalfitana.",
            font=("Arial", 18),
            bg="#4f9d7f",
            fg="white"
        ).pack(pady=20)

        tk.Button(
            self.frame_iniziale,
            text="Vai alla Prenotazione",
            font=("Arial", 16),
            bg="#007BFF",
            fg="white",
            relief="raised",
            height=2,
            width=20,
            command=self.mostra_schermata_prenotazione
        ).pack(pady=30)

    def mostra_schermata_prenotazione(self):
        self.frame_iniziale.destroy()
        self.crea_interfaccia()

    def crea_interfaccia(self):
        self.main_frame = tk.Frame(self.root, bg="#e4f1f6", bd=10)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text="Nome Cliente:", font=("Arial", 14), bg="#e4f1f6").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.entry_nome = tk.Entry(self.main_frame, font=("Arial", 14), width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="Seleziona Stanza:", font=("Arial", 14), bg="#e4f1f6").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.stanza_var = tk.StringVar(value=list(self.bnb.stanze.keys())[0])
        tk.OptionMenu(self.main_frame, self.stanza_var, *self.bnb.stanze.keys()).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="Seleziona Date:", font=("Arial", 14), bg="#e4f1f6").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.cal_inizio = Calendar(self.main_frame, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 12))
        self.cal_inizio.grid(row=3, column=0, padx=20, pady=10)

        self.cal_fine = Calendar(self.main_frame, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 12))
        self.cal_fine.grid(row=3, column=1, padx=20, pady=10)

        tk.Button(self.main_frame, text="Prenota", font=("Arial", 14), bg="#4f9d7f", fg="white", relief="raised", height=2, width=20, command=self.prenota).grid(row=4, column=0, columnspan=2, pady=20)

        tk.Label(self.main_frame, text="Prenotazioni:", font=("Arial", 16, "bold"), bg="#e4f1f6").grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.lista_prenotazioni = tk.Listbox(self.main_frame, font=("Arial", 12), width=50, height=10, bg="#ffffff", fg="#4f9d7f", selectmode="single")
        self.lista_prenotazioni.grid(row=6, column=0, columnspan=2, padx=20, pady=10)

        tk.Button(self.main_frame, text="Elimina Prenotazione", font=("Arial", 14), bg="#FF4D4D", fg="white", relief="raised", height=2, width=20, command=self.elimina_prenotazione).grid(row=7, column=0, columnspan=2, pady=20)

    def determina_stagione(self, inizio, fine):
        alta_inizio = datetime(inizio.year, 6, 1)
        alta_fine = datetime(inizio.year, 10, 1)

        if alta_inizio <= inizio <= alta_fine or alta_inizio <= fine <= alta_fine:
            return True
        return False

    def prenota(self):
        nome_cliente = self.entry_nome.get()
        nome_stanza = self.stanza_var.get()
        data_inizio = datetime.strptime(self.cal_inizio.get_date(), "%Y-%m-%d")
        data_fine = datetime.strptime(self.cal_fine.get_date(), "%Y-%m-%d")

        if data_fine <= data_inizio:
            messagebox.showerror("Errore", "La data di fine deve essere successiva alla data di inizio.")
            return

        giorni = (data_fine - data_inizio).days
        alta_stagione = self.determina_stagione(data_inizio, data_fine)

        if self.bnb.prenota_stanza(nome_stanza, nome_cliente, giorni, alta_stagione):
            stagione = "Alta Stagione" if alta_stagione else "Bassa Stagione"
            costo = self.bnb.calcola_prezzo(giorni, alta_stagione)
            self.lista_prenotazioni.insert(
                tk.END,
                f"{nome_cliente} - {nome_stanza} - {giorni} giorni - {stagione} - {costo} EUR",
            )
            messagebox.showinfo("Successo", "Prenotazione effettuata con successo.")
        else:
            messagebox.showerror("Errore", f"La stanza {nome_stanza} è già prenotata.")

    def elimina_prenotazione(self):
        selezione = self.lista_prenotazioni.curselection()
        if not selezione:
            messagebox.showerror("Errore", "Seleziona una prenotazione da eliminare.")
            return

        prenotazione = self.lista_prenotazioni.get(selezione)
        nome_stanza = prenotazione.split(" - ")[1]
        nome_cliente = prenotazione.split(" - ")[0]
        if self.bnb.elimina_prenotazione(nome_stanza, nome_cliente):
            self.lista_prenotazioni.delete(selezione)
            messagebox.showinfo("Successo", "Prenotazione eliminata con successo.")
        else:
            messagebox.showerror("Errore", "Impossibile eliminare la prenotazione.")
