WITH
{{ trades_with_prices }}

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
