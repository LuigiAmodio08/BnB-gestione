from datetime import datetime

def determina_stagione(inizio, fine):
    alta_inizio = datetime(inizio.year, 6, 1)
    alta_fine = datetime(inizio.year, 10, 1)
    return alta_inizio <= inizio <= alta_fine or alta_inizio <= fine <= alta_fine
