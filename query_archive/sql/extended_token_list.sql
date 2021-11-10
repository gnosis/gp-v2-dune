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