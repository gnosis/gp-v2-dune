WITH
extended_token_list AS (
    SELECT symbol, decimals, contract_address
    FROM erc20.tokens
    -- Use this repo to fetch and format token data https://github.com/gnosis/gp-v2-dune
    UNION
    SELECT *
    FROM (VALUES
('LGB', 18, decode('21e783bcf445b515957a10e992ad3c8e9ff51288', 'hex')),
('BYTES', 18, decode('7d647b1a0dcd5525e9c6b3d14be58f27674f8c95', 'hex'))
    ) as unlisted
),

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
        AND p2.hour > TO_DATE('2021/03/03', 'YYYY/MM/DD') --! Deployment Date or other.
        AND date_trunc('hour', p2.hour) = date_trunc('hour', evt_block_time)
)

SELECT
    block_time,
    CONCAT('<a href="https://etherscan.io/address/', CONCAT('0x', ENCODE(owner, 'hex')), '" target="_blank">', CONCAT('0x', ENCODE(owner, 'hex')),  '</a>') as trader,
    sell_token,
    buy_token,
    units_sold,
    units_bought,
       -- We use sell value when possible and buy value when not
    (CASE
        WHEN sell_price IS NOT NULL THEN sell_price * units_sold
        WHEN sell_price IS NULL AND buy_price IS NOT NULL THEN buy_price * units_bought
        ELSE  -0.01
    END) as usd_value,
    fee,
    CONCAT('<a href="https://etherscan.io/tx/', CONCAT('0x', ENCODE(tx_hash, 'hex')), '" target="_blank">', CONCAT('0x', ENCODE(tx_hash, 'hex')),  '</a>') as transaction,
    CONCAT('<a href="https://gnosis-protocol.io/orders/', CONCAT('0x', ENCODE(order_uid, 'hex')), '" target="_blank">', CONCAT('0x', ENCODE(order_uid, 'hex')),  '</a>') as order_uid
FROM trades_with_prices
ORDER BY block_time DESC