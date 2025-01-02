
import json
from datetime import datetime

class BnB:
    def __init__(self):
        self.stanze = {f"Stanza {i+1}": {"posti": 2, "prenotata": False} for i in range(10)}
        self.prezzo_bassa = 100
        self.prezzo_alta = 150
        self.prenotazioni = self.carica_prenotazioni()

    def calcola_prezzo(self, giorni, alta_stagione):
        prezzo = self.prezzo_alta if alta_stagione else self.prezzo_bassa
        return prezzo * giorni

    def prenota_stanza(self, nome_stanza, nome_cliente, giorni, alta_stagione):
        if self.stanze[nome_stanza]["prenotata"]:
            return False

        costo = self.calcola_prezzo(giorni, alta_stagione)
        prenotazione = {
            "cliente": nome_cliente,
            "stanza": nome_stanza,
            "giorni": giorni,
            "stagione": "Alta Stagione" if alta_stagione else "Bassa Stagione",
            "costo": costo,
        }

        self.prenotazioni.append(prenotazione)
        self.stanze[nome_stanza]["prenotata"] = True
        self.salva_prenotazioni()
        return True

    def annulla_prenotazione(self, nome_stanza):
        if self.stanze[nome_stanza]["prenotata"]:
            self.stanze[nome_stanza]["prenotata"] = False
            self.prenotazioni = [p for p in self.prenotazioni if p["stanza"] != nome_stanza]
            self.salva_prenotazioni()
            return True
        return False

    def elimina_prenotazione(self, nome_stanza, nome_cliente):
        for prenotazione in self.prenotazioni:
            if prenotazione["stanza"] == nome_stanza and prenotazione["cliente"] == nome_cliente:
                self.prenotazioni.remove(prenotazione)
                self.stanze[nome_stanza]["prenotata"] = False
                self.salva_prenotazioni()
                return True
        return False

    def carica_prenotazioni(self):
        try:
            with open("prenotazioni.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salva_prenotazioni(self):
        with open("prenotazioni.json", "w") as file:
            json.dump(self.prenotazioni, file, indent=4)
