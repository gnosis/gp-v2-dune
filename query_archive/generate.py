from typing import Any

from jinjasql import JinjaSql


# TODO - use this as a unit test. The following returns same result as below.
#  query, bind_params = j.prepare_query(EXTENDED_TOKEN_LIST_TEMPLATE, params)
EXTENDED_TOKEN_LIST_TEMPLATE = '''
extended_token_list AS (
    SELECT symbol, decimals, contract_address
    FROM erc20.tokens
    -- Use this repo to fetch and format token data https://github.com/gnosis/gp-v2-dune
    UNION
    SELECT *
    FROM (VALUES
{{ missing_tokens }}
    ) as unlisted
)
'''


def open_raw_sql(filename: str) -> str:
    with open(filename, 'r') as sql_file:
        return sql_file.read()


def generate_query(filename: str, params: dict[str, Any]) -> str:
    template = open_raw_sql(filename)
    query, bind_params = j.prepare_query(template, params)
    return query % bind_params


if __name__ == "__main__":
    # TODO generate missing tokens dynamically by invoking TS script in this REPO
    missing_tokens = [
        "('LGB', 18, decode('21e783bcf445b515957a10e992ad3c8e9ff51288', 'hex'))",
        "('BYTES', 18, decode('7d647b1a0dcd5525e9c6b3d14be58f27674f8c95', 'hex'))"
    ]
    j = JinjaSql(param_style='pyformat')

    params = {
        'missing_tokens': ",\n".join(missing_tokens)
    }
    extended_token_list = generate_query(
        'sql/extended_token_list.jinja',
        params={
            'missing_tokens': ",\n".join(missing_tokens)
        }
    )

    trades_with_prices = generate_query(
        './sql/trades_with_prices.sql',
        params={
            # These result in missing chars date(2021, 3, 3) '2021-03-03',
            'from_date': "TO_DATE('2021/03/03', 'YYYY/MM/DD')",
            'extended_token_list': extended_token_list,
        }
    )

    trade_history = generate_query(
        './sql/trade_history.sql',
        params={
            'trades_with_prices': trades_with_prices
        }
    )

    with open('trade_history.gen.sql', 'w') as file:
        file.write(trade_history)
