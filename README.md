# detectDdos
withPy
from flask import Flask, request
import threading
import time

app = Flask(__name__)

# Dictionnaire pour stocker les informations de connexion par adresse IP
connections = {}

# Seuil de connexions simultanées autorisées
seuil_connexions = 10

# Durée maximale autorisée pour une connexion (en secondes)
duree_max_connexion = 10

def detecter_attaque_slowloris():
    while True:
        # Parcours des connexions pour vérifier la durée
        for ip, (timestamp, conn) in list(connections.items()):
            if time.time() - timestamp > duree_max_connexion:
                print(f"Connexion expirée pour {ip}")
                conn.close()
                del connections[ip]

        # Vérification du seuil de connexions simultanées
        if len(connections) > seuil_connexions:
            print("Attaque Slowloris détectée!")
        
        time.sleep(1)

# Démarrer le thread de détection en arrière-plan
thread_detection = threading.Thread(target=detecter_attaque_slowloris)
thread_detection.daemon = True
thread_detection.start()

@app.route("/")
def home():
    ip = request.remote_addr
    
    if ip not in connections:
        connections[ip] = (time.time(), request.environ['wsgi.input'])
        print(f"Nouvelle connexion de {ip}")
    
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
