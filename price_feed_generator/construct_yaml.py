import csv
import json
from collections import defaultdict


def load_coins(filepath: str) -> dict[str, list[dict]]:
    with open(filepath, 'r') as file:
        entries = json.loads(file.read())
        res = defaultdict(list)
        for entry in entries:
            res[entry['symbol']].append(entry)
        return res


def load_tokens(filepath: str):
    with open(filepath, newline='') as file:
        return list(csv.DictReader(file))


if __name__ == "__main__":
    coins = load_coins('data/coinpaprikacoins.json')
    tokens = load_tokens('data/tokens_without_prices.csv')

    print("Total unlisted tokens", len(tokens))
    found = 0
    for token in tokens:
        if token['symbol'] in coins:
            # print(token, coins[token['symbol']])
            if len(coins[token['symbol']]) == 1:
                found += 1
    print(found, "uniquely identifyable (by symbol) tokens in paprika list")
