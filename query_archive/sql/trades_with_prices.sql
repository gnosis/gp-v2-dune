SELECT
    date_time,
    txHash,
    owner,
    order_uid,
    sell_token,
    (CASE
        WHEN tokens.symbol IS NULL THEN TEXT(trades."buyToken")
        ELSE tokens.symbol
    END) as buy_token,
    units_sold,
    sell_price,
    "buyAmount" / pow(10,tokens.decimals) as units_bought,
    median_price as buy_price,
    fee
FROM trades_with_sell_tokens_and_sell_price as trades
LEFT OUTER JOIN extended_token_list tokens
    ON trades."buyToken" = tokens.contract_address
LEFT OUTER JOIN dex.view_token_prices as p
    ON p.contract_address = (
            CASE
                WHEN trades."buyToken" = '\xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee' THEN '\xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                ELSE trades."buyToken"
            END)
    AND p.hour > TO_DATE('2021/03/03', 'YYYY/MM/DD') --! Deployment Date
    AND date_trunc('hour', p.hour) = date_trunc('hour', date_time)