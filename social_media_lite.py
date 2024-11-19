import sqlite3
import csv
import time
import pandas as pd 
import numpy as np
import datetime
import pwinput

def login():
    check = False
    checkTwo = False
    username = ""
    while check == False:
        print("Enter your username: ")
        username = input()
        s = "SELECT * FROM users WHERE username =  '" + username + "'"
        cur.execute(s)
        f = cur.fetchall()
        if len(f) == 0:
            print("User not found")
        if len(f) != 0:
            check = True

    while checkTwo == False:
        password = pwinput.pwinput(prompt="Enter your password: ")
        s = "SELECT password FROM users WHERE username =  '" + username + "'"
        cur.execute(s)
        f = cur.fetchall()
        pass2 = f[0]
        result = ''.join(pass2)

        if password == result:
            print("Successful Login\n")
            return username
        else:
            print("Access Denied")

def getLatestPost(user_id):
    s = f"SELECT max(number) FROM posts"
    cur.execute(s)
    f = cur.fetchall()
    first = f[0]
    num = int(first[0])
    return num

def getLatestFollow(user_id):
    s = f"SELECT max(number) FROM followers"
    cur.execute(s)
    f = cur.fetchall()
    first = f[0]
    num = int(first[0])
    return num


def choose():
    getID = "SELECT user_id FROM users WHERE username = '" + username + "'"
    cur.execute(getID)
    f = cur.fetchall()
    user_idT = f[0]
    user_id = user_idT[0]
    print("Please choose an action: ")
    checkChoice = False
    logout = False
    while checkChoice == False:
        print("a) User Info \nb) Posts \nc) Follow \nd) Log-Out \n=>", end=" ")
        selection = input()
        if selection != 'a' and selection != 'b' and selection != 'c' and selection != 'd':
            print("Invalid Choice")
        else:
            checkChoice = True
    if selection == 'a':
        userInfo(username)
    elif selection == 'b':
        posts(username)
    elif selection == 'c':
        follow(user_id)
    elif selection == 'd':
        print("Goodbye!")
        exit()

def userInfo(username):
    userInfo = ("SELECT * FROM users WHERE username =  '" + username + "'")
    cur.execute(userInfo)
    s = cur.fetchall()
    f = s[0]
    userName = f[3]
    userResult = ''.join(userName)
    print("Username: " + userResult)
    created = f[5]
    createdResult = ''.join(created)
    print("Account Created: " + createdResult)
    first = f[6]
    firstResult = ''.join(first)
    print("First Name: " + firstResult)
    last = f[7]
    lastResult = ''.join(last)
    print("Last Name: " + lastResult)
    dob = f[8]
    dobResult = ''.join(dob)
    print("Date of Birth: " + dobResult)
    userInfoAction(username)

def userInfoAction(username):
    checkChoice = False
    while checkChoice == False:
        print("Choose an option \na) Go back\nb) Edit\n=>", end=" ")
        selection = input()
        if selection == 'b':
            edit(username) 
            checkChoice = True    
        elif selection == 'a':
            choose()
            checkChoice = True


def edit(username):
    check = False
    while (check == False):
        print("Available Columns:\nemail_id\npassword\nfirst_name\nlast_name\nbirth_date\n" + 
        "Which column would you like to edit? ")
        column = input() 
        s = "SELECT " + column + " FROM users"
        try:
            cur.execute(s)
        except sqlite3.OperationalError:
            print("Invalid Choice")
            edit(username)
        #f = cur.fetchall()
        setInfo = input("What would you like to set " + column + " to?")
        s2 = f"UPDATE users SET {column} = '{setInfo}' WHERE username = '{username}'"
        cur.execute(s2)
        check = True
    userInfoAction(username)

def posts(username):
    getID = "SELECT user_id FROM users WHERE username = '" + username + "'"
    cur.execute(getID)
    f = cur.fetchall()

    user_idT = f[0]
    #user_id = ''.join(user_idT)
    user_id = user_idT[0]
    print("Posts: ")
    s = f"SELECT posted_date, post FROM users JOIN posts ON users.user_id = posts.user_id WHERE posts.user_id = '{user_id}' ORDER BY posted_date ASC"
    cur.execute(s)
    f = cur.fetchall() 
    for tup in f:
        date = tup[0]
        post = tup[1]
        print(date + ": " + post + "\n")
    postAction(username, user_id)
    
def postAction(username, user_id):
    checkChoice = False
    while checkChoice == False:
        print("Choose an option \na) Go back\nb) Add Post\n=>", end=" ")
        selection = input()
        if selection == 'b':
            addPost(username, user_id)
            checkChoice = True    
        elif selection == 'a':
            choose()
            checkChoice = True

def addPost(username, user_id):
    post = input("Type new post: ")
    now = datetime.datetime.now().strftime("%m/%d/%Y")
    #nowString = df.format(now)

    number = getLatestPost(user_id) + 1
    s = f"INSERT INTO posts (number, user_id, post, posted_date) VALUES ('{number}', '{user_id}', '" + post + f"' , '{now}')"
    cur.execute(s)
    posts(username)

def follow(user_id):
    print("Followers: ")
    followerQuery = f"SELECT user_id FROM followers WHERE follow_id = {user_id}"
    cur.execute(followerQuery)
    followerListTemp = cur.fetchall()
    followerList = []
    i = 0
    for e in followerListTemp:
        getName = f"SELECT first_name, last_name FROM users JOIN followers on users.user_id = followers.follow_id WHERE follow_id = '{e[0]}'"
        cur.execute(getName)
        f = cur.fetchall()
        print(f[0][0] + " " + f[0][1])
        i += 1

    print("\nFollowing: ")

    followingQuery = f"SELECT follow_id FROM followers WHERE user_id = {user_id}"
    cur.execute(followingQuery)
    followingListTemp = cur.fetchall()
    followingList = []
    i = 0
    for e in followingListTemp:
        getName = f"SELECT first_name, last_name FROM users JOIN followers on users.user_id = followers.follow_id WHERE follow_id = '{e[0]}'"
        cur.execute(getName)
        f = cur.fetchall()
        print(f[0][0] + " " + f[0][1])
        i += 1
    followAction(user_id)

def followAction(user_id):
    checkChoice = False
    while checkChoice == False:
        print("Choose an option \na) Go back\nb) New Follow\n=>", end=" ")
        selection = input()
        if selection == 'b':
            newFollow(user_id)
            checkChoice = True    
        elif selection == 'a':
            choose()
            checkChoice = True

def newFollow(user_id):
    print("People not following: ")
    nums = [1, 2, 3, 4, 5, 6, 7, 8]
    nonFollowingQuery = f"SELECT follow_id FROM followers WHERE user_id = {user_id}"
    cur.execute(nonFollowingQuery)
    nonfollowingListTemp = cur.fetchall()
    nonfollowingList = []
    i = 0
    for e in nonfollowingListTemp:
        getName = f"SELECT users.user_id FROM users JOIN followers on users.user_id = followers.follow_id WHERE follow_id = '{e[0]}'"
        cur.execute(getName)
        f = cur.fetchall()
        nonfollowingList.append(f[0][0])
    finalList = []

    for e in nums:
        if e not in nonfollowingList:
            nonQuery = f"SELECT first_name, last_name, user_id FROM users WHERE user_id = {e}"
            cur.execute(nonQuery)
            f = cur.fetchall()
            print(f"{f[0][0]}"  + " " + f"{f[0][1]}" + ", User ID: " + f"{f[0][2]}")
            finalList.append(f[0][2])
    if len(finalList) == 0:
        print("You are currently following all users")
    else:
        check = False
        while check == False:
            choice = input("Id of person to follow: ")
            if int(choice) in finalList:
                check = True
                followQuery = f"INSERT INTO followers (number, user_id, follow_id) VALUES ('{getLatestPost(user_id) + 1}', '{user_id}', '{choice}')"
                cur.execute(followQuery)
            else:
                print("Invalid Selection")
        



    followAction(user_id)




    
        




if __name__ == "__main__":

    conn = sqlite3.connect('social_media.db', isolation_level = None)
    cur = conn.cursor()


    #get the username from a successful login attempt
    username = login()

    #get a valid action
    selection = choose()
    if (selection == False):
        print("Goodbye!")


    

    






"""
username = "tracysmith"
userInfo = ("SELECT * FROM users WHERE username =  '" + username + "'")
checkChoice = False
while checkChoice == False:
    print("a) User Info \nb) Posts \nc) Follow \nd) Log-Out \n=>", end=" ")
    selection = input()
    if selection == 'a' or selection == 'b' or selection == 'c' or selection == 'd':
        checkChoice = True
    else:
        print("Invalid Choice")

checkChoice = False

if selection == 'a':
    cur.execute(userInfo)
    s = cur.fetchall()
    f = s[0]
    userName = f[3]
    userResult = ''.join(userName)
    print("Username: " + userResult)
    created = f[5]
    createdResult = ''.join(created)
    print("Account Created: " + createdResult)
    first = f[6]
    firstResult = ''.join(first)
    print("First Name: " + firstResult)
    last = f[7]
    lastResult = ''.join(last)
    print("Last Name: " + lastResult)
    dob = f[8]
    dobResult = ''.join(dob)
    print("Date of Birth: " + dobResult)
    while (checkChoice == False):
        print("Choose an Option \na) Go Back \nb) Edit \n =>", end="")
        option = input()
        if option == 'a'
"""


