from jinjasql import JinjaSql

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


if __name__ == "__main__":
    extended_token_list_template = open_raw_sql('./sql/extended_token_list.sql')
    # TODO generate missing tokens with TS script in this REPO
    missing_tokens = [
        "('LGB', 18, decode('21e783bcf445b515957a10e992ad3c8e9ff51288', 'hex'))",
        "('BYTES', 18, decode('7d647b1a0dcd5525e9c6b3d14be58f27674f8c95', 'hex'))"
    ]
    params = {
        'missing_tokens': ",\n".join(missing_tokens)
    }
    j = JinjaSql(param_style='pyformat')
    # query, bind_params = j.prepare_query(EXTENDED_TOKEN_LIST_TEMPLATE, params)
    query, bind_params = j.prepare_query(EXTENDED_TOKEN_LIST_TEMPLATE, params)
    print(query % bind_params)
