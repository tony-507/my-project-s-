from time import time
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers,datasets,models
from tensorflow.keras.models import Sequential

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



# DNN parameter
reg = 0.03 # Regularization constant
Epo = 10 # Epoch
input_shape = (h,w,1)

# ######################################################
# Pre-processing
t0 = time()

print('Splitting into test set and training set...')

X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.25, random_state=42)

print('Done in %f s' % (time()-t0))

# ######################################################
# Monitor data
reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=4, min_lr=0.0001)
model_callback = keras.callbacks.ModelCheckpoint(filepath='./model', monitor='val_loss', save_best_only=True)
tensorboard = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1)

# Convolution Layer

#t0 = time()

#print('Creating model...')

model = models.Sequential()

model.add(layers.Conv2D(4, (3, 3), activation='relu', input_shape=input_shape ,kernel_regularizer=keras.regularizers.l2(reg)))
model.add(keras.layers.BatchNormalization())

model.add(layers.Conv2D(5, (2, 2), activation='relu',kernel_regularizer=keras.regularizers.l2(reg)))
model.add(keras.layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))

# Dense layer

model.add(keras.layers.Dropout(0.5))
model.add(layers.Flatten())

model.add(layers.Dense(14))
model.add(layers.Dense(16))
model.add(layers.Dense(64, activation='relu'))
#model.add(layers.Dense(13, activation='relu'))
model.add(layers.Dense(n_classes))

model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

#print('Done in %f s' % (time()-t0))

model.summary()

t0 = time()

#print('Training model...')

history = model.fit(X_train, y_train, epochs=Epo, validation_data=(X_test, y_test))

#print('Done in %f s' % (time()-t0))

model.save('my_model.h5')

res = model.evaluate(X_test,y_test)
print(res)

# ######################################################
# Visualisation of error

plt.figure()

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

plt.show()