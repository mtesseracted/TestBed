
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()

ax = plt.axes(xlim=(0, 2), ylim=(0, 100))

line = []
N = 4

for j in range(N):
    temp, = plt.plot([], [])
    line.append(temp)

line = tuple(line)

def init():
    for j in range(N):
        line[j].set_data([], [])
    return line,

def animate(i):
    for j in range(N):
        line[j].set_data([0, 2], [10 * j,i])
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True)

plt.show()
