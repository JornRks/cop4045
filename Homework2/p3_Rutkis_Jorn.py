#indexed by username
#a)add user
from testif import testif #for test if 

def add_user(sn: dict, username: str, fullname: str) -> bool: 
    '''Adds a user to the social network if not already added'''
    try:
        if username in sn: #if user alr in sn
            return False
        else: #if not add user with empty friends list
            sn[username] = (fullname, [])
            return True
    except Exception:
        print('Error wwhile adding user')
        raise
        
#b)add_friend
def add_friend(sn: dict, user1: str, user2: str) -> bool:
    '''Adds two users to eachothers friends lists'''
    try: 
        if user1 in sn and user2 in sn: #if both users are in sn, add to eachother freind list, else return false
            sn[user1][1].append(user2)
            sn[user2][1].append(user1)
            return True
        else:
            return False
    except Exception:
        print('Error while adding friend')
        raise

#c) get friends
def get_friends(sn: dict, user1: str, distance: int) -> list:
    '''Shows all friends of a user within a specified distance'''  
    try:
        im_friends = []
        if user1 not in sn: #if no user exists, returns empty list
            return im_friends
        im_friends = sn[user1][1].copy() #copy the immediate freinds of user 1, set as cur_friends
        cur_friends = im_friends
        cur_dist = 1 #firend distance is 1 as these are immediate friends
        while cur_dist < distance: #while current distance is less than user specified dist
            sec_friends = [] #store friends of  current friends
            for friend in cur_friends: #for each current friend
                for sec_friend in sn[friend][1]: #for each of the current friends friends
                    if sec_friend not in im_friends and sec_friend not in sec_friends and sec_friend != user1:
                        sec_friends.append(sec_friend) #if the scond friend isnt in im_friends, or sec_friends, and is not the user, add to sec_friends
            im_friends = im_friends + sec_friends #adds immediate and secnd friends together
            cur_friends = sec_friends #second friends become current for next iteration
            cur_dist += 1 #increase friend distance 
        return(im_friends)
    except Exception:
        print('Error getting friends')
        raise

#d) save_network
def save_network(filename: str, sn: dict) -> None:
    '''Saves social network to csv'''
    import csv
    csv_file = open(filename, 'w') #open write file
    for username in sn: #for each user in sn, write the user, name, and friends to csv
        friends = []
        user_info = username + ',' + sn[username][0] #user and full name
        for friend in sn[username][1]:
            friends.append(friend) #adds friends to lst

        friends_str = ','.join(friends) #turns friends list into a string
        csv_file.write(user_info + ',' + friends_str + '\n') #writes all user info to csv
    csv_file.flush() #save
    csv_file.close() #close

#e) Load network
def load_network(filename: str) -> dict:
    '''Loades a social network from a csv into a dictionary'''
    try:
        sn = {}
        csv_input = open(filename, 'r') #open read file
        for line in csv_input: #for each line of csv
            info = line.strip().split(',') #split into a list
            user = info[0] #get user
            name = info[1] #get name
            friends = info[2:] #get friends
            sn[user] = (name, friends) #adds to the sn dictionary, user is key, name/friends is value
        csv_input.flush()
        csv_input.close() #save and close
        return sn
    except FileNotFoundError: #if file not found, print error and raise exception
        print('File was not found')
        raise
    
#extra creddits testif module
def test() -> None:
    '''uses testif module from weeks 3,4 to test functions'''
    tested_sn = {}
    add_user(tested_sn, 'test', 'Test Mark')
    testif(add_user(tested_sn, 'jorn', 'Jorn Rutkis'), 'add_user test', 'adding succsess', 'adding failed' )
    testif(add_friend(tested_sn, 'jorn', 'test'), 'add_freind test', 'friend added', 'friend not added')
    testif(get_friends(tested_sn, 'jorn', 1), 'get_freinds test', 'friends found', 'friends not found')
    save_network('tested_sn.csv', tested_sn)
    check_file = open('tested_sn.csv', 'r')
    check_contents = check_file.read()
    check_file.close()
    testif('jorn' in check_contents, 'save network test', 'network was correctly saved', 'network wasnt saved correctly')
    loaded_sn = load_network('tested_sn.csv')
    testif(loaded_sn == tested_sn, 'load network test', 'network loaded correctly', 'network didnt load correctly')
    
#main to run/test functions
def main():
    sn = {
        'allen': ('Allen Bo', ['tom']),
        'tom': ('Tom Can', ['allen', 'rich', 'mary']),
        'rich': ('Rich Strike', ['tom', 'mary']),
        'mary': ('Mary Lamb', ['rich', 'tom'])
    }

    input_user = input('The user name you want: ')
    username = input_user
    input_fullname = input('Give full name: ')
    fullname = input_fullname

    #test add user
    if add_user(sn, username, fullname) == True:
        print('User added')
        print('New Network:')
        print(sn)
    else: 
        print('User not added')

    #test add_friend
    print('Add Friends: ')
    user1 = input('Add user 1: ')
    user2 = input('Add user 2: ')
    add_friend(sn, user1, user2)
    print('New Network:')
    print(sn)

    #test get_friends
    print('Get Friends: ')
    user_get = input('Add user 1: ')
    dist_str = input('Add friend distance: ')
    dist = int(dist_str)
    friends = get_friends(sn, user_get, dist)
    print(friends)

    #test save and load
    save_network('sn.csv', sn)
    loaded_sn = load_network('sn.csv')
    print(loaded_sn)
main()
test()