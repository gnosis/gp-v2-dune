{{ extended_token_list }},

trades_with_prices AS (
    SELECT
        evt_block_time as block_time,
        evt_tx_hash as tx_hash,
        owner,
        "orderUid" as order_uid,
        (CASE
            WHEN sell_token.symbol IS NULL THEN TEXT(trades."sellToken")
            ELSE sell_token.symbol
        END) sell_token,
        (CASE
            WHEN buy_token.symbol IS NULL THEN TEXT(trades."buyToken")
            ELSE buy_token.symbol
        END) as buy_token,
        ("sellAmount" - "feeAmount")/ pow(10, sell_token.decimals) as units_sold,
        p1.median_price as sell_price,
        "buyAmount" / pow(10, buy_token.decimals) as units_bought,
        p2.median_price as buy_price,
        "feeAmount" / pow(10, sell_token.decimals) as fee
    FROM gnosis_protocol_v2."GPv2Settlement_evt_Trade" as trades
    LEFT OUTER JOIN extended_token_list sell_token
        ON trades."sellToken" = sell_token.contract_address
    LEFT OUTER JOIN dex.view_token_prices as p1
        ON trades."sellToken" = p1.contract_address
        AND p1.hour > TO_DATE('2021/03/03', 'YYYY/MM/DD') --! Deployment Date
        AND date_trunc('hour', p1.hour) = date_trunc('hour', evt_block_time)
    LEFT OUTER JOIN extended_token_list buy_token --! Could also put jinja params here
        ON trades."buyToken" = buy_token.contract_address
    LEFT OUTER JOIN dex.view_token_prices as p2
        ON p2.contract_address = (
                CASE
                    WHEN trades."buyToken" = '\xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                    THEN '\xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                    ELSE trades."buyToken"
                END)
        AND p2.hour > {{ from_date }} --! Deployment Date or other.
        AND date_trunc('hour', p2.hour) = date_trunc('hour', evt_block_time)
)
