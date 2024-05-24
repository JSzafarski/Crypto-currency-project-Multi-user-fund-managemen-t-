from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair

client = Client("https://api.mainnet-beta.solana.com")
master_wallet = "4vRvpS3zpygYZWdwE4JGq7RVfHsh6GzSDMVFxTCYpDeT"
master_priv_key = "3gKY76n8vdPBZgwU9e1mF2AfFNFCU1hQKh5kv32MpeZnvTH2D9ZWozfgqZp5QR2uekV8FohYempgQRDPyJUAdgef"


def transfer_to_master(user_priv_key, amount):  # identical to withdraw function but it will have one withdrawal adress
    sender = Keypair.from_private_key(user_priv_key)
    receiver = PublicKey(master_wallet)
    amount = float(amount)
    amount = int(amount * 10 ** 9)
    instruction = transfer(
        from_public_key=sender.public_key,
        to_public_key=receiver,
        lamports=amount
    )
    transaction = Transaction(instructions=[instruction], signers=[sender])
    result = client.send_transaction(transaction)
    print("Transaction response: ", result)
    return True


def withdraw(withdrawal_address, amount):
    sender = Keypair.from_private_key(master_priv_key)
    receiver = PublicKey(withdrawal_address)
    amount = float(amount)
    amount = int(amount * 10 ** 9)
    instruction = transfer(
        from_public_key=sender.public_key,
        to_public_key=receiver,
        lamports=amount
    )
    transaction = Transaction(instructions=[instruction], signers=[sender])
    result = client.send_transaction(transaction)
    return True, result
