# Movie Trivia by Logan Larocque

import psycopg2
conn = psycopg2.connect(dbname="IMDB",user="postgres")
cur = conn.cursor()

score = 0
question_number = 0

def ask_question():
    correct_ans = 0
    print("Generating next question...")
    cur.execute("SELECT primarytitle,primaryname,startyear FROM basics JOIN principals ON basics.tconst=principals.tconst JOIN namebasics ON principals.nconst=namebasics.nconst JOIN ratings ON basics.tconst=ratings.tconst WHERE principals.category IN ('actor','actress') AND startyear > 1990 AND numvotes > 500000 AND ordering = 1 ORDER BY RANDOM() LIMIT 2;")
    title_actor_year = cur.fetchall()
    releasedate_diff = title_actor_year[0][2] - title_actor_year[1][2]
    if releasedate_diff == 0:
        print("Pulled two movies with the same release year!")
        return 0
    elif releasedate_diff > 0:
        correct_ans = 2
    elif releasedate_diff < 0:
        correct_ans = 1
    response = int(input(f" \n Which movie released first? (to answer, type: 1 or 2 or 0 to quit) \n 1. {title_actor_year[0][0]}, Starring {title_actor_year[0][1]}, OR\n 2. {title_actor_year[1][0]}, Starring {title_actor_year[1][1]} \n\n"))
    if response == 0:
        global again
        again = 0
        print("Quitting")
        return 0
    while not response in (1,2):
        response = int(input(f" \n Invalid Response! Please only type 1 or 2! \n\n Which movie released first? \n 1. {title_actor_year[0][0]}, Starring {title_actor_year[0][1]}, OR\n 2. {title_actor_year[1][0]}, Starring {title_actor_year[1][1]} \n\n"))
    if response == correct_ans:
        print(f" \n Correct! {title_actor_year[0][0]} released in {title_actor_year[0][2]} and {title_actor_year[1][0]} released in {title_actor_year[1][2]} !")
        return 1
    else:
        print(f" \n Incorrect! {title_actor_year[0][0]} released in {title_actor_year[0][2]} and {title_actor_year[1][0]} released in {title_actor_year[1][2]} ! \n")
        return 0
print ("\n"*10)
print("Welcome to IMDB Movie Trivia by Logan Larocque!")
again = 1
while not again == 0:
    scorediff = ask_question()
    score += scorediff
    question_number += 1
    print(f" \n Your score is {score} out of {question_number}!")
