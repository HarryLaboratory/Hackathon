# Harry
1. Your hackathon project is great! The code is well-structured, clean, and easy to read. The idea is well-thought-out, and the execution and results are good.
2. From your code and your comments, it's clear that you understand what you've done and how you've done it.
3. However I noticed a couple of issues in your code:
    1. When updating the user's score, your program creates a new user each time, so every time my score as username "raquel" changes, a new raquel user is created in your user table, instead of updating the existing one.
    2. There is a small issue with your usage of bcrypt. The way the password is beeing hashed for data storage at the sign in session is different from the way it is hashed for login verification. So the login raise an error in your code and break the run of the code.
4. Kol Hakavod! You've done a wonderful job!
