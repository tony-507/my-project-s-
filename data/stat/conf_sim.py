import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import t

x = []

plt.subplot(1,2,1)
plt.axis([1,9,0,50])
for i in range(50):
	new = np.random.normal(5,4,1)
	x.append(new)
	mu = np.mean(x)
	sd = 4
	x1 = mu + 1.645*sd/math.sqrt(i+1)
	x2 = mu - 1.645*sd/math.sqrt(i+1)	
	plt.plot([x1,x2],[i+1,i+1],'b')
plt.plot([5,5],[0,50],'r')


plt.subplot(1,2,2)
plt.axis([1,9,0,50])
x = []
for i in range(50):
	new = np.random.normal(5,4,1)
	x.append(new)
	mu = np.mean(x)
	sd = 4
	p = -t.ppf(0.05,i)
	x1 = mu + p*sd/math.sqrt(i+1)
	x2 = mu - p*sd/math.sqrt(i+1)	
	plt.plot([x1,x2],[i+1,i+1],'b')
plt.plot([5,5],[0,50],'r')

plt.show()
