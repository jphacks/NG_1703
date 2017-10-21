import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
x = np.arange(0, 10, 0.1)

ims = []
for a in range(50):
    y = np.sin(x - a)
    line, = plt.plot(x, y, "r")
    ims.append([line])

ani = animation.ArtistAnimation(fig, ims)
ani.save('anim.gif', writer="imagemagick")
ani.save('anim.mp4', writer="ffmpeg")
plt.show()
