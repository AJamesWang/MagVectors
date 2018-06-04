from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
                      np.arange(-0.8, 1, 0.2),
                      np.arange(-0.8, 1, 0.8))

u = 1#np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
v = 1#-np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
w = 1#(np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
     #np.sin(np.pi * z))

q = ax.quiver(x, y, z, u, v, w, length=0.1, cmap='binary', lw=2)

test = np.arange(np.prod(x.shape)-2)#np.array([np.arange(np.prod(y.shape)**.5), np.random.rand(np.prod(x.shape))])
q.set_array(test)
print(test)
# print("\n\n\n\n\n\n")
# print(np.prod(x.shape))
# print("\n\n\n\n\n\n")
# print(len(np.random.rand(np.prod(x.shape))))

plt.show()