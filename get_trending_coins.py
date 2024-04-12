from requests import request
from bitcoin_value import currency

header = {
    "User-Agent": " ".join(
        [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/113.0.0.0 Safari/537.36",
        ]
    )
}
mbtc_pair = "ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc"


def get_market_cap(token):
    print(token)
    token_result = request('GET',
                           f"https://api.dexscreener.com/latest/dex/pairs/solana/{token}",
                           headers=header)
    return token_result.json()["pairs"][0]["fdv"]


# make this so it adds by itself?
big_sol_coins = {  # use the pair address ser
    "wif": "EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx",
    "bonk": "3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1",
    "harambe": "2BJKy9pnzTDvMPdHJhv8qbWejKiLzebD7i2taTyJxAze",
    "bome": "DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt",
    "mew": "879F697iuDJGMevRkRcnW21fcXiAeLJK1ffsw2ATebce",
    "boden": "6UYbX1x8YUcFj8YstPYiZByG7uQzAq2s46ZWphUMkjg5",
    "slerf": "AgFnRLUScRD2E4nWQxW73hdbSN7eKEUb2jHX7tx9YTYc",
    "popcat": "FRhB8L7Y9Qq41qZXYLtC2nw8An1RJfLLxRF2x9RwLLMo",
    "ansom": "ADwQhgVS41xbMSDeHbd9nDiGnky1y2CtgG4ctVcoUv1R",
    "mumu": "FvMZrD1qC66Zw8VPrW15xN1N5owUPqpQgNQ5oH18mR4E",
    "wynn": "EcHXwaRp26ChgAsmfdrVki44XRr8tibwJ17DbsUTiJGe",
    "duko": "BGS69Ju7DRRVxw9b2B5TnrMLzVdJcscV8UtKywqNsgwx",
    "wen": "7BZzoP3QB2zK3R7WqRzjS5fpeeErgdy3HGzxXrN97aEY",
    "catwif": "J37wzATp3rvAh1y1tq3Y4M3c9Rg1LJSA4YDDXBm9t3x2",
    "myro": "5WGYajM1xtLy3QrLHGSX4YPwsso3jrjEsbU1VivUErzk",
    "hodl": "6FcHJg65kNUa3DPmG5HfNAh3BBXcHoAYGLxMAzpM2Yyf",
    "pups": "DLXrjEzjgm7u35MTRbpG38CcBAD2JjRCRhwCszd6bKwf",
    "ponke" :"5uTwG3y3F5cx4YkodgTjWEHDrX5HDKZ5bZZ72x8eQ6zE"
}


def convert_to_standard(token_input):
    lower_case_string = token_input.lower()
    lower_case_string = lower_case_string.replace("$", "")
    return lower_case_string


def compare(token):
    standard_token_version = convert_to_standard(token)
    if standard_token_version in big_sol_coins:
        string_builder = ""
        mbtc_fdv = float(get_market_cap(mbtc_pair))
        token_fdv = float(get_market_cap(big_sol_coins[standard_token_version]))
        ratio = int(token_fdv / mbtc_fdv)
        if ratio < 1:
            string_builder = "decrease"
        else:
            string_builder = "increase"
        ratio = str(f"{ratio}").replace(".", ",")
        return f"To reach the market cap of *{standard_token_version}*, Mini Bitcoin would have to *{string_builder}* by *{ratio}x*"
        # compare market cap x's
    elif standard_token_version == "bitcoin":
        btc_mc = currency("USD") * 21000000
        string_builder = ""
        mbtc_fdv = float(get_market_cap(mbtc_pair))
        ratio = int(btc_mc / mbtc_fdv)
        if ratio < 1:
            string_builder = "decrease"
        else:
            string_builder = "increase"
        ratio = str(f"{ratio}").replace(".", "\\.")
        return f"To reach the market cap of *{standard_token_version}*, Mini Bitcoin would have to *{string_builder}* by *{ratio}x*"
    else:
        return False
