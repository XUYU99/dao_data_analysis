import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 读取 DAO 治理数据
data = pd.read_csv("dune_voter_hold_vote_500.csv")

# 删除包含 NaN 的整行数据
data_cleaned = data.dropna()

# 选择特征和标签
X = data[['balance']]
y = data['uni_vote_count']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练 XGBoost 模型
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, max_depth=5)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 计算评估指标
mse = mean_squared_error(y_test, y_pred)  # 均方误差（MSE）
rmse = np.sqrt(mse)  # 均方根误差（RMSE）
mae = mean_absolute_error(y_test, y_pred)  # 平均绝对误差（MAE）
r2 = r2_score(y_test, y_pred)  # R² 决定系数（模型拟合度）

# 输出评估结果
print(f"模型评估结果：")
print(f"均方误差 (MSE): {mse:.4f}")
print(f"均方根误差 (RMSE): {rmse:.4f}")
print(f"平均绝对误差 (MAE): {mae:.4f}")
print(f"决定系数 (R²): {r2:.4f}")

# 可视化预测结果 vs. 真实值
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='blue', label="forecast_value")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], '--', color='red', label="Ideal data")
plt.xlabel("real vote_count (y_test)")
plt.ylabel("forecast vote_count (y_pred)")
plt.title("XGBoost forecast vs. real")
plt.legend()
plt.show()

# 保存模型
model.save_model("dao_gov_model.json")
