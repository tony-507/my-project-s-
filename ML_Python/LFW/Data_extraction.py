import numpy as np
from sklearn.datasets import fetch_lfw_people

lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

X = lfw_people.data
y = lfw_people.target
target_names = lfw_people.target_names

num_person = len(target_names)

data = np.column_stack((X,y))
np.savetxt('data.txt',data)

f = open('label.txt','w')
for i in range(0,num_person):
	f.write('%s\n' % target_names[i])
f.close()
