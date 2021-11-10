SELECT
    evt_block_time as date_time,
    evt_tx_hash as txHash,
    owner,
    "orderUid" as order_uid,
    (CASE
        WHEN tokens.symbol IS NULL THEN TEXT(trades."sellToken")
        ELSE tokens.symbol
    END) sell_token,
    "buyToken",
    ("sellAmount" - "feeAmount")/ pow(10,tokens.decimals) as units_sold,
    "buyAmount",
    "feeAmount" / pow(10,tokens.decimals) as fee,
    median_price as sell_price
FROM gnosis_protocol_v2."GPv2Settlement_evt_Trade" trades
LEFT OUTER JOIN extended_token_list tokens
    ON trades."sellToken" = tokens.contract_address
LEFT OUTER JOIN dex.view_token_prices as p
    ON trades."sellToken" = p.contract_address
    AND p.hour > TO_DATE('2021/03/03', 'YYYY/MM/DD') --! Deployment Date
    AND date_trunc('hour', p.hour) = date_trunc('hour', evt_block_time)