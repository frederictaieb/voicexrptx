def make_prompt(commande):
    prompt = f"""
    Tu es un assistant de paiement. 
    À partir du texte suivant: {commande}, génère un JSON complet avec les champs suivants:
    - "action" : "send"
    - "amount" : "20"
    - "currency" : "XRP"
    - "recipient" : "Alice"
    Réponds uniquement avec un JSON strictement valide, sans commentaire ni texte additionnel. 
    """
    return prompt
