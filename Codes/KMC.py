import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

X = np.array([
    [15, 39], [15, 81], [16,  6], [16, 77], [17, 40], [17, 76], [18,  6], [18, 94],
    [19,  3], [19, 72], [19, 14], [19, 99], [20, 77], [20,  6], [21, 94], [23, 35],
    [23,  5], [24, 73], [25,  5], [28, 14], [28, 82], [29, 32], [30, 73], [33,  4],
    [33, 92], [34, 14], [37, 32], [38, 92], [39, 36], [39, 61], [40,  6], [40, 72],

    [15, 39], [15, 81], [16,  6], [16, 77], [17, 40], [17, 76], [18,  6], [18, 94],
    [19,  3], [19, 72], [19, 14], [19, 99], [20, 77], [20,  6], [21, 94], [23, 35],
    [23,  5], [24, 73], [25,  5], [28, 14], [28, 82], [29, 32], [30, 73], [33,  4],
    [33, 92], [34, 14], [37, 32], [38, 92], [39, 36], [39, 61], [40,  6], [40, 72],

    [15, 39], [15, 81], [16,  6], [16, 77], [17, 40], [17, 76], [18,  6], [18, 94],
    [19,  3], [19, 72], [19, 14], [19, 99], [20, 77], [20,  6], [21, 94], [23, 35],
    [23,  5], [24, 73], [25,  5], [28, 14], [28, 82], [29, 32], [30, 73], [33,  4],
    [33, 92], [34, 14], [37, 32], [38, 92], [39, 36], [39, 61], [40,  6], [40, 72],
])


kmeans = KMeans(n_clusters=5)
y_kmeans = kmeans.fit_predict(X)

print(y_kmeans)

colors = ['red', 'blue', 'green', 'yellow' , 'orange']

for i in range(5):
    plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], s=200, c=colors[i], label=f'cluster {i+1}')

plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=300, c='pink', label='Centroids')
plt.title("Customer Segmentation using K-Means")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (0100)")
plt.legend()
plt.show()
