import pandas as pd
from dune_client.client import DuneClient

# 不重复随机获取 500 个投票者信息
    # SELECT voter_address
    # FROM dao.votes
    # GROUP BY voter_address
    # ORDER BY RANDOM()
    # LIMIT 500
    
# 初始化 DuneClient
dune = DuneClient("TIsYkoRVCJL99pVPLcLHExujpdEGPi8u")

# 获取查询结果
query_result = dune.get_latest_result(4801311)

# 提取数据
if hasattr(query_result, 'result') and hasattr(query_result.result, 'rows'):
    data = query_result.result.rows  # 获取结果中的行数据
    df = pd.DataFrame(data)  # 转换为 DataFrame

    # 保存为 CSV
    df.to_csv("dune_voter_votedata_500.csv", index=False, encoding='utf-8')

    print("数据已成功保存为 dune_voter_votedata_500.csv")
else:
    print("查询结果格式不符合预期:", query_result)