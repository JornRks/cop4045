import csv
#a) top collabs
def display_top_collaborations(top_rated: str, top_casts: str) -> None:
    '''Displays the ranked top collaborations (Director, actor, # of movies)'''
    rated = open(top_rated, 'r', encoding='utf-8') #open read file
    rated_reader = csv.reader(rated)
    clean_movies = []
    for movie_info in rated_reader:#essentially 'for each line in the file'
        if movie_info[0] != 'Rank': #skips 1st line w labels
            name = movie_info[1]
            clean_movies.append(name) #gets name and appends it to clean movies

    casts = open(top_casts, 'r', encoding='utf-8') #same here
    casts_reader = csv.reader(casts)
    clean_casts = []
    for cast_info in casts_reader: #for line in the file, if the movie name is in clean_movies, append the movie name and 5 actors
        if cast_info[0] in clean_movies:
            clean_casts.append(cast_info[0:1] + cast_info[2:])

    top_collabs = {} #dict for top collabs, where actor and director tuple is key, movie count is value
    num_movies = 1
    for casts in clean_casts:
        director = casts[1] #gets dir name
        for actor in casts[2:]: #for each of 5 actors
            collab = (director, actor) #making collab tuple w director and actor
            if collab not in top_collabs: #if not in dict, add to dict w value 1, if it is, add 1 to movie count
                top_collabs[collab] = num_movies
            else:
                top_collabs[collab] += num_movies
    display = []
    for collab in top_collabs: #make a list of tuples to sory and display
        dis_director = collab[0] #get dir
        dis_actor = collab[1] #get actor
        dis_num = top_collabs[collab] #get movie count
        display.append((dis_num, dis_actor, dis_director)) #use this order so i can reverse tuple after sorting and its properly formatted

    display.sort(reverse=True) #this sorts the tuples using movie count, from high to low hence reverse
    sorted_display = []
    for tuple in display:
        sorted_display.append(tuple[::-1]) #appending reversed tuple to get proper format (dir, actor, movie count)

    print_display = sorted_display[0:10] #splice to only get the top 10
    for collab in print_display:
        print(collab) #print line by line



#b) top actors
def display_top_actors(gross_file: str, cast_file: str) -> None:
    '''Displays the top grossing actors ranked by revenue'''
    gross = open(gross_file, 'r', encoding='utf-8')  #open read file
    gross_reader = csv.reader(gross)

    clean_gross = [] #follows the same logic as above, skips 1st line, gets movie name and revenue, then adds to clean_gross
    for gross_info in gross_reader:
        if gross_info[0] != 'Rank':
            gross_name = gross_info[1]
            gross_total = gross_info[3]
            clean_gross.append((gross_name, gross_total))

    casts = open(cast_file, 'r', encoding='utf-8') #open read file
    casts_reader = csv.reader(casts)
    clean_actors = []
    for actor_info in casts_reader: #follows same logic, gets name, checks if its in clean_gross, if so appends the name, actors and revenue
        movie_name = actor_info[0]
        for gross_name, gross_total in clean_gross:
            if movie_name == gross_name:
                movie_rev = gross_total
                clean_actors.append([movie_name] + actor_info[3:] + [movie_rev])

    gross_dict = {} #dict for the actors and total revenue, actor name is key, revenue is value. follow same logic as top_collabs dict when it comes to assigning/adding key
    for movie in clean_actors:
        rev = int(movie[-1]) #makes revenue string an int
        for actor in movie[1:6]:
            if actor in gross_dict:
                gross_dict[actor] += rev
            else: 
                gross_dict[actor] = rev

    gross_display = [] #creates list of tuples wtih revenue and actor, revenue starts first so i can sort
    for actor in gross_dict:
        revenue = gross_dict[actor]
        gross_display.append((revenue, actor))
    gross_display.sort(reverse=True) #sorts by revenue form high to low
    sorted_gross = []
    for tuple in gross_display:
           sorted_gross.append(tuple[::-1]) #reverses tuples so the format is correct (actr, revenue)

    print_gross = sorted_gross[0:10] #same as above
    for actor in print_gross:
        print(actor)

#c) main function 
def main():
    rated = 'imdb-top-rated.csv' 
    grossing = 'imdb-top-grossing.csv'
    cast = 'imdb-top-casts.csv'

    print('top collabs:')
    display_top_collaborations(rated, cast)

    print('top grossing:')
    display_top_actors(grossing, cast)
main()

        
    

    


    





