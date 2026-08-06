SELECT
    block_date AS activity_date,
    COUNT(DISTINCT signer_address) AS unique_successful_signers
FROM solana.transactions
CROSS JOIN UNNEST(signers) AS signer_accounts(signer_address)
WHERE block_date >= CURRENT_DATE - INTERVAL '7' DAY
  AND block_date < CURRENT_DATE
  AND success = TRUE
GROUP BY 1
ORDER BY 1;
