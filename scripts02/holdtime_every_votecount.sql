/* 1. 提取 Aave 项目的提案投票数据 */
WITH vote_count_table AS (
  SELECT
    dv.project AS project,           -- 项目名称
    dv.voter_address AS voter_address, -- 投票者地址
    COUNT(dv.voter_address) AS vote_count      -- 投票数量
  FROM dao.votes AS dv
  WHERE dv.project = 'uniswap'            -- 筛选项目
  GROUP BY dv.project,dv.voter_address
),

/* 2. 从 tokens_ethereum.balances 表中获取 UNI 代币的持币快照，计算每个地址各个快照之间的时间段 */
 balance_periods AS (
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
),

/* 6. 汇总每个地址的总加权持币时长 */
total_hold AS (
SELECT
    hwp.address,
    hwp.hold_weight + lhwp.latest_hold_weight AS total_hold_weight
  FROM latest_hold_weight_period lhwp
  LEFT JOIN hold_weight_periods hwp ON hwp.address = lhwp.address
)

-- 7. 最后将投票数据与每个地址的持币情况关联
SELECT
   vct.voter_address,
   vct.vote_count,
   th.total_hold_weight  -- 该地址加权持币时长（小时）
FROM vote_count_table vct
LEFT JOIN total_hold th
  ON vct.voter_address = th.address
ORDER BY th.total_hold_weight