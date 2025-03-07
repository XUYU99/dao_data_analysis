```sql
-- 随机获取 500 个投票者信息
SELECT *
FROM dao.votes
ORDER BY RANDOM()
LIMIT 500

-- 随机选取 500 个投票地址，并统计它们在不同 project（项目）中的投票次数
WITH voter_address_table AS (
    SELECT voter_address
    FROM dao.votes
    ORDER BY RANDOM()
    LIMIT 500
)
SELECT
    v.project,                 -- 统计不同项目的投票情况
    v.voter_address,
    COUNT(*) AS vote_count
FROM dao.votes v
JOIN voter_address_table vat
    ON v.voter_address = vat.voter_address
GROUP BY v.project, v.voter_address   -- 按 project 和 voter_address 统计
ORDER BY voter_address, vote_count DESC

-- 获取投票者的UNI代币持有量
SELECT
    *
FROM tokens_ethereum.balances
where token_address =0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
and address = 0x018c1ccdda1857fc79a46c4d3b2db57a6bb76302

test
SELECT
    *
FROM tokens_ethereum.balances
where token_address =0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
order by block_number DESC
limit 20


--
WITH voter_address_table AS (
    -- 随机选取 500 个投票人
    SELECT voter_address
    FROM dao.votes
    ORDER BY RANDOM()
    LIMIT 500
)
SELECT
    v.project,                 -- 统计不同项目的投票情况
    v.voter_address,
    COUNT(*) AS vote_count,
    balance -- UNI 代币持有量（转换为人类可读格式）
FROM dao.votes v
JOIN voter_address_table vat
    ON v.voter_address = vat.voter_address
LEFT JOIN tokens_ethereum.balances tokens_balance  -- 关联查询 UNI 代币持有量
    ON v.voter_address = tokens_balance.token_address
    AND tokens_balance.token_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 -- Uniswap (UNI) 代币地址
GROUP BY v.project, v.voter_address, tokens_balance.balance
ORDER BY v.voter_address, vote_count DESC
```

| blockchain | block_number | block_time       | address                                    | token_address                              | token_standard | balance_raw         | balance | token_symbol | token_id | collection_name |
| ---------- | ------------ | ---------------- | ------------------------------------------ | ------------------------------------------ | -------------- | ------------------- | ------- | ------------ | -------- | --------------- |
| ethereum   | 15151435     | 2022-07-16 03:54 | 0x018c1ccdda1857fc79a46c4d3b2db57a6bb76302 | 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 | erc20          | 1000000000000000000 | 1       | UNI          |          |                 |
