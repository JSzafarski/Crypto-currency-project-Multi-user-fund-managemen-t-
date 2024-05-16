from helius import BalancesAPI
from solana.rpc.api import Client, Keypair
import base58

client = Client("https://api.mainnet-beta.solana.com")
balances_api = BalancesAPI("edb81864-738f-4d62-8f20-f4d71545eb79")


def return_solana_balance(wallet_address):  # up to 25 addresses return a string
    spl_balances = balances_api.get_balances(wallet_address)
    sol_balance = float(spl_balances["nativeBalance"]) / 10 ** 9
    return sol_balance


def create_wallet():  # this is the wallet the user will deposit sol to
    if client:
        print("Connected to Solana cluster.")
    else:
        print("Unable to connect to Solana cluster.")
        return "", ""
    new_account = Keypair()
    wallet_address = new_account.pubkey()
    private_key_bytes = new_account.secret()
    public_key_bytes = bytes(new_account.pubkey())
    encoded_keypair2 = private_key_bytes + public_key_bytes
    private_key = base58.b58encode(encoded_keypair2).decode()
    return str(wallet_address), str(private_key)
