import csv
import json
import yaml
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
    output = ""
    for token in tokens:
        if token['symbol'] in coins:
            # print(token, coins[token['symbol']])
            possible_coins = coins[token['symbol']]
            if len(possible_coins) == 1:
                coin = possible_coins[0]
                if coin['is_active'] == True and coin['is_new'] == False:
                    # For some reason dune uses the snake case id as the name
                    coin_name = coin['id'].replace('-', '_')
                    output += f"- name: {coin_name}\n  id: {coin['id']}\n  symbol: {token['symbol']}\n  address: {token['address']}\n  decimals: {token['decimals']}\n"""
                    found += 1
    print(found, "uniquely identifyable (by symbol) tokens in paprika list")
    # print(output)
    with open('./data/output.yaml', 'w') as out_file:
        out_file.write(output)
    
