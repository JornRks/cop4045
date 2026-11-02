#problem 4
from testif import testif
#a) functions
def ed_read(filename: str, fro: int=0, to: int=-1) -> str:
    '''returns as a string the content of the specified file, from (from-to), if to = -1, return all content.
    indexs out of range will raise an IndexError exception while errors related to file I/0 are passed to the caller.'''
    with open(filename, 'r', encoding='utf-8') as temp_file:
        content = temp_file.read() #reads all lines from file as a string and returns it
        if fro < 0 or to < -1: #if fro is less than 0 or to is less than -1, raise IndexError
            raise IndexError("Index out of range")
    if to == -1: #if to is -1, return all content
        to = len(content) #set to to length of content
    if fro > len(content) or to > len(content): #check for valid range
        raise IndexError("Out of range")
    file_content = content[fro:to] #return the content from fro to to
    return file_content

def ed_find(filename: str, search_str: str) -> list:
    '''returns a list of with index positions in the file where srearch_str is found, if not found returns an empty list.
    ValueError raised if search_str is empty string.'''
    if search_str == "": #if search_str is empty, raise ValueError
        raise ValueError("search_str is empty")
    with open(filename, 'r', encoding='utf-8') as temp_file:
        content = temp_file.read() #reads all lines from file as a string and returns it
    indexs = []
    for i in range(len(content)):
        if content[i:i+len(search_str)] == search_str: #if substring starting at index i matches the search_str
            indexs.append(i) #append the index to the list
    return indexs

def ed_replace(filename: str, search_str: str, replace_with: str, occurance: int = -1) -> int:
    '''replaces the search string with replace_with.
    if occurance is -1, replaces all occurances, otherwise replaces the specified occurance,
    where 0 is the first occurance, 1 is the second, etc.
    if occurance exceeds the files occurance index, the function will not replace anything.
    '''
    if search_str == "": #search_str is empty so raise ValueError
        raise ValueError("search_str cant be empty")
    if occurance < -1: #occurance is less than -1 so raise IndexError
        raise IndexError("occurance must be either -1 or non-negative")
    
    with open(filename, 'r', encoding='utf-8') as temp_file:
        content = temp_file.read() #reads all lines from file as a string and returns it
        replaced_count = 0 #initialize replaced_count to 0
    if occurance == -1: #-1 means replace all occurances
        new_str = content.replace(search_str, replace_with) #replace all occurance with replace_with 
        replaced_count = content.count(search_str) #count the number of occurances replaced
    else: 
        positions = ed_find(filename, search_str) #get the index positions of the search_str in the file using ed_find
        if occurance >= len(positions): #if occurances is greater than the number of occurances in the file, dont replace anything
            return 0
        replaced_occurance = positions[occurance] #get the index of the specified occurance, for example the 3rd occurance would be the third index in the positions list
        new_str = content[:replaced_occurance] + replace_with + content[replaced_occurance + len(search_str):] #spliced from start to occurance index, add replaced content, then spliced from end of occurance index to end of content
        #the new content/strign is what was before the occuarnce, plus what is being replaced, plus eveything that was after the occurance
        replaced_count = 1 #only one occurance was replaced, the one specified by the user
    with open(filename, 'w', encoding='utf-8') as temp_file:
        temp_file.write(new_str) #write new_str to the file
    return replaced_count #return the number of occurances that were replaced

def ed_append(filename: str, string: str) -> int:
    '''appends the string to the end of the file.
    if the file dosent exist it creates a file with the name
    returns the number of characters written to the file.'''
    with open(filename, 'a', encoding='utf-8') as temp_file:
        temp_file.write(string) #append specified string to the end of the file
        count = len(string) #length of string to be returned
    return count #return the number of characters appended  
    
def test_ed_replace() -> None:
    '''tests ed_replace'''
    filename = 'p4test.txt'
    with open(filename, 'w', encoding='utf-8') as temp_file:
        temp_file.write("This is a test file to find and replace an instant of the word test. I like to test my functions.")

    count = ed_replace(filename, "test", "exam") #replace all occurances of test with exam
    testif(count == 3, "test replacing all occurances with exam", "correct = 3", "incorrect")

    with open(filename, 'w', encoding='utf-8') as temp_file:
        temp_file.write("This is a test file to find and replace an instant of the word test. I like to test my functions.")

    count = ed_replace(filename, "test", "exam", 0) #replace first occurance of test with exam
    testif(count == 1, "test replacing first occurance with exam", "correct = 1", "incorrect")
    
        
def test_ed_find() -> None:
    '''tests ed_find'''
    filename = 'p4test.txt'
    with open(filename, 'w', encoding='utf-8') as temp_file:
        temp_file.write("This is a test file to find and replace an instant of the word test. I like to test my functions.")
    indexs = ed_find(filename, "test") #find all occurances of test
    testif(indexs == [10, 63, 79], "test finding all occurances of test", "correct = [10, 63, 79]", "incorrect")
    indexs = ed_find(filename, "wow") #find all occurances of wow, which is not in the file
    testif(indexs == [], "test finding missing occurances", "correct = []", "incorrect")

def main():
    test_ed_find()
    test_ed_replace()
    filename = 'p4test_write.txt'
    with open(filename, 'w', encoding='utf-8') as temp_file:
        temp_file.write("")
    print("Content of file before append: {}".format(ed_read(filename)))
    count = ed_append(filename, "abcdab") #append abcdab to the file
    print("Number of characters appended: {}".format(count))
    print("Content of file after append: {}".format(ed_read(filename)))
    print('Content of file from index 0 to 2: {}'.format(ed_read(filename, 0, 2)))
    print('Content of file from index 2 to end of file: {}'.format(ed_read(filename, 2)))
    print('Indexs of ab = {}'.format(ed_find(filename, "ab")))
    print('Number of times ab was replaced with xy = {}'.format(ed_replace(filename, "ab", "xy")))
    print('Content of file after replacing ab with xy: {}'.format(ed_read(filename)))
    print('Jorn Rutkis')
    print('Z-Number: Z23737550')
if __name__ == "__main__":
    main()