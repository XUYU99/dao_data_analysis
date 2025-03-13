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


-- 获取aave所有提案的投票情况
SELECT
  dp.project AS project,             -- 项目名称
  dp.proposal_id AS proposal_id,     -- 提案 ID
  dv.voter_address AS voter_address, -- 投票者地址
  dv.votes AS votes                  -- 投票数量
FROM
  dao.proposals AS dp
JOIN
  dao.votes AS dv
ON
  dp.proposal_id = dv.proposal_id    -- 通过 proposal_id 连接两个表
WHERE
  dp.project = 'aave'                -- 正确的 WHERE 条件，筛选出 aave 项目
ORDER BY
  dp.project,                        -- 按项目名称排序
  dp.proposal_id,                    -- 按提案 ID 排序
  dv.voter_address,                  -- 按投票者地址排序
  dv.votes                          -- 按投票数量排序

  /* 关联投票记录，统计每个地址的投票次数 */
/* 查询每个地址的首次持币时间（以UNI代币为例） */
/* 关联投票记录，统计每个地址的投票次数 */
/* 查询每个地址的首次持币时间（以UNI代币为例） */
WITH first_hold AS (
  SELECT
    "to" AS address,
    MIN(block_time) AS first_hold_time
  FROM tokens.transfers
  WHERE
    contract_address = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 /* UNI代币合约地址 */
    AND to != 0x0000000000000000000000000000000000000000 /* 排除销毁地址 */
  GROUP BY
    1
)
SELECT
  fh.address,
  fh.first_hold_time,
  date_diff('second', fh.first_hold_time, CURRENT_TIMESTAMP) / 3600.0 AS hold_duration_hours,  -- 计算持币时长
  COUNT(univ.voter_address) AS vote_count                   -- 统计该地址的投票次数
FROM first_hold AS fh
JOIN uniswap_v3_ethereum.votes AS univ
  ON univ.voter_address = fh.address                         -- 根据地址关联投票记录
GROUP BY 1, 2


--计算每个地址在各个时间段内的加权持币时长
WITH balance_periods AS (
  SELECT
    address,                              -- 地址
    block_time,                           -- 余额快照时间
    balance,                              -- 当时的余额
    LAG(block_time) OVER (PARTITION BY address ORDER BY block_time) AS pre_time,
    LAG(balance) OVER (PARTITION BY address ORDER BY block_time) AS pre_balance
  FROM tokens_ethereum.balances
  WHERE token_address = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984  -- UNI代币合约地址
   AND address = 0xffff610b80fb89654e91cca2e8504aa629daf22c
),

hold_balance_periods AS (
  SELECT
    address,                              -- 地址
    block_time,                           -- 余额快照时间
    balance,                              -- 当时的余额
    pre_time,
    pre_balance,
    date_diff('second', pre_time, block_time) / 3600.0 AS hold_duration_hours,
    date_diff('second', pre_time, block_time) / 3600.0 * pre_balance AS hold_weight_before_last
  FROM balance_periods
)

SELECT
    address,
    SUM(
      hold_weight_before_last
    ) AS hold_weight
  FROM hold_balance_periods
  GROUP BY address

-- 计算各个地址总的持有代币权重
WITH balance_periods AS (
  SELECT
    address,                              -- 地址
    block_time,                           -- 余额快照时间
    balance,                              -- 当时的余额
    LAG(block_time) OVER (PARTITION BY address ORDER BY block_time) AS pre_time,
    LAG(balance) OVER (PARTITION BY address ORDER BY block_time) AS pre_balance
  FROM tokens_ethereum.balances
  WHERE token_address = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984  -- UNI代币合约地址
),

/* 3. 计算每个地址在各个时间段内的加权持币时长（不包括最后一期） */
hold_balance_periods AS (
  SELECT
    address,                              -- 地址
    block_time,                           -- 余额快照时间
    balance,                              -- 当时的余额
    pre_time,
    pre_balance,
    date_diff('second', pre_time, block_time) / 3600.0 AS hold_duration_hours,
    date_diff('second', pre_time, block_time) / 3600.0 * pre_balance AS hold_weight_before_last
  FROM balance_periods
),
/* 4. 计算每个地址总的持有代币权重（不包括最后一期） */
hold_weight_periods AS (
  SELECT
    address,
    SUM(
      hold_weight_before_last
    ) AS hold_weight
  FROM hold_balance_periods
  GROUP BY address
),

/* 5. 计算每个地址 最后一期 加权持币时长 */
latest_hold_weight_period AS (
WITH latest_balances AS (
  SELECT
    address,                                          -- 地址
    block_time,                                       -- 余额快照时间
    balance,                                          -- 当时的余额
    ROW_NUMBER() OVER (PARTITION BY address ORDER BY block_time DESC) AS rn
  FROM tokens_ethereum.balances
  WHERE token_address = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984  -- UNI代币合约地址，用单引号括起
)
SELECT
  address,
  block_time,
  balance,
  date_diff('second', block_time, CURRENT_TIMESTAMP) / 3600.0 AS latest_hold_duration_hours,  -- 计算持币时长（单位：小时）
  (date_diff('second', block_time, CURRENT_TIMESTAMP) / 3600.0) * balance AS latest_hold_weight  -- 持币时长乘以余额得到的权重
FROM latest_balances
WHERE rn = 1
)

/* 6. 汇总每个地址的总加权持币时长 */
  SELECT
    hwp.address,
    hwp.hold_weight + lhwp.latest_hold_weight AS tatal_hold_weight
  FROM latest_hold_weight_period lhwp
  LEFT JOIN hold_weight_periods hwp ON hwp.address = lhwp.address
```

| blockchain | block_number | block_time       | address                                    | token_address                              | token_standard | balance_raw         | balance | token_symbol | token_id | collection_name |
| ---------- | ------------ | ---------------- | ------------------------------------------ | ------------------------------------------ | -------------- | ------------------- | ------- | ------------ | -------- | --------------- |
| ethereum   | 15151435     | 2022-07-16 03:54 | 0x018c1ccdda1857fc79a46c4d3b2db57a6bb76302 | 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 | erc20          | 1000000000000000000 | 1       | UNI          |          |                 |

scripts02 文件夹
hold_percentage.py --开发 Python 脚本分析治理代币集中度，计算前 10%地址的投票权重占比
