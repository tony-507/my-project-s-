from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

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


# ######################################################
# Pre-processing
t0 = time()

print('Splitting into test set and training set...')

X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.25, random_state=42)

print('Done in %f s' % (time()-t0))

# PCA
n_components = 150

t0 = time()
print('Implementing PCA...')

pca = PCA(n_components=n_components, svd_solver='randomized',
			whiten=True).fit(X_train)

print('Done in %f s' % (time()-t0))

t0 = time()
print("Extracting the top %d eigenfaces from %d faces..."
		% (n_components, X_train.shape[0]))

eigenfaces = pca.components_.reshape((n_components, h, w))

X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

print('Done in %f s' % (time()-t0))

# ######################################################
# SVM

t0 = time()
print('Fitting model...')

param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
			'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }

clf = GridSearchCV(
    SVC(kernel='rbf', class_weight='balanced'), param_grid
)
clf = clf.fit(X_train_pca, y_train)

print('Done in %f s' % (time()-t0))

print("Best estimator found by grid search:")
print(clf.best_estimator_)

# ########################################################
# Evaluation


print('Predicting labels on test set...')

y_pred = clf.predict(X_test_pca)
print("done in %fs" % (time() - t0))

print(classification_report(y_test, y_pred, target_names=target_names))
print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))

# ######################################################
# Visualisatioin by matplotlib

def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
	"""Helper function to plot a gallery of portraits"""
	plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
	plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
	for i in range(n_row * n_col):
		plt.subplot(n_row, n_col, i + 1)
		plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
		plt.title(titles[i], size=12)
		plt.xticks(())
		plt.yticks(())

# plot the result of the prediction on a portion of the test set

def title(y_pred, y_test, target_names, i):
	pred_name = target_names[int(y_pred[i])]
	true_name = target_names[int(y_test[i])]
	return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

prediction_titles = [title(y_pred, y_test, target_names, i)
					for i in range(y_pred.shape[0])]

plot_gallery(X_test, prediction_titles, h, w)

# plot the gallery of the most significative eigenfaces

eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
plot_gallery(eigenfaces, eigenface_titles, h, w)

plt.show()