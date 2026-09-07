import math
import pylab

while True:
    a_int = input("Enter a value: ")
    if a_int == "":
        break
    b_int = input("Enter b value: ")
    c_int = input("Enter c value: ")

    a_float = float(a_int)
    b_float = float(b_int)
    c_float = float(c_int)

    b_val = b_float ** 2 #squared b val
    ac_val = 4 * a_float * c_float #4ac val
    disc_val = b_val - ac_val

    if disc_val < 0:
        print("No real solutions")
        #for plotting
        plot_x_opt = -b_float / (2 * a_float)
        plot_x_min = plot_x_opt - 5 #center dom around x_opt
        plot_x_max = plot_x_opt + 5


    elif disc_val == 0:
        x1_val = -b_float / (2 * a_float) #dont worry abt +- disc as its 0
        print("One solution X1: ", x1_val)

        plot_x_min = x1_val - 5 #center dom around single root
        plot_x_max = x1_val + 5

    else: 
        x1_disc = -b_float + math.sqrt(disc_val)
        x2_disc = -b_float - math.sqrt(disc_val)
        x1_val = x1_disc / (2 * a_float)
        x2_val = x2_disc / (2 * a_float)
        print("Two solutions x1, x2: ", x1_val, x2_val)

        if x1_val < x2_val:
            plot_x_min = x1_val - 5 #if x1 is smaller, base the min off x1 and max off x2
            plot_x_max = x2_val + 5
        else: 
            plot_x_min = x2_val - 5 #same here
            plot_x_max = x1_val + 5

    x_vals = []
    y_vals = []
    num_points = 150
    dx = (plot_x_max - plot_x_min) / num_points

    x = plot_x_min
    while x <= plot_x_max:
        x_vals.append(x)
        y = a_float * x**2 + b_float * x + c_float #gen y points based on x vals
        y_vals.append(y)
        x += dx

    pylab.plot(x_vals, y_vals, "ro-")
    pylab.show()
