import numpy as np
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from time import time

# 全局变量存储测试准确率
model_test_accuracy = 0.9649  # 默认值，首次训练后更新
X_test = None
y_test = None
sc = None

def random_forest_train():
    global X_test, y_test, sc, model_test_accuracy
    
    # Importing the dataset
    dataset = pd.read_csv('Breast Cancer Data.csv')
    X = dataset.iloc[:, 2:32].values
    y = dataset.iloc[:, 1].values

    # Encoding categorical data
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder
    labelencoder_X_1 = LabelEncoder()
    y = labelencoder_X_1.fit_transform(y)

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    # 计算并保存测试准确率
    output = clf.predict(X_test)
    model_test_accuracy = accuracy_score(y_test, output)
    print("Model training completed. Test accuracy: ", model_test_accuracy)

    return clf

def randorm_forest_test(clf):
    t = time()
    output = clf.predict(X_test)
    acc = accuracy_score(y_test, output) 
    print("The accuracy of testing data: ",acc)
    print("The running time: ",time()-t)

def random_forest_predict(clf, inp):
    t = time()
    inp = sc.transform(inp)
    output = clf.predict(inp)
    acc = clf.predict_proba(inp)
    print("The running time: ",time()-t)

    return output, acc, time()-t

def get_model_accuracy():
    return model_test_accuracy