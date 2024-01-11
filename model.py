

import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
import matplotlib
from matplotlib import pyplot as plt
import pickle
import warnings

phishing_df = pd.read_csv(r'original_new_phish_25k.csv')
legitimate_df = pd.read_csv(r'legit_data.csv')

data = pd.concat([legitimate_df, phishing_df])
#data = data.drop('url',axis=1)
data = data.drop(['url','NonStdPort','GoogleIndex','double_slash_redirecting','https_token'],axis=1)

non_numeric_cols = data.select_dtypes(exclude=['number']).columns.tolist()
data[non_numeric_cols] = data[non_numeric_cols].apply(pd.to_numeric, errors='coerce')
data.dropna(inplace=True)

X = data.drop('Label', axis=1)
y = data['Label']
X.sample(frac=1)
X.shape

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25, random_state=0)

# print('X_train:',np.shape(X_train))
# print('y_train:',np.shape(y_train))
# print('X_test:',np.shape(X_test))
# print('y_test:',np.shape(y_test))

input_shape = [X_train.shape[1]]


#structure
model = keras.Sequential([
    layers.BatchNormalization(input_shape=input_shape),
    layers.Dense(130, activation='sigmoid'),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(128, activation='relu'), 
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(1, activation='sigmoid'),
])
    
#compile
model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(),
                metrics=['binary_accuracy'])

model.fit(X_train,y_train,epochs=50)

model.save ("nn.h5")
# pickle.dump(model,open("model.h5","wb"))
# model = pickle.load(open("model.h5","rb"))

# def pred(sample):
#     predicted = model.predict(sample)
#     return predicted