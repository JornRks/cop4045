#5a)
from turtle import *
from testif import testif
def draw_leaf_straight(level: int, length: float) -> None:
    '''draws a leaf shape with the given level and length'''
    def branch(length: float, depth: int) -> None: #local function to draw a branch of the leaf
        '''one branch only'''
        if depth == 0:
            forward(length)
            backward(length)
            return #base case: straight line
        else:
            forward(length) #draws the main branch
            left(45) #turns left to draw the left branch
            branch(length*0.4, depth - 1) #recursive call to draw the left branch using 40% of the length and decreasing depth by 1
            right(90) #turns right to draw the right branch
            branch(length * 0.4, depth - 1) #recursive call to draw the right branch using 40% of the length and decreasing depth by 1
            left(45) #turns left to face the main branch again
            if depth == 1: #if depth is 1, draw a straight tip
                forward(length) 
                backward(length)
            else:
                branch(length*0.7, depth - 1) #else draws a branch using 70% of the length and decreasing depth by 1
            backward(length) #returns to starting point
    branch(length, level) #calls auxiliary function to draw leaf

#5b)
def strB(n: int, base: int=10) -> str:
    '''returns string representation of n in base specified
    pre: n is a non-negative int, base is an integer between 2 and 26
    post: returns string representation of n in base specified'''

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #letter reps for digits greater than 9
    rem = n % base #returns remainder of n divided by base
    if rem < 10: #if remainder is < 10, no need to use letters
        remainder = str(rem) #string rep of remainder
    else: #if gearter than 9, use letter rep
        remainder = letters[rem - 10] #subtracts 10 as letter reps begin at 10, ex: 13-10 = 3 = D
    if n < base: 
        return remainder #base case: digit fits in single base, return remainder
    result = strB(n // base, base) #recusrivly call strB w n divided by base
    return result + remainder #return result plus remainder

def test_strB() -> None:
    '''testif function for strB'''
    testif(strB(10, 2) == "1010", "binary representation of 10", "correct = " + str(strB(10, 2)), "incorrect")
    testif(strB(346, 12) == "24A", "base 12 representation of 346", "correct = " + str(strB(346, 12)), "incorrect")
    testif(strB(1254, 16) == "4E6", "hexadecimal representation of 1254", "correct = " + str(strB(1254, 16)), "incorrect")
    testif(strB(30, 24) == "16", "base 24 representation of 30", "correct = " + str(strB(30, 24)), "incorrect")
    print("Jorn Rutkis")
    print("Z-Number: Z23737550")

#5c)
binom_dict = {} #will store already computed values of C(n, k) to avoid recomputation
def Cnk_m(n: int, k: int) -> int:
    '''computesd the values of the binomial coefficent suing recursion and memoization
    pre: n and k are non-negative integers where n >= k
    post: returns binomial coefficient C(n, k)'''
    if (n, k) in binom_dict: #if n and k are already computed, return the value
        return binom_dict[(n, k)]
    if k == 0 or k == n: #base case, return 1 
        return 1
    ways = Cnk_m(n-1, k-1) + Cnk_m(n-1, k) #recursive call to compute binomial coefficient 
    binom_dict[(n, k)] = ways #store the value in dict 
    return ways #return the binomial coefficient

def test_Cnk_m() -> None:
    '''testif function for Cnk_m'''
    testif(Cnk_m(7, 2) == 21, "C(7, 2)", "correct = " + str(Cnk_m(7, 2)), "incorrect")
    testif(Cnk_m(22, 3) == 1540, "C(22, 3)", "correct = " + str(Cnk_m(22, 3)), "incorrect")
    testif(Cnk_m(11, 4) == 330, "C(11, 4)", "correct = " + str(Cnk_m(11, 4)), "incorrect")
    testif(Cnk_m(31, 5) == 169911, "C(31, 5)", "correct = " + str(Cnk_m(31, 5)), "incorrect")
    print("Jorn Rutkis")
    print("Z-Number: Z23737550")

#5d)
def make_pairs(seq1: list, seq2: list, accumulator: list | None = None) -> list:
    '''returns list of tuples of pairs from seq1 and seq2'''
    if len(accumulator) == 0: #if accumulator is empty, initialize it
        accumulator = []
    if len(seq1) == 0 or len(seq2) == 0: #base case: one list is empty/out of elements, return acc
        return accumulator
    tup = (seq1[0], seq2[0]) #uple of first elements of both lists at same index
    accumulator.append(tup) #append tuple to accumulator
    return make_pairs(seq1[1:], seq2[1:], accumulator) #recursive call on smaller lists with first elemnts removed

def test_make_pairs() -> None:
    '''testif function for make_pairs'''
    testif(make_pairs([], ['x', 'y'], []) == [], 'test w empty first sequence', "correct = " + str(make_pairs([], ['x', 'y'], [])), "incorrect")
    testif(make_pairs(['a', 'b'], [], []) == [], "test w empty second sequence", "correct = " + str(make_pairs(['a', 'b'], [], [])), "incorrect")
    testif(make_pairs(['a', 'b', 'c'], ['x', 'y', 'z'], []) == [('a', 'x'), ('b', 'y'), ('c', 'z')], 'test w equal lengths', "correct = " + str(make_pairs(['a', 'b', 'c'], ['x', 'y', 'z'], [])), "incorrect")
    testif(make_pairs(['a', 'b'], ['x', 'y', 'z'], []) == [('a', 'x'), ('b', 'y')], "test w bigger first length", "correct = " + str(make_pairs(['a', 'b'], ['x', 'y', 'z'], [])), "incorrect")
    testif(make_pairs(['a', 'b', 'c'], ['x', 'y'], []) == [('a', 'x'), ('b', 'y')], "test w bigger second length", "correct = " + str(make_pairs(['a', 'b', 'c'], ['x', 'y'], [])), "incorrect")
    print("Jorn Rutkis")
    print("Z-Number: Z23737550")

def run_Cnk(n: int, k: int) -> None:
    '''prints the value of binomial coefficient for C(n, k)
    made this so i can call it from the command line with different values of n and k'''
    result = Cnk_m(n, k)
    print("C({}, {}) = {}".format(n, k, result))

def main() -> None:
    """set up and draw the leaf."""
    clearscreen()
    delay(0)
    up()
    goto(0, 0) #start position
    down() #sets pen down to draw
    left(90) #faces upwards
    draw_leaf_straight(6, 120) #calls the func to draw leaf, level is 6 and length is 120
    done()
    print('5b)')
    test_strB() #calls the testif for strB
    print('5c)')
    test_Cnk_m() #calls the testif for Cnk_m
    print('5d)')
    test_make_pairs() #calls the testif for make_pairs
if __name__ == "__main__":
    main()