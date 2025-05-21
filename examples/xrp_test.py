from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import submit_and_wait

def send_tx(amount: float, recipient: str):
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)

    # Generate a test wallet
    print("Generating test Wallet...")
    wallet_generated = generate_faucet_wallet(client, debug=True)
    print(wallet_generated)

    # Create a payment transaction
    payment = Payment(
        account=wallet_generated.address,
        amount=xrp_to_drops(amount),
        destination=recipient,
    )

    tx_response = submit_and_wait(payment, client, wallet_generated)
    print(tx_response)

if __name__ == "__main__":
    send_tx(20, "r9iwLjPvqcaMSodxD38moZfEtiUSQQepfa")