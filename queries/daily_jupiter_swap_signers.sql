-- Distinct signers of intended swaps recorded by Dune's curated Jupiter table.
-- "Returning" means the signer also swapped during the preceding seven days.
-- Fee-payer overlap is an address intersection, not a count of people.
WITH jupiter_signers AS (
    SELECT DISTINCT
        CAST(block_time AS DATE) AS activity_date,
        tx_signer
    FROM jupiter_solana.aggregator_swaps
    WHERE block_month >= CAST(
            DATE_TRUNC('month', CURRENT_DATE - INTERVAL '14' DAY) AS DATE
        )
      AND block_time >= CAST(
            CURRENT_DATE - INTERVAL '14' DAY AS TIMESTAMP
        )
      AND block_time < CAST(CURRENT_DATE AS TIMESTAMP)
      AND tx_signer IS NOT NULL
),
fee_payers AS (
    SELECT DISTINCT
        block_date AS activity_date,
        signer AS fee_payer
    FROM solana.transactions
    WHERE block_date >= CURRENT_DATE - INTERVAL '7' DAY
      AND block_date < CURRENT_DATE
      AND success = TRUE
),
output_days AS (
    SELECT DISTINCT activity_date
    FROM jupiter_signers
    WHERE activity_date >= CURRENT_DATE - INTERVAL '7' DAY
      AND activity_date < CURRENT_DATE
)
SELECT
    days.activity_date,
    COUNT(DISTINCT current_users.tx_signer) AS unique_jupiter_swap_signers,
    COUNT(DISTINCT CASE
        WHEN fee_payers.fee_payer IS NOT NULL THEN current_users.tx_signer
    END) AS jupiter_fee_payer_overlap,
    COUNT(DISTINCT CASE
        WHEN prior.tx_signer IS NOT NULL THEN current_users.tx_signer
    END) AS returning_jupiter_swap_signers
FROM output_days AS days
LEFT JOIN jupiter_signers AS current_users
    ON current_users.activity_date = days.activity_date
LEFT JOIN fee_payers
    ON fee_payers.activity_date = current_users.activity_date
   AND fee_payers.fee_payer = current_users.tx_signer
LEFT JOIN jupiter_signers AS prior
    ON prior.tx_signer = current_users.tx_signer
   AND prior.activity_date BETWEEN
       current_users.activity_date - INTERVAL '7' DAY
       AND current_users.activity_date - INTERVAL '1' DAY
GROUP BY 1
ORDER BY 1;
