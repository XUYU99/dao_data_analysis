from web3 import Web3

# 连接到以太坊主网（使用你的 RPC URL）
rpc_url = "https://sepolia.infura.io/v3/b6826ba6d4fb46faa9e127277ed1ef25"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# 指定交易哈希
tx_hash = "0x37eaa21a4c4c8bf42f02d2ad7a4c4ec1b4ea4c4dedcfd7ad1c45045d270409b8"
address = "0x683a4F9915D6216f73d6Df50151725036bD26C02"
address2 = "0xE283850eae553f77D7b6E5dd1F0b5cC9E51951ca"
# 获取交易信息
code = web3.eth.get_code(address2)

# 打印返回结果（使用 .hex() 方法转换为十六进制字符串）
print("Address", address, "code:", code.hex())

