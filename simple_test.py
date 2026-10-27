import os
os.chdir('d:\\31905\\breast-cancer-detection-master')

from implementation import random_forest_train, random_forest_predict
import numpy as np
import pandas as pd

print('=== 预测概率测试 ===\n')

# 加载模型
print('1. 加载模型...')
clf = random_forest_train()
print('   模型加载完成\n')

# 读取数据集
dataset = pd.read_csv('Breast Cancer Data.csv')
X = dataset.iloc[:, 2:32].values

# 测试前10个样本
print('2. 测试前10个样本的预测：\n')
probabilities = []
for i in range(10):
    test_sample = X[i:i+1]
    out, acc, t = random_forest_predict(clf, test_sample)
    
    prob_benign = float(acc[0][0])
    prob_malignant = float(acc[0][1])
    
    probabilities.append((prob_benign, prob_malignant))
    
    print(f'   样本 {i+1}:')
    print(f'     结果: {"Malignant" if out[0] == 1 else "Benign"}')
    print(f'     良性概率: {prob_benign * 100:.2f}%')
    print(f'     恶性概率: {prob_malignant * 100:.2f}%')
    print()

# 检查概率是否有变化
print('3. 检查概率变化：\n')
benign_values = [p[0] for p in probabilities]
malignant_values = [p[1] for p in probabilities]

print(f'   良性概率范围: {min(benign_values) * 100:.2f}% - {max(benign_values) * 100:.2f}%')
print(f'   恶性概率范围: {min(malignant_values) * 100:.2f}% - {max(malignant_values) * 100:.2f}%')

if len(set(benign_values)) > 1:
    print('\n   ✓ 良性概率有变化 - 正常！')
else:
    print('\n   ✗ 警告：所有良性概率相同！')

if len(set(malignant_values)) > 1:
    print('   ✓ 恶性概率有变化 - 正常！')
else:
    print('   ✗ 警告：所有恶性概率相同！')
