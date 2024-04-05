# whales movements
# provide info how much is left in lp pool every 10 minutes of if someone does command
from requests import request

solscan_header = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MDY3NTM5ODAzOTQsImVtYWlsIjoic29sYmFieTMyNUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE3MDY3NTM5ODB9.Lp77APFLV-rOnNbDzc1ob43Vp-9-KpeMe_b-fiOQrr0',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36'
}


def whale_alert():
    temp_txHash_array = []
    token_address = "mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"
    spl_transfers = request('GET',
                            "https://pro-api.solscan.io/v1.0/token/transfer?tokenAddress=" + str(
                                token_address) + "&limit=10&offset=0",
                            headers=solscan_header)
    spl_transfers_json = spl_transfers.json()
    for transfer in spl_transfers_json["items"]:
        if transfer["txHash"] not in temp_txHash_array:
            temp_txHash_array.append(transfer["txHash"])
            if float(transfer["amount"]) / 10 ** 11 > 10:
                transfer_amount = float(transfer["amount"]) / 10 ** 11
                from_address = transfer["sourceOwnerAccount"]
                to_address = transfer["destOwnerAccount"]
                print(F"Whale Alert! {transfer_amount} mBTC Transferred From {from_address} to {to_address}")


whale_alert()
