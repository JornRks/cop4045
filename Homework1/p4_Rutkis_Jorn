import matplotlib.pyplot as plt
def plot_function(fun_str, xmin, xmax, ns):

    num_samples = ns
    dx = (xmax - xmin) / num_samples #create step size 
    x = xmin
    xs = []
    for i in range(ns): #loop for number of samples
        xs.append(x)
        x += dx #add step size and append to list of xs
    ys = []
    for x in xs: #loop through xs 
        y = eval(fun_str) #evaluate function at that x value
        ys.append(y) #append y result to ys

    print("{:<8} {:>11}".format('X:', 'Y:')) #X is left justified 8 spaces after and Y is right justified with 11 spaces before
    print("---------------------------------")
    for x in range(len(xs)): #loop through xs, printing the values at x (index) in both xs and ys
        print("X Value: {:>8.3f} Y Values: {:>8.3f}".format(xs[x],ys[x])) #formatted right justified, 8 spaces, float w 3 decimal places

    plt.plot(xs, ys)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph of Function Y')
    plt.show()

fun_str = input("Enter function using variable x: ")
ns_str = input("Enter # of samples: ")
ns = int(ns_str)
xmin_str = input('Enter min: ')
xmin = float(xmin_str)
xmax_str = input("Enter max: ")
xmax = float(xmax_str)

plot_function(fun_str, xmin, xmax, ns)