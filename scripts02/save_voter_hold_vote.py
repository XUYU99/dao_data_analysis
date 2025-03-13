import pandas as pd
from dune_client.client import DuneClient
    
# 初始化 DuneClient
dune = DuneClient("8n5Z9DUxFvaFXZQiDxkQ8W3OGFtbOLtM")

# 获取查询结果
query_result = dune.get_latest_result(4844760)

# 提取数据
if hasattr(query_result, 'result') and hasattr(query_result.result, 'rows'):
    data = query_result.result.rows  # 获取结果中的行数据
    df = pd.DataFrame(data)  # 转换为 DataFrame

    # 保存为 CSV
    df.to_csv("uniswap_holdweight_votecount.csv", index=False, encoding='utf-8')

    print("数据已成功保存为 uniswap_holdweight_votecount.csv")
else:
    print("查询结果格式不符合预期:", query_result)




