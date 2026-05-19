# Finance Quiz

A small quiz game written in Python that asks the player questions about finance. It runs in the terminal with colored text and keeps a list of the best scores.

## What the program does

When you start the program you see a menu with three choices:

1. Play the quiz
2. View the leaderboard
3. Quit

If you choose to play, the program asks for your name, then asks you to pick a category (Accounting, Corporate Finance, Valuation, Markets, or All) and a difficulty (Beginner, Intermediate, Expert, or All). You also choose how many questions you want to answer. The program then shows the questions one by one. For each question you type A, B, C, or D. At the end you see your score and you can review the questions you got wrong. Your score is saved into a file so you can see it later in the leaderboard.

## Files in the project

```
main.py         The Python program
questions.csv   The list of questions
scores.csv      The list of past scores (created automatically)
README.md       This file
```

## How to run the program

You need Python 3 installed on your computer. To run the program, open a terminal in the folder that contains `main.py` and type:

```
python3 main.py
```

On Windows you may need to type `python main.py` instead.

That is the only command. The program uses one library called colorama (for the colored text). If colorama is not already installed, the program installs it for you the first time you run it. You do not have to do anything by hand.

## How the code is organized

The program is one Python file, `main.py`. It is split into small functions, each one doing one thing. Here are the main ones:

* `load_questions()` reads `questions.csv` and puts every question into a list.
* `main_menu()` shows the menu and waits for the user's choice.
* `play_quiz()` runs one full game: ask name, ask category, ask difficulty, show questions, count the score, save it.
* `display_question()` prints one question with its four answers.
* `read_answer()` asks the user for A, B, C, or D and keeps asking if the answer is not valid.
* `save_score()` adds one line at the end of `scores.csv` with the date, the name, and the score.
* `show_leaderboard()` reads `scores.csv` and prints the top 5 scores.

There are also small helper functions like `clear_screen()` to clear the terminal and `print_title()` to print a nice frame around a title.

## The questions file

`questions.csv` is a normal CSV file. Each line is one question with these columns:

```
category, difficulty, question, option_a, option_b, option_c, option_d, correct
```

The last column is the letter of the correct answer (A, B, or C, or D). You can add your own questions by adding a new line to this file.

## The scores file

Every time a game ends, the program adds one line to `scores.csv` with this format:

```
date, name, category, difficulty, score, total
```

## Notes

* The questions are stored outside the code, in `questions.csv`, so it is easy to add new ones without changing the program.
* The program checks the user's input. If you type something that is not A, B, C, or D, it asks again instead of crashing.
* The leaderboard sorts the scores by percentage, so a 5/5 is better than a 9/10.
