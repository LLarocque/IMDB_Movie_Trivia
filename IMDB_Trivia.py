# Movie Trivia by Logan Larocque


import random

#connect to PSQL
import psycopg2
conn = psycopg2.connect(dbname="IMDB",user="postgres")
cur = conn.cursor()

#Generate a list of title constants from basics table
cur.execute("SELECT tconst FROM basics WHERE startyear > 1970;")
tconsts = cur.fetchall()

score = 0
question_number = 0
again = 1
correct_ans = 0

def gen_releasedate_question(reldate_consts):
    print("Please wait, generating a trivia question...")
    #Pick two random entries from our tconst list
    random_indices = random.sample(range(0,len(reldate_consts)),2)
    tconst1 = reldate_consts[random_indices[0]][0]
    tconst2 = reldate_consts[random_indices[1]][0]

    #Pull data from our table using the selected title constants
    cur.execute(f"SELECT primarytitle,primaryname,startyear FROM basics JOIN principals ON basics.tconst=principals.tconst JOIN namebasics ON principals.nconst=namebasics.nconst JOIN ratings ON basics.tconst=ratings.tconst WHERE basics.tconst='{tconst1}' AND ordering=1 LIMIT 1;")
    title_actor_year1 = cur.fetchall()
    cur.execute(f"SELECT primarytitle,primaryname,startyear FROM basics JOIN principals ON basics.tconst=principals.tconst JOIN namebasics ON principals.nconst=namebasics.nconst JOIN ratings ON basics.tconst=ratings.tconst WHERE basics.tconst='{tconst2}' AND ordering=1 LIMIT 1;")
    title_actor_year2 = cur.fetchall()

    #Compare release dates
    releasedate_diff = title_actor_year1[0][2] - title_actor_year2[0][2]
    if releasedate_diff > 0:
        correct_ans = 2
    elif releasedate_diff < 0:
        correct_ans = 1
    else:
        print("Pulled two movies with the same year, trying again...")
        correct_ans = 0
    return title_actor_year1, title_actor_year2, correct_ans

def ask_releasedate_question(title_actor_year1, title_actor_year2, correct_ans):
    #Ask the question, prompt for answer
    response = int(input(f" \n Which movie released first? (to answer, type: 1 or 2 or 0 to quit) \n 1. {title_actor_year1[0][0]}, Starring {title_actor_year1[0][1]}, OR\n 2. {title_actor_year2[0][0]}, Starring {title_actor_year2[0][1]} \n\n"))
    if response == 0:
        global again
        again = 0
        print("Quitting")
        return 0
    while not response in (1,2):
        response = int(input(f" \n Invalid Response! Please only type 1 or 2! \n\n Which movie released first? \n 1. {title_actor_year1[0][0]}, Starring {title_actor_year1[0][1]}, OR\n 2. {title_actor_year2[0][0]}, Starring {title_actor_year2[0][1]} \n\n"))
    if response == correct_ans:
        print(f" \n Correct! {title_actor_year1[0][0]} released in {title_actor_year1[0][2]} and {title_actor_year2[0][0]} released in {title_actor_year2[0][2]} !")
        return 1
    else:
        print(f" \n Incorrect! {title_actor_year1[0][0]} released in {title_actor_year1[0][2]} and {title_actor_year2[0][0]} released in {title_actor_year2[0][2]} ! \n")
        return 0
    
print ("\n"*5)
print("Welcome to IMDB Movie Trivia by Logan Larocque!")
while not again == 0:
    while correct_ans == 0:
        title_actor_year1, title_actor_year2, correct_ans = gen_releasedate_question(tconsts)
        
    scorediff = ask_releasedate_question(title_actor_year1, title_actor_year2, correct_ans)
    score += scorediff
    if again==1:
        question_number += 1
    correct_ans = 0
    print(f" \n Your score is {score} out of {question_number}!")
