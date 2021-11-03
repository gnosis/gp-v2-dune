import csv
import json

from collections import defaultdict


def load_coins(filepath: str) -> dict[str, list[dict]]:
    with open(filepath, 'r') as file:
        entries = json.loads(file.read())
        res = defaultdict(list)
        for entry in entries:
            if entry['type'] == 'token':
                # only include ethereum tokens
                res[entry['symbol']].append(entry)
        return res


def load_tokens(filepath: str):
    with open(filepath, newline='') as file:
        return list(csv.DictReader(file))


if __name__ == "__main__":
    coins = load_coins('data/coin-paprika.json')
    tokens = load_tokens('data/tokens-by-popularity.csv')

    tokens.sort(key=lambda entry: int(entry['popularity']), reverse=True)

    found, output = 0, ""
    for token in tokens:
        if token['symbol'] in coins:
            possible_tokens = coins[token['symbol']]
            if len(possible_tokens) == 1:
                possible_token = possible_tokens[0]
                if possible_token['is_active'] and not possible_token['is_new']:
                    # dune uses the snake case id as the name
                    token_name = possible_token['id'].replace('-', '_')
                    # TODO - use real object and dump to yaml with yaml library
                    output += f"- name: {token_name}\n  id: {possible_token['id']}\n  symbol: {token['symbol']}\n  address: {token['address']}\n  decimals: {token['decimals']}\n"""
                    found += 1
            else:
                print("Token not uniquely identifiable!", token, len(possible_tokens))
        if found > 50:
            break
    with open('./data/reduced-output.yaml', 'w') as out_file:
        out_file.write(output)
