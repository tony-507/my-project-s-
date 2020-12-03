import numpy as np
import tensorflow as tf
import pickle
from tensorflow import keras
from tensorflow.keras import layers

label_test = []

# Test data
f = open("../SR-ARE-score/names_onehots.pickle","rb")
data_test = pickle.load(f)
f.close()

smile_test = data_test['onehots'].reshape(-1,70,325,1)

# Model
model = keras.models.load_model('my_model.h5',)

label = model.predict(smile_test)
label = np.where(label>0.5, 1, 0)

total = len(label)

f = open('labels.txt','w')
for i in range(total):
	np.savetxt(f,label[i])
f.close()