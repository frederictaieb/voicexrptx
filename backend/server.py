# backend/main.py
import whisper
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import make_prompt
import json

from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm


FOLDER_PATH = "data"
FILEPATH_AUDIO = FOLDER_PATH + "/audio.mp3"
FILEPATH_TRANSCRIBE = FOLDER_PATH + "/transcribe.txt"
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

#async def send_tx(amount: float, recipient: str):
    
    

    # Generate a test wallet
    # print("Generating test Wallet...")
    # wallet_generated = generate_faucet_wallet(client, debug=True)
    # print(wallet_generated)

    #wallet_src = Wallet.from_seed(seed="sEdVUPEuvc6Q16gq4dupSNfYdFZc1gT", algorithm=CryptoAlgorithm.ED25519)
    #print(wallet_src.address) # "rMCcNuTcajgw7YTgBy1sys3b89QqjUrMpH"

    # Create a payment transaction
    #payment = Payment(
    #    account=wallet_src.address,
    #    amount=xrp_to_drops(amount),
    #    destination=recipient,
    #)

    #tx_response = await submit_and_wait(payment, client, wallet_src)
    #print(tx_response)

app = FastAPI()

# Autoriser le frontend Next.js à accéder à l'API
origins = [
    "http://localhost:3000",  # Adresse du frontend Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("turbo")

@app.get("/api/transcribe")
async def transcribe_audio():
    result = model.transcribe(FILEPATH_AUDIO)
    with open(FILEPATH_TRANSCRIBE, "w") as file:
        file.write(result["text"])
    return {"text": result["text"]}

@app.get("/api/interpret")
async def interpret():
    with open(FILEPATH_TRANSCRIBE, "r") as file:
        text = file.read()
    print("DEBUG TEXT:", text)
               
    prompt = make_prompt(text)
    print("DEBUG PROMPT:", prompt)

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    print("DEBUG RESPONSE:", response.json())  # 👈 ajoute     cette ligne
    response_json = response.json()
    response_str = response_json["response"]
    response_str = response_str.strip()
    try:
        response_json = json.loads(response_str)
        print("DEBUG RESPONSE JSON:", response_json)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response: " + response_str}
    return response_json

@app.post("/api/send_xrp")
async def send_xrp(amount: float, recipient: str):
    client = JsonRpcClient(JSON_RPC_URL)
    wallet_src = Wallet.from_seed(seed="sEdVUPEuvc6Q16gq4dupSNfYdFZc1gT", algorithm=CryptoAlgorithm.ED25519)
    payment = Payment(
        account=wallet_src.address,
        amount=xrp_to_drops(amount),
        destination=recipient,
    )
    tx_response = await submit_and_wait(payment, client, wallet_src)
    return tx_response
    #send_tx(10, "r9iwLjPvqcaMSodxD38moZfEtiUSQQepfa")
    #return 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)