def find_dup_str(s,n):

    front_i = 0
    while front_i <= len(s): #while front index is less than the length of string
        base = s[front_i:front_i+n] #my basis will be the length specified by n, aka if im starting at i=0, and n=3, i splice [0:3]

        back_i = front_i+n #setting back index to start where front splice ends
        while back_i < len(s):#same here
            comp = s[back_i:back_i+n] #splice i will be comparing my basis too

            if base == comp: #if a match is found, return the duplicate substring
                return base
            back_i += 1 #iterate back index 
        front_i += 1 #iterate starting index
    return ""   #return empty stringll

#for testing
#string = input('Enter the string: ')
#sublength = input('Enter the substring length: ')
#length = int(sublength)

#output = find_dup_str(string, length)
#print("The first duplicate substring is: ", output)

def find_max_dup(s):
    dupes = []
    for i in range(0, len(s)): 
        dupe = find_dup_str(s, i)#for loop is calling the find_dup_str function, using the same string but differing substring lengths
        dupes.append(dupe) #appends all found dupes to dupes list

    longest_dupe = "" #set initial dupe as empty string
    for i in dupes: #iterate through dupplicates listed in dupes
        if len(i) > len(longest_dupe): #compare length to existing longest 
            longest_dupe = i #set new longest
    return longest_dupe

input_str = input("Please enter string: ")
output = find_max_dup(input_str)
print("The longest substring is: ", output)
