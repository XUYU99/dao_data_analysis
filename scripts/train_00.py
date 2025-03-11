import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 读取 DAO 治理数据
data = pd.read_csv("dao_governance_data.csv")

# 选择特征和标签
X = data[['投票次数', '持币量', '持币时间', '贡献度', 'DAO_投票模式']]
y = data['治理权转换比例']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练 XGBoost 模型
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, max_depth=5)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pred)
print(f"模型均方误差: {mse}")

# 保存模型
model.save_model("dao_gov_model.json")