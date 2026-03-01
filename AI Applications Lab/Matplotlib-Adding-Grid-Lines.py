import numpy as np
import matplotlib.pyplot as plt
x=np.array([30,40,50,60,70,80,90])
y=np.array([240,250,260,270,280,290,300])
plt.title("Sports Watch Data")
plt.xlabel("Average Pulse")
plt.ylabel("Calorie Burnage")
plt.plot(x,y)
plt.grid()
plt.show()