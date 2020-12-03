# Variable: data, data_test, label, label_test


import tensorflow as tf
import numpy as np
import pickle
from tensorflow import keras
from tensorflow.keras import layers

# Universal constants 
reg = 0.03 # Regularization constant
Batch = 32 # Batch size
Epo = 8 # Epoch


# Training data
pos = 0
neg = 0
label = []
label_test = []

f = open("data/SR-ARE-train/names_onehots.pickle","rb")
data = pickle.load(f)
f.close()

smile = data['onehots'].reshape(-1,70,325,1)

f = open("data/SR-ARE-train/names_labels.txt", "r", newline="\n")
lines = np.loadtxt(f, dtype=str, delimiter=",")
for line in lines:
	toxic = line[1]
	if int(toxic)==1:
		pos = pos + 1
	else: neg = neg + 1
	label.append(int(toxic))
f.close()

# Test data
f = open("data/SR-ARE-test/names_onehots.pickle","rb")
data_test = pickle.load(f)
f.close()

f = open("data/SR-ARE-test/names_labels.txt", "r", newline="\n")
lines = np.loadtxt(f, dtype=str, delimiter=",")
for line in lines:
	toxic = line[1]
	label_test.append(int(toxic))
f.close()

smile_test = data_test['onehots'].reshape(-1,70,325,1)


# Class weight to deal with imbalanced data
total = pos + neg
weight_for_0 = (1 / neg)*(total)/2.0 
weight_for_1 = (1 / pos)*(total)/2.0
class_weight = {0: weight_for_0, 1: weight_for_1}

# Monitor data
reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=4, min_lr=0.0001)
model_callback = keras.callbacks.ModelCheckpoint(filepath='./model', monitor='val_loss', save_best_only=True)
tensorboard = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1)


# Model training
model = tf.keras.Sequential()

model.add(keras.layers.Conv2D(4,(2,2), input_shape=smile.shape[1:], kernel_regularizer=keras.regularizers.l2(reg)))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

model.add(keras.layers.Conv2D(4,(2,2), kernel_regularizer=keras.regularizers.l2(reg)))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(10))
model.add(keras.layers.Activation('relu'))

model.add(keras.layers.Dense(1))
model.add(keras.layers.Activation('sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(smile,label, epochs=Epo, batch_size=Batch, validation_data=(smile_test,label_test), class_weight=class_weight, callbacks=[tensorboard, reduce_lr, model_callback])

model.save('my_model.h5')

res = model.evaluate(smile_test,label_test)
print(res)

