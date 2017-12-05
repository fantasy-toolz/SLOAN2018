from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import rcParams


rcParams['axes.linewidth'] = 1.5



#Player,Clusters,R.Slope,BB.Slope,H.Slope,R.R^2,BB.R^2,H.R^2

Clusters = np.genfromtxt('/Users/mpetersen/Downloads/GC2_ClusteringTable_BB_H_R.csv',\
                        names=['Player','Cluster','r_s','bb_s','h_s','r_r2','bb_r2','h_r2'],\
                         skip_header=1,delimiter=',')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = fig.add_axes([0.3,0.3,0.9,0.9], projection='3d')




ax.scatter(Clusters['r_s'],Clusters['bb_s'],Clusters['h_s'],\
           s=4.,facecolor=cm.jet(Clusters['Cluster']/6.,1.),edgecolor=cm.jet(Clusters['Cluster']/6.,1.))


ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

ax.xaxis._axinfo["grid"]['color'] 

ax.xaxis.set_rotate_label(False)
ax.yaxis.set_rotate_label(False)
ax.zaxis.set_rotate_label(False)

ax.set_xlabel("m$_{\\rm R}$",size=16,rotation=0,labelpad=15)
ax.set_ylabel("m$_{\\rm BB}$",size=16,labelpad=15)
ax.set_zlabel("m$_{\\rm H}$",size=16,labelpad=15)

ax.set_xlabel("m$_{\\rm R}$",size=16,rotation=0)
ax.set_ylabel("m$_{\\rm BB}$",size=16,rotation=0)
ax.set_zlabel("m$_{\\rm H}$",size=16,rotation=0)





ax.set_xlim(0.,1.)
ax.set_ylim(0.,1.)
ax.set_zlim(0.,1.5)


ax.view_init(30., 30.)

#ax.set_position([0.3,0.3,0.3,0.3])

#ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
#ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
#ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)


#plt.subplots_adjust(bottom=0.3,left=0.3)
plt.savefig('/Users/mpetersen/Desktop/rot2.png')

#

plt.show(block=True)
