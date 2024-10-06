import socket

HOST = '127.0.0.1'  
PORT = 12000        

def start_client():
    # Opretter en TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Forsøger at oprette forbindelse til serveren ved den angivne adresse og port
        s.connect((HOST, PORT))
        print(f"Forbundet til serveren på {HOST}:{PORT}")

        try:
            while True:
                # Modtager data fra serveren (op til 1024 bytes)
                data = s.recv(1024).decode()  # Modtager og dekoder beskeden fra serveren
                if not data:
                    break  # Afbryd hvis der ikke modtages nogen data
                print(f"Server: {data}")  # Udskriver beskeden fra serveren

                # Tjekker, om serverens besked indeholder en specifik prompt
                if "Skriv enten 'add', 'random' eller 'subtract':" in data or "Indtast to heltal" in data:
                    # Tager input fra brugeren og sender det til serveren
                    message = input("Du: ")
                    s.sendall(message.encode())  # Koder beskeden og sender den til serveren

        except Exception as e:
            # Håndterer eventuelle fejl
            print(f"Fejl: {e}")

if __name__ == "__main__":
    # Starter klientprogrammet
    start_client()
