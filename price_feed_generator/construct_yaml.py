import csv
import json
from collections import defaultdict

import yaml


def load_coins(filepath: str) -> dict[str, list[dict]]:
    with open(filepath, 'r') as file:
        entries = json.loads(file.read())
        res = defaultdict(list)
        for entry in entries:
            if entry['type'] == 'token' and entry['is_active'] and not entry['is_new']:
                # only include ethereum tokens
                res[entry['symbol']].append(entry)
        return res


def load_tokens(filepath: str) -> list[dict]:
    with open(filepath, newline='') as file:
        return list(csv.DictReader(file))


if __name__ == "__main__":
    coins = load_coins('data/coin-paprika.json')
    # Fetch tokens orders by descending, popularity
    tokens = sorted(
        load_tokens('data/tokens-by-popularity.csv'),
        key=lambda entry: int(entry['popularity']),
        reverse=True
    )

    found, output, res = 0, "", []
    for token in tokens:
        if token['symbol'] in coins:
            possible_tokens = coins[token['symbol']]
            if len(possible_tokens) == 1:
                coin_id = possible_tokens[0]['id']
                # dune uses the snake case id as the name
                name = coin_id.replace('-', '_')
                # TODO - use real object and dump to yaml with yaml library
                output += f"- name: {name}\n  id: {coin_id}\n  symbol: {token['symbol']}\n  address: {token['address']}\n  decimals: {token['decimals']}\n"""
                res.append({
                    'name': name,
                    'id': coin_id,
                    'symbol': token['symbol'],
                    'address': token['address'],
                    'decimals': int(token['decimals']),
                })
                found += 1
            else:
                print("Token not uniquely identifiable!", token, len(possible_tokens))
        if found > 50:
            break
    with open('./data/reduced-output.yaml', 'w') as out_file:
        out_file.write(output)

    # TODO - the problem with this is that the token address has quotes on the output.
    with open('./data/result.yml', 'w') as yaml_file:
        yaml.dump(res, yaml_file, default_flow_style=False)
