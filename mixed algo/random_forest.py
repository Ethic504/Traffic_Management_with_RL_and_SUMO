# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 09:49:12 2020

@author: lappy
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('action_list_q_learning.csv')
# print(df.info())
# print(df.shape)
# print(df.columns.values)

X = df[["Time","Wate","Reward"]]    # independent variable
y = df["Action"]                    # dependent variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

acr = RandomForestClassifier(n_estimators = 30)

acr.fit(X_train, y_train)
print(acr.score(X_test,y_test))     # print the accuracy




pred = acr.predict(X_train)         # prediction


y_test = np.array(list(y_test))
t = np.resize(y_test, (1,2000))     # resize Y_test
y_pred = np.array(pred)
p = np.resize(y_pred, (1,2000))     # # resize Y_pred


comp = pd.DataFrame({'Actual':t.flatten(),
                     'Predict':p.flatten()})

graph = comp.head(20)    # take top 20 valus in graph
graph.plot(kind = 'bar') # shor bar chart of graph