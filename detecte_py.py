import time
from sklearn.ensemble import IsolationForest

# Chemin vers le fichier de logs Apache
LOG_FILE = "/var/log/apache2/access.log"

# Nombre maximum de requêtes par seconde tolérées
THRESHOLD = 100

# Fonction pour charger les données du fichier de logs
def load_data():
    with open(LOG_FILE, 'r') as file:
        # Charger les adresses IP à partir des logs Apache
        ips = [line.split()[0] for line in file]
    return ips

# Fonction pour détecter une attaque DDoS
def detect_ddos(ips):
    # Utiliser Isolation Forest pour détecter des anomalies dans les données
    model = IsolationForest(contamination=0.1)  # ajuster selon les besoins
    model.fit([[ip] for ip in ips])

    while True:
        # Charger les adresses IP actuelles à partir des logs Apache
        current_ips = load_data()

        # Prédire les anomalies avec le modèle
        predictions = model.predict([[ip] for ip in current_ips])

        # Identifier les adresses IP suspectes
        suspicious_ips = [ip for ip, pred in zip(current_ips, predictions) if pred == -1]

        if suspicious_ips:
            print("Attaque DDoS détectée. Adresses IP suspectes :", suspicious_ips)
            # Ajouter ici des règles pour bloquer les adresses IP, notifier, etc.

        time.sleep(1)

# Démarrer la détection
ips_data = load_data()
detect_ddos(ips_data)
