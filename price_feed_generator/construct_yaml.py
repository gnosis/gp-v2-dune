import csv
import json
from collections import defaultdict

import yaml


# Begin Hack
# This little block is a hack to get the address (as a number) to print without quotes.
class HexInt(int):
    pass


def representer(dumper, data):
    result = yaml.ScalarNode(
        'tag:yaml.org,2002:int',
        '0x{:040x}'.format(data)
    )
    return result


yaml.add_representer(HexInt, representer)


# End Hack

def load_coins(filepath: str) -> dict[str, list[dict]]:
    with open(filepath, 'r') as file:
        entries = json.loads(file.read())
        coin_dict = defaultdict(list)
        for entry in entries:
            if entry['type'] == 'token' and entry['is_active'] and not entry['is_new']:
                # only include ethereum tokens
                coin_dict[entry['symbol']].append(entry)
        return coin_dict


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

    found, res = 0, []
    for token in tokens:
        if token['symbol'] in coins:
            possible_tokens = coins[token['symbol']]
            if len(possible_tokens) == 1:
                coin_id = possible_tokens[0]['id']
                res.append({
                    # dune uses the snake case id as the name
                    'name': coin_id.replace('-', '_'),
                    'id': coin_id,
                    'symbol': token['symbol'],
                    'address': HexInt(int(token['address'], 16)),
                    'decimals': int(token['decimals']),
                })
                found += 1
            else:
                print("Token not uniquely identifiable!", token, len(possible_tokens))
        if found > 50:
            break

    with open('./data/result.yaml', 'w') as yaml_file:
        yaml.dump(res, yaml_file, default_flow_style=False, sort_keys=False)
