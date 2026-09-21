# ignore comments above the comprehsnions, i built them normally then made them comprehensions
#a) List comp of integers
distinct_integers = [(a, b, c, d) for a in range(1,11) for b in range(1,11) for c in range(1,11) for d in range(1,11) if a**2 + b**2 == c**2 + d**2 and len({a, b, c, d}) == 4]
print('a) ', distinct_integers)

#b) list of strings
#using original to set up my comprehension
#lst = ['One', 'SEVEN', 'three', 'two', 'Ten']
#lower_lst = []
#for element in lst:
    #if len(element) < 5:
        #lower_lst.append(element.lower(), len(element))
lst =  ['One', 'SEVEN', 'three', 'two', 'Ten']
low_lst = [(element.lower(), len(element)) for element in lst if len(element) < 5]
print('b) ',low_lst)

#c) names
names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
#names_formatted = []
#for name in names:
#   names_formatted.append(name.split()[0] +' '+ name.split()[1][0] + '. ' + name.split()[2])
#print(names_formatted)
names_formatted = [(name.split()[0] +' '+ name.split()[1][0] + '. ' + name.split()[2]) for name in names]  
print('c) ',names_formatted)

#d) 
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
low_anagram = []
#for i in lst1:
    #for j in lst2:
        #if sorted(i.lower()) == sorted(j.lower()):
            #low_anagram.append((i, j))
#print(low_anagram)
low_anagram = [(i, j) for i in lst1 for j in lst2 if sorted(i.lower()) == sorted(j.lower())]
print('d) ',low_anagram)

#e) dict comp 
s = ['one', 'two', 'three']
pairs = {}
#for string in s:
#    pairs[string] = len(string)
pairs = {string: len(string) for string in s}
print('e) ',pairs)

#f) dict comp for vowels 
text = 'Hello World'
dict = {}
#for i, c in enumerate(text):
#    if c in 'aeiou':
#        dict[i] = c
dict = {i:c for i,c in enumerate(text) if c in 'aeiou'}
print('f) ',dict)

          

