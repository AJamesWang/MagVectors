from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# load some test data for demonstration and plot a wireframe
X, Y, Z = axes3d.get_test_data(0.1)
ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5)

# rotate the axes and update
while True:
	angle=ax.azim+1
	elev=ax.elev
	ax.view_init(elev, angle)
	plt.draw()
	plt.pause(.001)
	print(angle)