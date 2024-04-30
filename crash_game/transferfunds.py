from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair

client = Client("https://api.mainnet-beta.solana.com")
master_wallet = "DbDnA5p2BsuGwCB7QJ7txZNxd5Exh4u3WJ6zDtyardcX"
master_priv_key = "5Q7L6PD7oLPt4Z5ms7AcJoLtDRTTa6V7eo7TTeEXqRyt58CKGzKau5V6AA2hj1THzhn5U5ZdfYP9mxLAzrBAkP6K"


def transfer_to_master(user_priv_key, amount):  # identical to withdraw function but it will have one withdrawal adress
    sender = Keypair.from_private_key(user_priv_key)
    receiver = PublicKey(master_wallet)
    amount = float(amount) - 0.001
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
    amount = float(amount) - 0.001
    amount = int(amount * 10 ** 9)
    instruction = transfer(
        from_public_key=sender.public_key,
        to_public_key=receiver,
        lamports=amount
    )
    transaction = Transaction(instructions=[instruction], signers=[sender])
    result = client.send_transaction(transaction)
    return True, result
