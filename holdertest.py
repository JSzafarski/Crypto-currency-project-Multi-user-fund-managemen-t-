from requests import request

solscan_header = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MDY3NTM5ODAzOTQsImVtYWlsIjoic29sYmFieTMyNUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE3MDY3NTM5ODB9.Lp77APFLV-rOnNbDzc1ob43Vp-9-KpeMe_b-fiOQrr0',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36'
}


def get_holders():
    holder_list = request('GET',
                          "https://pro-api.solscan.io/v1.0/token/holders?tokenAddress"
                          "=mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ&limit=10&offset=0",
                          headers=solscan_header)
    holder_list_json = holder_list.json()
    return int(holder_list_json["total"])


print(get_holders())
