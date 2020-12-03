from time import time
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow import keras
from sklearn.model_selection import train_test_split

# ######################################################
# Data Extraction

data = np.loadtxt('data.txt')
X = data[:,0:-1]
y = data[:,-1]

target_names = []
f = open('label.txt','r',newline="\n")
lines = np.loadtxt(f, dtype=str, delimiter=",")
for line in lines:
	target_names.append(line)
f.close()

(n_samples, n_features) = X.shape
n_classes = len(target_names)
h = 50
w = 37

X = X.reshape(n_samples,h,w,1)

# ######################################################
# Pre-processing
t0 = time()

print('Splitting into test set and training set...')

X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.25, random_state=42)

print('Done in %f s' % (time()-t0))

# Prediction
model = keras.models.load_model('my_model.h5',)

filters, bias = print(model.layers[0].get_weights())
print(filters)