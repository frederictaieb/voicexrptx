import requests
import json
def ask_ollama(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    #print("DEBUG JSON:", response.json())  # 👈 ajoute cette ligne
    return response.json()["response"].strip()


# Exemple : compréhension de commande
commande = "Envoie 20 XRP à Alice"

prompt = f"""
    Tu es un assistant de paiement. 
    À partir du texte suivant: {commande}, génère un JSON complet avec les champs suivants:
    - action : send
    - amount : 20 
    - currency : XRP
    - recipient : Alice
    Réponds uniquement avec l'objet JSON, sans texte additionnel. "
    """

resultat = ask_ollama(prompt)
print(json.loads(resultat.strip()))
