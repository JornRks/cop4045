#parse python files
#a) Line number function
def line_number(in_file: str, out_file: str) -> None:
    '''Reads lines from input file and outputs them numbered in the ouput file'''
    try:
        input_file = open(in_file, 'r') #open read file
        output_file = open(out_file, 'w') #open write file

        for number, line in enumerate(input_file, 1): #create tuples using enumerate with (number, line)
            output_file.write('{}. {}'. format(number, line)) #write to output, i use format here to add number and line

        input_file.close()#close input
        output_file.flush()#save
        output_file.close()#close
    except FileNotFoundError: #if the file is not found, print error, raise exception
        print('The file could not be found')
        raise

#b) parse functions
def parse_functions(py_file: str) -> tuple:
    '''Reads from python file, parses text, and returns tuples for each function
    containing the line number, the function name, the formal argument, 
    the function code as a string'''
    try:
        file_input = open(py_file, 'r') #open read file
        clean_input = '' #list for cleaned input
        line_num = 0 #track line number
        function_lineNums = [] #list for the function line numbers
        functions = [] #list to hold function tuples

        for line in file_input: #for each line 
            line_num += 1 #increase line number
            if line[:4] == 'def ': #if line has 'def'
                function_lineNums.append(line_num) #append line number
            if '#' in line: #if there is a comment in the line
                line = line.split('#')[0] +'\n' #split at the comment, and keep the 1st part, which is the code in this case
            if line.strip() != "": #if line is not empty
                clean_input += line #add the line to clean input
        file_input.close()

        clean_input = '\n' +clean_input #adds newline to clean input so fucntions are properly split
        function_parts = clean_input.split('\ndef ') #splits at def, includes the new line so its only when a new function starts, not a def string in my code
        for parts, function_lineNums in zip(function_parts[1:], function_lineNums): #i loop through each function part and line number, zip combines the two lists to a tuple
            code = 'def ' + parts #adding def at the start since lost to split
            name = parts.split('(')[0] #splitting the parenthesis around the functions arguments, keeping the 1st part which is the func name
            args = parts.split('(')[1].split(')')[0] #splittinf at the same parenthesis, but keeping the 2nd part (function areguments), splitting again at the closing and the 1st part to isolate the arguments
            if '\nmain()' in code: #this is for the second main() in the main fucntion, i remove it so its not included in the code string
                code = code.split('\nmain()')[0] #split at the 2nd main() (bottom of my main fucntion) and i keep the 1st part
                        

            function_elements = (function_lineNums, name, args, code) #tuple for functions elements
            functions.append(function_elements) #append the tuple to functions

            names = [] #store func names
            sorted_tuples = [] #store sorted function tuples
            for function in functions: #for each function tuple
                names.append(function[1]) #append the 2nd element to names (this is the name of the function)
            names.sort() #sort the names alphabetically for proper format
            for name in names: #for each name stored
                for function in functions: #for each function tuple
                    if function[1] == name: #if the function name matches the current name in the loop, append to sorted_tuples. This work bc the names are sorted, and functions are appended by said name, so the tuples are sorted
                        sorted_tuples.append(function)

            tup = tuple(sorted_tuples) #convert list of tuples to a tuple of tuples for proper formatting
        return tup 
    except FileNotFoundError: #same as above, if file not found, error is printed and exception raised
        print('The file was not found!')
        raise
        


def main():
    testing_a = line_number('p1_Rutkis_Jorn.py', 'testing.txt')
    testing_b = parse_functions('p1_Rutkis_Jorn.py')
    print(testing_b)
main()