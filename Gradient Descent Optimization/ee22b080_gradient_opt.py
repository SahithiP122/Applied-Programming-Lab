# Set up imports which are required
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm

# grad_opt() function which implements the gradient descent algorithm for 1D and 2D polynomials only
def grad_opt(func,grad_func,base,best):

    # Learning rate is set to be 0.1 for all cases
    lr = 0.1

    # Lists to store the coordinates of the optimization path
    xall,yall,zall = [],[],[]

    # 1D functions
    if len(best) == 1:
        xbase = base[0]
        ybase = [func(i) for i in xbase]
        fig,ax = plt.subplots()
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.plot(xbase,ybase,label=f"Given function {func.__name__}")
        lnall,  = ax.plot([], [], 'ro',label="Convergence Path")
        lngood, = ax.plot([], [], 'go', markersize=10)
        ax.legend()

        # onestepderiv() function updates the points in the path
        def onestepderiv(frame):
            nonlocal best
            xall.append(best[0])
            yall.append(func(best[0]))

            # Equation to update the points in the path
            x = best[0] - grad_func[0](best[0])*lr
            best[0] = x

            lngood.set_data([x],[func(x)])
            lnall.set_data(xall,yall)
            ax.set_title(f"x = {best[0]}\ny = {func(best[0])}")
        
        # Creating animation to show how the optimization happens
        animation = FuncAnimation(fig,onestepderiv,frames=range(80),interval=80,repeat=False)
        plt.show()
        print(f"Optimized Values for {func.__name__}(x):")
        print(f"x: {round(best[0],4)}\ny: {round(func(best[0]),4)}")

    # 2D functions
    elif len(best) == 2:
        xbase,ybase = base[0],base[1]
        zbase = [func(base[0][i],base[1][i]) for i in range(len(base[0]))]
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        mx, my = np.meshgrid(base[0], base[1])
        mz = func(mx, my)
        s = ax.plot_surface(mx,my,mz,cmap=cm.PuBu,alpha=0.9)
        lngood, = ax.plot([], [], [], 'go', markersize=10)
        scat = ax.scatter([],[],[],color='red',s=30,label="Convergence Path")
        ax.legend()

         # onestepderiv() function updates the points in the path, usage is different in 1D and 2D
        def onestepderiv(frame):
            nonlocal best
            xall.append(best[0])
            yall.append(best[1])
            zall.append(func(best[0],best[1]))
            lngood.set_data([best[0]],[best[1]])
            lngood.set_3d_properties([func(best[0],best[1])])

            # Equations to update the points in the path
            best[0] -= grad_func[0](best[0],best[1])*lr
            best[1] -= grad_func[1](best[0],best[1])*lr

            scat._offsets3d = (xall,yall,zall)
            ax.set_title(f"x = {best[0]}, y = {best[1]}\n{func.__name__}(x,y) = {func(best[0],best[1])}")
        
        # Creating animation to show how the optimization happens
        animation = FuncAnimation(fig,onestepderiv,frames=80,interval=80,repeat=False)
        plt.show()
        print(f"Optimized Values for {func.__name__}(x,y): ")
        print(f"x: {round(best[0],4)}, y: {round(best[1],4)}\nf3(x,y): {round(func(best[0],best[1]),4)}")

# Some examples of functions along with their gradients
def f1(x):
    return x**2 + 3*x + 8
def f1_dx(x):
    return 2*x + 3
def f3(x, y):
    return x**4 - 16*x**3 + 96*x**2 - 256*x + y**2 - 4*y + 262
def df3_dx(x, y):
    return 4*x**3 - 48*x**2 + 192*x - 256
def df3_dy(x, y):
    return 2*y - 4
def f4(x,y):
    return np.exp(-(x - y)**2) * np.sin(y)
def df4_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)
def df4_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)
def f5(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1
def f5_dx(x):
    return (-4)*(np.cos(x)**3)*np.sin(x) + (-3)*np.cos(x)*(np.sin(x)**2) + (-8)*np.sin(x)*np.cos(x) - np.sin(x)

# Setting the ranges for optimization
xbase1 = np.linspace(-5,5,100)
xbase2 = np.linspace(-10,10,100)
ybase2 = np.linspace(-10,10,100)
xbase3 = np.linspace(-np.pi,np.pi,100)
ybase3 = np.linspace(-np.pi,np.pi,100)
xbase4 = np.linspace(0,2*np.pi,100)

# Setting the starting points
bx1 = 5
bx2,by2 = 5,5
bx3,by3 = -0.5,-0.5
bx4 = np.pi - 0.1

# Implementation
grad_opt(f1,[f1_dx],[xbase1],[bx1])
grad_opt(f3,[df3_dx,df3_dy],[xbase2,ybase2],[bx2,by2])
grad_opt(f4,[df4_dx,df4_dy],[xbase3,ybase3],[bx3,by3])
grad_opt(f5,[f5_dx],[xbase4],[bx4])