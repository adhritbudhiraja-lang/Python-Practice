import numpy as np
import matplotlib.pyplot as plt
x=np.linspace(0,2 *np.pi,100)
y1=np.sin(x)
y2=np.cos(x)
plt.plot(x,y1, label = "Sin(x)")
plt.plot(x,y2,label = "Cos(x)")
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.title("Multple Lines Using Matplotlib")
plt.legend()
plt.show()