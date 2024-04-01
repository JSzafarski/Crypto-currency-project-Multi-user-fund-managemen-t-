from solana.rpc.api import Client
from solana.rpc.core import UnconfirmedTxError
from spl.token.client import Token
from solders.pubkey import Pubkey
from solana.transaction import Transaction
import solders

mint = Pubkey.from_string(
    "mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"
)
program_id = Pubkey.from_string(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
)

privkey = "32Rn2QKHZFJ9dUWrH1FdUzZe2VwuNQcyRKUt6fhSArjGVBqhgD5Bguuvbc62aYBAcpQN7FsFd1FdrzemeJb7tiHU"
# key_pair = Keypair.from_base58_string(privkey)
key_pair = solders.keypair.Keypair.from_base58_string(privkey)
solana_client = Client("https://mainnet.helius-rpc.com/?api-key=f61ec600-eb2e-492c-b5ca-5c6393d1b7e1")
spl_client = Token(
    conn=solana_client, pubkey=mint, program_id=program_id, payer=key_pair
)
source = Pubkey.from_string("G12Gw8DWHLL4ADUsumZTh2AsvVCpWJ6whpPmLYP1x8px")


def send_tokens(dest_address, amount):
    dest = Pubkey.from_string(dest_address)
    try:
        source_token_account = (
            spl_client.get_accounts_by_owner(
                owner=source, commitment=None, encoding="base64"
            )
            .value[0]
            .pubkey
        )
    except IndexError:
        source_token_account = spl_client.create_associated_token_account(
            owner=source, skip_confirmation=False, recent_blockhash=None
        )

    try:
        dest_token_account = (
            spl_client.get_accounts_by_owner(owner=dest, commitment=None, encoding="base64")
            .value[0]
            .pubkey
        )
    except IndexError:
        while True:
            try:
                dest_token_account = spl_client.create_associated_token_account(  # thsi si the problem
                    owner=dest, skip_confirmation=False, recent_blockhash=None
                )
                print(dest_token_account)
                break
            except UnconfirmedTxError:
                print("retesting")
                continue

    transaction = spl_client.transfer(
        source=source_token_account,
        dest=dest_token_account,
        owner=key_pair,
        amount=int(float(amount) * 10 ** 11),  # 11 decimals
        multi_signers=None,
        opts=None,
        recent_blockhash=None,
    )

    return f"https://solscan.io/tx/{transaction.value}"

# print(send_tokens(100, "A7xvKH7emePiPvnAYvrjHzJ6XB5vqTA6Py2fJtHBrY2p")) for testing
