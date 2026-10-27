import sys
import os
os.chdir('d:\\31905\\breast-cancer-detection-master')

from implementation import random_forest_train, random_forest_predict
import numpy as np

print('=== 预测系统测试 ===\n')

# 加载模型
print('1. 正在加载模型...')
clf = random_forest_train()
print('   ✓ 模型加载完成\n')

# 读取数据集获取一些测试样本
import pandas as pd
dataset = pd.read_csv('Breast Cancer Data.csv')
X = dataset.iloc[:, 2:32].values
y = dataset.iloc[:, 1].values

# 测试多个不同样本
print('2. 测试不同样本的预测结果：\n')
for i in range(5):
    test_sample = X[i:i+1]
    print(f'   样本 {i+1}:')
    
    out, acc, t = random_forest_predict(clf, test_sample)
    prob_benign = float(acc[0][0])
    prob_malignant = float(acc[0][1])
    
    print(f'   预测结果: {"Malignant" if out[0] == 1 else "Benign"}')
    print(f'   良性概率: {prob_benign * 100:.2f}%')
    print(f'   恶性概率: {prob_malignant * 100:.2f}%')
    print('   ' + '-'*40)

print('\n3. 测试不同的特征值：\n')
# 创建一些极端测试数据
test_cases = [
    np.random.randn(1, 30) * 5,  # 极端负值
    np.random.randn(1, 30) * 10,  # 极端值
    np.abs(np.random.randn(1, 30) * 3)  # 全正值
]

for i, test in enumerate(test_cases):
    out, acc, t = random_forest_predict(clf, test)
    prob_benign = float(acc[0][0])
    prob_malignant = float(acc[0][1])
    
    print(f'   测试 {i+1} (随机特征):')
    print(f'   预测结果: {"Malignant" if out[0] == 1 else "Benign"}')
    print(f'   良性概率: {prob_benign * 100:.2f}%')
    print(f'   恶性概率: {prob_malignant * 100:.2f}%')
    print('   ' + '-'*40)
