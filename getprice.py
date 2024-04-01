from requests import request

header = {
    "User-Agent": " ".join(
        [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/113.0.0.0 Safari/537.36",
        ]
    )
}


def get_price():
    token_address = "bewtdnb34l8lceya2ff1cgph3gjwfdgjcqyqza94uat1"  # change to mini btc later
    token_result = request('GET',
                           f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}",
                           headers=header)
    return token_result.json()["pairs"][0]["priceUsd"]



