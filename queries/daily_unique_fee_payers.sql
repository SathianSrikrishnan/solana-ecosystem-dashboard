-- Distinct fee-paying addresses on successful non-vote Solana transactions.
-- Dune's solana.transactions table excludes validator vote transactions.
-- The current UTC day is excluded because it is still incomplete.
SELECT
    block_date AS activity_date,
    COUNT(DISTINCT signer) AS unique_fee_payers
FROM solana.transactions
WHERE block_date >= CURRENT_DATE - INTERVAL '7' DAY
  AND block_date < CURRENT_DATE
  AND success = TRUE
GROUP BY 1
ORDER BY 1;
