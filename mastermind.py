# Nome: Matteo Borgio
# Partner: /

import random as r

# Funzione per generare la sequenza segreta
def genera_sequenza_segreta(dimensione: int = 4, minimo: int = 1, massimo: int = 6):
    sequenza_segreta = []
    while len(sequenza_segreta) < dimensione:
        numero = r.randint(minimo, massimo)
        if numero not in sequenza_segreta:
            sequenza_segreta.append(numero)
        else:
            continue
    return sequenza_segreta

# Funzione per fare in modo che l'utente inserisca una sequenza segreta
def leggi_sequenza_utente(dimensione: int = 4, minimo: int = 1, massimo: int = 6):
    sequenza_utente = []
    for i in range(dimensione):
        while True:
            try:
                numero = int(input(f"Inserisci il {i+1}° numero: "))
                if numero < 1 or numero > 6:
                    print(f"Il numero deve essere compreso tra {minimo} e {massimo}.")
                    continue
                sequenza_utente.append(numero)
                break
            except ValueError:
                print("! Devi inserire un numero valido.")
    return sequenza_utente

# Funzione per verificare la correttezza della sequenza e dare un feedback sulla correttezza delle lettere
def calcola_feedback(sequenza_segreta: list, sequenza_utente: list):
    elementi_posto_giusto = []
    elementi_posto_sbagliato = []
    for i in range(len(sequenza_segreta)):
        if sequenza_utente[i] == sequenza_segreta[i]:                # Verifica se il numero nella posizione "i" corrisponde in entrambe le sequenza di numeri
            elementi_posto_giusto.append(sequenza_utente[i])
        elif sequenza_utente[i] in sequenza_segreta:                 # Verifica se il numero nella posizione "i" è presente nella sequenza segreta
            elementi_posto_sbagliato.append(sequenza_utente[i])
    feedback = {                                                     # Utilizzo un dizionario con 2 chiavi, a cui corrispondono rispettivamente le liste
        "elementi_posto_giusto": elementi_posto_giusto,
        "elementi_posto_sbagliato": elementi_posto_sbagliato
    }
    return feedback                                                   # Ritorna il dizionario "feedback"

# Funzione per determinare il numero di tentativi
def selezione_difficoltà():
    while True:
        try:                                                                   # Try ed except per la gestione dell'errore, ad esempio Value Error se l'utente inserisce un valore non numerico
            print("Seleziona la difficoltà: ")
            print("1. Facile: 15 tentativi")
            print("2. Medio: 10 tentativi")
            print("3. Difficile: 7 tentativi \n")
            difficoltà = int(input())
            print("")
            if difficoltà < 1 or difficoltà > 3:
                print("! Seleziona una difficoltà valida. \n")
                continue
            if difficoltà == 1:
                print("Difficoltà impostata su facile. \n")
                return 15
            elif difficoltà == 2:
                print("Difficoltà impostata su medio. \n")
                return 10
            else:
                print("Difficoltà impostata su difficile. \n")
                return 7
        except ValueError:
            print("")
            print("! Inserisci un numero che corrisponda a una difficoltà (1, 2 o 3). \n")
            continue

# Funzione che racchiude il funzionamento del gioco
def gioca_partita(tentativi: int = 10):
    sequenza_segreta = genera_sequenza_segreta(4, 1, 6)
    count = 0
    for i in range(tentativi):
        count += 1
        print(f"Tentativo {i+1}/{tentativi}:")
        sequenza_utente = leggi_sequenza_utente(4, 1, 6)
        feedback = calcola_feedback(sequenza_segreta, sequenza_utente)
        print("")
        print(f"Elementi posti giusto: {feedback['elementi_posto_giusto']}")
        print(f"Elementi posti sbagliati: {feedback['elementi_posto_sbagliato']}")
        print("")
        if sequenza_utente == sequenza_segreta:                                   # Verifica se le sequenza sono identiche
            print("Hai indovinato la sequenza!")
            break
        if count == tentativi:
            print(f"Hai esaurito i tentativi. La sequenza era: {sequenza_segreta}")
            break
    return None

# Definisco la funzione principale
def main():
    print("")
    print("Benvenuto in Mastermind!")
    print("Il tuo obiettivo è indovinare la sequenza segreta di numeri. \n")

    # Scelta della difficoltà
    tentativi = selezione_difficoltà()

    # Avvia la partita
    gioca_partita(tentativi)

    print("Grazie per aver giocato!")

main()
