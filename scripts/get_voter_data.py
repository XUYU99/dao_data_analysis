from dune_client.client import DuneClient
dune = DuneClient("TIsYkoRVCJL99pVPLcLHExujpdEGPi8u")
query_result = dune.get_latest_result(4801311)
print(query_result)

# 不重复随机获取 500 个投票者信息
    # SELECT voter_address
    # FROM dao.votes
    # GROUP BY voter_address
    # ORDER BY RANDOM()
    # LIMIT 500