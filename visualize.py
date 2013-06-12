import pylab as pl
from mpl_toolkits.mplot3d import Axes3D


# Plotting
fignum = 1
fig = pl.figure(fignum, figsize=(16,9))

#Clear figure
pl.clf()

#Create view perspective
ax = Axes3D(fig, rect=[0,0,1,1], elev=48, azim=134)

#Clear axis
pl.cla()

#---------------Plotting---------------#
import numpy as np
from sklearn.cluster import KMeans

a = np.random.randn(200,4)

est = KMeans(n_clusters=3)
est.fit(a)
labels = est.labels_
ax.scatter(a[:, 3], a[:, 0], a[:, 2], c=labels.astype(np.float))

#Axis tick increments
ax.w_xaxis.set_ticklabels(range(0,20,2))
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
#Axis Labels
ax.set_xlabel('X-Axis')
ax.set_ylabel('Y-Axis')
ax.set_zlabel('Z-Axis')

#Render
pl.show()