import pandas as pd
from web3 import Web3

# 设置 Ethereum 节点的 HTTP Provider（例如 Infura 节点）
provider_url = "https://mainnet.infura.io/v3/b6826ba6d4fb46faa9e127277ed1ef25"
web3 = Web3(Web3.HTTPProvider(provider_url))

# 检查连接是否成功
if not web3.is_connected():
    raise Exception("无法连接到 Ethereum 节点，请检查 provider_url 或网络设置。")

# 读取包含 voter_address 列的 CSV 文件（请替换为你的文件路径）
file_path = "dune_voter_500.csv"
df = pd.read_csv(file_path)

address = "0x408ed6354d4973f66138c91495f2f2fcbd8724c3"
# 0x683a4F9915D6216f73d6Df50151725036bD26C02
# 0x553F674dD7D102ad79C644103974a1cc53b62Ac2
address2 = "0xe409121c12E6d748d29c132BE68552Bdc8162a81"
address = web3.to_checksum_address(address)
# print(f"地址: {address} 类型: {address}")
code = web3.eth.get_code(address)
print(f"地址: {address} 类型: {code}")

address2 = web3.to_checksum_address(address2)
code2 = web3.eth.get_code(address2)
print(f"地址: {address2} 类型: {code2}")


# 定义函数：判断地址是合约地址还是个人地址
# def get_address_type(address):
#     code = web3.eth.get_code(address)
#     # 如果返回的字节码为 "0x" 则说明没有代码，即为个人地址（EOA），否则为合约地址
#     print(f"地址: {address} 类型: {address_type}")

# for address in df['voter_address']:
#     code = web3.eth.get_code(address)
#     print(f"地址: {address} 类型: {code.hex()}")
    

# 对 voter_address 列中的每个地址进行判断，并新增一列 address_type 保存结果
# df["address_type"] = df["voter_address"].apply(get_address_type)

# # 输出前几行结果
# print(df.head())

# 如有需要，也可以将结果保存到新的 CSV 文件中
# df.to_csv("voter_data_with_address_type.csv", index=False)
