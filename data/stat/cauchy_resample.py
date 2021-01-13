import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm

# Sampling from Cauchy distribution (shifted by +5) to determine the distribution of corresponding trimmed mean

n = 40
x = np.zeros(n)
y = np.random.uniform(0,1,n)
for i in range(n):
	x[i] = math.tan(math.pi*(y[i]+0.5))+5

# Resampling from empirical distribution
N = 1000
n_bins = 80
data = []
for i in range(N):
	index = np.random.randint(n,size=n)
	r = x[index]
	r = np.sort(r)
	trun = r[int(3*n/8):int(5*n/8)]
	m = trun.mean()
	data.append(m)
data.sort()

# Quantiles of N(0,1)
y = []
for i in range(N):
	q = norm.ppf((i+1)/N)
	y.append(q)

plt.subplot(1,2,1)
plt.hist(data,bins=n_bins,density=1,color='blue',alpha=0.7)
plt.xlabel('Trimmed mean',fontsize=10)
plt.ylabel('Height',fontsize=10)
plt.title('Trimmed mean of Cauchy distribution',fontsize=10)

plt.subplot(1,2,2)
plt.scatter(data,y,c='black',s=5,marker='o',alpha=0.7)
plt.xlabel('Trimmed mean quantiles',fontsize=10)
plt.ylabel('Normal quantiles',fontsize=10)
plt.title('q-q plot with N(0,1)',fontsize=10)

plt.tight_layout()
plt.show()