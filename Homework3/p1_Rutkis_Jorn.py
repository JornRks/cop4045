#problem 1 
#importing testif
from testif import testif
#a)
class NVector(object):
    '''represents an N-dimensional vector of real numbers which are stored in a list object.'''

    # def __init__(self, realNums: list | tuple) -> None:
    #     self.numbers = list(realNums)
#b)
    def __init__(self, *args: list | tuple | float) -> None:
        '''constructuor takes list or tuple of real numbers as args 
        pre: all args are real numbers or a single list/tuple of real numbers
        post: creates a new NVector object with the specified numbers'''
        
        if len(args) >= 2:
            self.numbers = list(args)
        else:
            if len(args) == 0:
                raise TypeError("one arg is required")
            self.numbers = list(args[0])
#c)
    def __len__(self) -> int:
        '''Returns the length of of the vector'''
        return len(self.numbers)

#d)
    def __getitem__(self, index: int) -> int | float:
        '''returns the number at the specified index of the vector
        accepts negative indexing'''
        return self.numbers[index]
#e) 
    def __setitem__(self, index: int, value: int | float) -> None:
        '''sets the number at the specified index of the vector to the specified value
        accepts negative indexing
        pre: value is a real number
        post: sets the number at the specified index of the vector to the specified value
        '''
        self.numbers[index] = value
#f)
    def __str__(self) -> str:
        '''returns a string representation of the vector'''
        return "{}".format(self.numbers)    
#g) 
    def __eq__(self, comparison: object) -> bool:
        '''returns true if the vector is equal to the specified vector, false otherwise
        pre: comparison is an NVector object
        post: returns true if the vector is equal to the specified vector, false otherwise'''
        if isinstance(comparison, NVector):
            if comparison.numbers == self.numbers:
                return True
        return False
    
    def __ne__(self, comparison: object) -> bool:
        '''returns true if the vector is not equal to the specified vector, false otherwise
        pre: comparison is an NVector object
        post: returns true if the vector is not equal to the specified vector, false otherwise'''
        if isinstance(comparison, NVector):
            if comparison.numbers == self.numbers:
                return False
        return True
#h)
    def __add__(self, added: object) -> object:
        '''adds the vector to another NVector or a number
        pre: added is an NVector object or a real number
        post: returns a new NVector object with the sum of the two vectors or the vector and the number'''
        newVector = []
        if isinstance(added, NVector):
            if len(self.numbers) != len(added.numbers):
                raise ValueError("vectors are not the same length")
            for i in range(len(self.numbers)):
                newVector.append(self.numbers[i] + added.numbers[i])
        else:
            for number in self.numbers:
                newVector.append(number + added)
        return NVector(newVector)

    def __radd__(self, added: object) -> object:
        '''reverse addition with another NVector or a number'''
        return self.__add__(added)
#i) 
    def __mul__(self, multiplied: object) -> float:
        '''scalar multiplication with another NVector or a number
        pre: multiplied is an NVector object or a real number
        post: returns the dot product of the two vectors or the vector and the number'''
        product = 0
        if isinstance(multiplied, NVector):
            if len(self.numbers) != len(multiplied.numbers):
                raise ValueError("vectors are not the same length")
            for i in range(len(self.numbers)):
                product += self.numbers[i] * multiplied.numbers[i]
        else:
            for number in self.numbers:
                product += number * multiplied
        return product
    
    def __rmul__(self, multiplied: object) -> float:
        return self.__mul__(multiplied)
#j)  
    def zeros(n: int) -> object:
        '''class methods that returns a new NVector object with dimension n with all elements 0
        pre: n is a non-negative integer
        post: returns a new NVector object with dimension n with all elements 0'''
        zeroVector = []
        if n < 0:
            raise ValueError("n must be a non-negative integer")
        for i in range(n):
            zeroVector.append(0)
        return NVector(zeroVector)
    
#k) main func using testif to test parts a-j (hw says a-i but i did j to be sure)
def main():
    #testing a)
    va = NVector([1, 2, 3, 4])
    testif(va.numbers == [1, 2, 3, 4], "constructor test with list", "constructor works", "constructor failed")
    
    #testing b)
    vb = NVector(1, 2, 3, 4)
    testif(vb.numbers == [1, 2, 3, 4], "constructor test with multiple args", "constructor works", "constructor failed")
    
    #testing c)
    vc = NVector([1, 2, 3, 4])
    testif(len(vc) == 4, "len test", "len works", "len failed")
    
    #testing d)
    vd = NVector([1, 2, 3, 4])
    testif(vd[2] == 3, "getitem test with positive index", "getitem works", "getitem failed")
    testif(vd[-2] == 3, "getitem test with negative index", "getitem works", "getitem failed")
    
    #testing e)
    ve = NVector([1, 2, 3, 4])
    ve[2] = 10
    testif(ve[2] == 10, "setitem test", "setitem works", "setitem failed")
    
    #testing f)
    vf = NVector([1, 2, 3, 4])
    testif(str(vf) == "[1, 2, 3, 4]", "str test", "str works", "str failed")
    
    #testing g)
    vg = NVector([1, 2, 3, 4])
    vgEQ = NVector([1, 2, 3, 4])
    vgNE = NVector([1, 0, 1, 0])
    testif(vg == vgEQ, "eq test", "eq works", "eq failed")
    testif(vg != vgNE, "ne test", "ne works", "ne failed")
    
    #testing h)
    vh = NVector([1, 2, 3, 4])
    vhAdded = NVector([1, 2, 3, 4])
    testif(vh + vhAdded == NVector([2, 4, 6, 8]), "add test with NVector", "add works", "add failed")
    testif(vh + 2 == NVector([3, 4, 5, 6]), "add test with number", "add works", "add failed")
    testif(2 + vh == NVector([3, 4, 5, 6]), "radd test with number", "radd works", "radd failed")
    
    #testing i)
    vi = NVector([1, 2, 3, 4])
    viMultiplied = NVector([1, 2, 3, 4])
    testif(vi * viMultiplied == 30, "mul test with NVector", "mul works", "mul failed")
    testif(vi * 5 == 50, "mul test with number", "mul works", "mul failed")
    testif(5 * vi == 50, "rmul test with number", "rmul works", "rmul failed")
    
    #testing j)
    vj = NVector.zeros(6)
    testif(vj.numbers == [0, 0, 0, 0, 0, 0], "zeros() test", "zeros() works", "zeros() failed")

    #fauID
    print('Jorn Rutkis')
    print('Z-Number: Z23737550') 
if __name__ == "__main__":
    main()
