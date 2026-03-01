import numpy as np
import matplotlib.pyplot as plt

array = np.array([25,35,75,85,90,20,70,120])
mylabel = ["A","B","C","D","E","F","G","H"]

plt.pie(array,labels=mylabel)
plt.legend()
plt.show()
