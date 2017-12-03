# -*- coding: utf-8 -*-
"""
Created on Sat Dec 02 22:58:08 2017

@author: Erich Rentz
"""

from sklearn.cluster import KMeans
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from scipy.interpolate import spline
from sklearn.metrics import mean_absolute_error
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Quick Clustering Exercise 
final_df = aggregate_growth_chart_2('data')

cluster_list = ['R.Slope','BB.Slope', 'H.Slope', 'R.R^2','BB.R^2', 'H.R^2']

X = final_df[cluster_list].values
X_std = StandardScaler().fit_transform(X)

num_clusters = 7
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(X_std)

predict = kmeans.predict(X_std)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_

final_df['Clusters'] = pd.Series(predict, index=final_df.index)
colors = ["k.","r.", "c.","y.", "m.", "g.", "b."]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(len(X)):
    ax.scatter(X[i][1], X[i][2], X[i][0], c = colors[labels[i]][0], linewidths = 0, alpha = 0.3)
fig

df_columns = ['Player', 'Clusters']
df_columns.extend(cluster_list)

cluster_df = final_df[df_columns]

df_list = []
for vector in cluster_list:
    df = cluster_df.groupby(['Clusters'], as_index=False)[vector].median()
    df_list.append(df)

cluster_summary = df_list[0]
for df in df_list[1:]:
    cluster_summary = cluster_summary.merge(df, how='left', on="Clusters")
    
cluster_summary.to_csv("data\GC2_ClusteringSummary_BB_H_R.csv", index=False)
cluster_df.to_csv("data\GC2_ClusteringTable_BB_H_R.csv", index=False)