import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import joblib

# 1. 数据处理
# 读取 CSV 数据
df = pd.read_csv('dune_voter_hold_vote_200.csv')
# 删除包含 NaN 的整行数据
df.dropna(inplace=True)
# 选择 'balance' 作为特征，'uni_vote_count' 作为标签
X = df[['balance']]
y = df['uni_vote_count']
# 划分训练集与测试集（80% 训练，20% 测试）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 模型训练（使用随机森林回归）
model = RandomForestRegressor(n_estimators=200, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 3. 模型评估
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 打印模型评估结果
print("MSE:", mse)
print("RMSE:", rmse)
print("MAE:", mae)
print("R^2:", r2)

# 4. 可视化 y_test 与 y_pred 的对比图
plt.figure(figsize=(8, 6))
plt.scatter(range(len(y_test)), y_test, label='Actual')
plt.scatter(range(len(y_test)), y_pred, label='Predicted')
plt.legend()
plt.title("Actual vs Predicted values")
plt.xlabel("Sample index")
plt.ylabel("uni_vote_count")
plt.show()

# 5. 保存模型到 dao_rf_model.pkl
joblib.dump(model, 'dao_rf_model.pkl')
