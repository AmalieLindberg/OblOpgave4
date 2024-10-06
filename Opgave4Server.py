import socket
import threading
import random

HOST = '127.0.0.1'  
PORT = 12000        

# Funktion til at håndtere kommunikation med en klient
def handle_client(conn, addr):
    print(f"Connected by {addr}")  # Udskriver klientens adresse ved forbindelse
    
    try:
        while True:
            # Send instruktion til klienten om at skrive en kommando ('add', 'random' eller 'subtract')
            conn.sendall("Skriv enten 'add', 'random' eller 'subtract': ".encode())

            # Modtag kommando fra klienten
            command = conn.recv(1024).decode().strip()  # Modtager og dekoder kommandoen
            if not command:
                break  # Afslut hvis der ikke er modtaget nogen kommando
            print(f"Received command: {command}")

            # Tjek for gyldige kommandoer
            if command not in ["add", "random", "subtract"]:
                # Hvis kommandoen ikke er gyldig, sendes en fejlmeddelelse
                conn.sendall("Ukendt kommando. Skriv enten 'add', 'random' eller 'subtract'.".encode())
                continue  # Gå tilbage til starten af løkken for at modtage en ny kommando

            # Bed klienten om at indtaste to tal
            conn.sendall("Indtast to heltal adskilt af mellemrum: ".encode())

            # Modtag tallene fra klienten
            numbers = conn.recv(1024).decode().strip()  # Modtager og dekoder tallene
            print(f"Received numbers: {numbers}")

            try:
                # Forsøg på at konvertere input til to heltal
                num1, num2 = map(int, numbers.split())
            except ValueError:
                # Hvis konverteringen fejler, sendes en fejlmeddelelse til klienten
                print("Fejl: Kunne ikke læse tallene. Sørg for at sende to heltal adskilt af et mellemrum.")
                conn.sendall("Fejl: Sørg for at sende to gyldige heltal adskilt af et mellemrum.".encode())
                continue  # Gå tilbage til starten af løkken for at modtage nye tal

            # Beregn resultatet baseret på klientens kommando
            result = ""
            if command == "random":
                # Hvis kommandoen er 'random', genereres et tilfældigt tal mellem de to indtastede tal
                result = f"Tilfældigt tal mellem {num1} og {num2}: {random.randint(num1, num2)}"
            elif command == "add":
                # Hvis kommandoen er 'add', beregnes summen af de to tal
                result = f"Summen af {num1} og {num2} er: {num1 + num2}"
            elif command == "subtract":
                # Hvis kommandoen er 'subtract', beregnes differencen mellem de to tal
                result = f"Differencen mellem {num1} og {num2} er: {num1 - num2}"

            # Send resultatet tilbage til klienten
            conn.sendall(result.encode())
            print(f"Sent result: {result}")

            # Efter at have sendt resultatet, sendes instruktionen igen for at modtage en ny kommando
            conn.sendall("\nSkriv enten 'add', 'random' eller 'subtract': ".encode())

    except Exception as e:
        # Håndterer eventuelle fejl
        print(f"Fejl ved håndtering af klient {addr}: {e}")
    finally:
        # Lukker forbindelsen til klienten, når løkken afsluttes
        conn.close()

# Funktion til at starte serveren
def start_server():
    # Opretter en TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Binder serveren til den angivne IP-adresse og port
        s.bind((HOST, PORT))
        # Lytter efter indgående forbindelser
        s.listen()
        print(f"Server started on {HOST}:{PORT}")

        while True:
            # Accepterer en ny forbindelse fra en klient
            conn, addr = s.accept()
            # Starter en ny tråd for at håndtere klienten
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()  # Starter tråden, som håndterer klienten

# Starter serveren, når scriptet køres
if __name__ == "__main__":
    start_server()