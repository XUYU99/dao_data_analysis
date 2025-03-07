from dune_client.client import DuneClient
dune = DuneClient("TIsYkoRVCJL99pVPLcLHExujpdEGPi8u")
query_result = dune.get_latest_result(4801311)
print(query_result)
