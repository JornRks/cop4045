
def find_pythagorean(n):
    solutions = []
    a = 1
    #b = 1 didnt need as i did this in nested while loops
    #c = 1
    while a <= n:
        b = 1 #reset b once a incremeants, start at 1 as 0 cant be a value in pythagorean
        while b <= n:
            c = 1 #reset c once b incremeants
            while c <=n:
                if a**2 + b**2 == c**2:
                    solutions.append((a,b,c)) #appends a b c to solutions list
                c += 1 #inc c
            b += 1
        a += 1

    return solutions

n_str = input("Please enter the value of n: ")
n = int(n_str)

output_tuples = find_pythagorean(n) #calls function and assigns output to output_tuples
print(output_tuples)