from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair

mint = Pubkey.from_string("Bc4itdH5eAJU2WN9h7uSZ8i9RZXSbNrVdUkaedFTHyDc")
program_id = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")

privkey = '4HjSgpCQML37Xw9Vo7jjnJGi7yKSRq88SuQUBVhAMfDxHZxmcpj5XYNCQb3TkU7vV7AxiHP5dEYJBLWBvmKZXZoN'
key_pair = Keypair.from_base58_string(privkey)

solana_client = Client("https://mainnet.helius-rpc.com/?api-key=f61ec600-eb2e-492c-b5ca-5c6393d1b7e1")
spl_client = Token(conn=solana_client, pubkey=mint, program_id=program_id, payer=key_pair)

source = Pubkey.from_string('G12Gw8DWHLL4ADUsumZTh2AsvVCpWJ6whpPmLYP1x8px')
dest = Pubkey.from_string('65WPcFptr5ivMBVkvY2crqu9p2MAta9SwzQQDuYXWpFj')

source_token_account = spl_client.create_associated_token_account(owner=source, skip_confirmation=False,
                                                                  recent_blockhash=None)

dest_token_account = spl_client.create_associated_token_account(owner=dest, skip_confirmation=False,
                                                                recent_blockhash=None)

amount = 500000000

transaction = spl_client.transfer(source=source_token_account, dest=dest_token_account, owner=key_pair,
                                  amount=int(float(amount)), multi_signers=None, opts=None,
                                  recent_blockhash=None)
print(transaction)
