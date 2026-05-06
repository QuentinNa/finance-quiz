# Auto installation of colorama if it's not already installed, anyone can run it without installing manually the colorama package
import subprocess
import sys

try:
    # Try to import colorama normally first
    from colorama import Fore, Back, Style, init
except ImportError:
    # If the import fails, colorama is not installed yet
    print("Installing colorama (one time setup)...")
    # replace the user writting in the terminal
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    # Now it's installed we can import it
    from colorama import Fore, Back, Style, init

# Import the modules we need
# random lets us shuffle the questions so each game is different
import random

# datetime lets us record the date when we save scores
from datetime import datetime

# csv handles reading and writing the scores and questions files
import csv

# os lets us use feature of the operating system
import os

# Initializing colorama so colors work on all platforms
init(autoreset=True)

# autoreset=True means colors automatically reset after each print, which is convenient
init(autoreset=True)


# Function the clear the terminal screen so each section starts fresh
# os.name is "nt" on Windows and "posix" on Mac/Linux/Replit
def clear_screen():
    # detect if it's a windows or mac/linux/replit
    # windows device
    if os.name == "nt":
        # command to clear the console on windows
        os.system("cls")
    # mac/linux/replit
    else:
        # command to clear the console on mac/linux/replit
        os.system("clear")


# Function to print a nicely framed title using box drawing
# Fore to change the color of the text
def print_title(text):
    width = len(text) + 4
    print()
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * width + "╗")
    print(Fore.CYAN + Style.BRIGHT + "║  " + text + "  ║")
    print(Fore.CYAN + Style.BRIGHT + "╚" + "═" * width + "╝")
    print()


# Function to print a thin separator line for in-game sections
def print_separator():
    # Fore to change the color of the text
    print(Fore.BLUE + "─" * 60)


# Function to display a progress bar showing how far the player is in the quiz
# Filled blocks for completed questions and empty blocks for remaining
def print_progress_bar(current, total):
    filled = "▓" * current
    empty = "░" * (total - current)
    percentage = round((current / total) * 100)
    print(Fore.MAGENTA + "Progress: [" + filled + empty + "] " + str(percentage) + "%")


# Function to load the question bank from the external CSV file
# Storing questions outside the code means we can add or edit them without touching the program at all
def load_questions():
    questions = []
    # Try to open the file and read the questions
    try:
        # Open the file in read mode
        file = open("questions.csv", "r", newline="")
        # Create a CSV reader object
        reader = csv.reader(file)
        # The first row is the header (column names), we skip it
        next(reader)
        # Loop through each remaining row and build a question dictionary
        for row in reader:
            # A valid row has 8 columns; skip anything malformed
            if len(row) != 8:
                # go to the next row
                continue
            # Build a dictionary with the question data
            question = {
                "category": row[0],
                "difficulty": row[1],
                "question": row[2],
                "options": [row[3], row[4], row[5], row[6]],
                "correct": row[7],
            }
            # Add the question to the list of questions
            questions.append(question)
        # Close the file
        file.close()
    # If the file doesn't exist we print an error message and exit
    except FileNotFoundError:
        print(
            Fore.RED
            + "Error: questions.csv not found. Please make sure the file exists."
        )
        # Exit the program
        exit()
    # It returns the list of questions as output of the function
    return questions

# Load the questions once at the start of the program
question_bank = load_questions()

# Function to display one question on screen with its options labeled A, B, C, D
# Includes a small header showing question number, category, and difficulty
def display_question(question, question_number, total_questions):
    print()
    print_progress_bar(question_number - 1, total_questions)
    print()
    # Header with category and difficulty in yellow
    print(
        Fore.YELLOW
        + "Question "
        + str(question_number)
        + "/"
        + str(total_questions)
        + "  |  "
        + question["category"]
        + "  |  "
        + question["difficulty"]
    )
    # A thin separator line by calling the function
    print_separator()
    # The question itself in white/bright
    print(Style.BRIGHT + question["question"])
    print()
    # The four options, each in cyan with a bold letter
    letters = "ABCD"
     # Loop through the options and print them with the corresponding letter
    for i in range(len(question["options"])):
        print(
            Fore.CYAN
            + Style.BRIGHT
            + "  "
            + letters[i]
            + ". "
            + Style.NORMAL
            + Fore.WHITE
            + question["options"][i]
        )
    print()


# Function to read the user's answer and keep asking until it's a valid letter (A, B, C, D)
def read_answer():
    # Loop until a valid answer is given
    while True:
        # Try to read the input and if the user presses Ctrl+D (EOF) we print an error message and exit
        try:
            # strip is for removing any extra spaces and upper is for converting to uppercase
            # upper is for converting to uppercase
            answer = input(Fore.GREEN + "Your answer (A/B/C/D): ").strip().upper()
        except EOFError:
            print(Fore.RED + "Error: no input received. Exiting.")
            exit()

        if answer in ["A", "B", "C", "D"]:
            return answer
        # If the answer is not A, B, C, or D we print an error message and ask again
        print(Fore.RED + "✗ Please enter A, B, C, or D.")


# Function to read an integer from the user, looping until it's valid and in the given range
def read_integer_in_range(prompt, minimum, maximum):
    # Loop until a valid answer is given
    while True:
        # Try to read the input, if the user presses Ctrl+D (EOF) we print an error message and exit
        try:
            # Convert the input to an integer
            value = int(input(Fore.GREEN + prompt))
        
        except ValueError:
            print(Fore.RED + "✗ Please enter a valid integer.")
            # Continue to the next iteration of the loop
            continue
        # If the user presses Ctrl+D (EOF) we print an error message and exit
        except EOFError:
            print(Fore.RED + "Error: no input received. Exiting.")
            exit()

        if value < minimum or value > maximum:
            print(
                Fore.RED
                + "✗ The number must be between "
                + str(minimum)
                + " and "
                + str(maximum)
                + "."
            )
            # Continue to the next iteration of the loop
            continue
        # If the input is valid and in the range we return the value
        return value


# Function to filter the question bank to only keep questions matching a category and difficulty
def filter_questions(category, difficulty):
    # Create an empty list to store the filtered questions
    filtered = []
    # Loop through each question in the question bank
    for question in question_bank:
        # If the category is not "All" and the question's category does not match the selected category, skip it
        if category != "All" and question["category"] != category:
            # Continue to the next iteration of the loop
            continue
        # If the difficulty is not "All" and the question's difficulty does not match the selected difficulty, skip it
        if difficulty != "All" and question["difficulty"] != difficulty:
            # Continue to the next iteration of the loop
            continue
         # If the question matches the selected category and difficulty, add it to the filtered list
        filtered.append(question)
    # Return the filtered list of questions
    return filtered

######################################################################################################################################################
#HERE#
# Ask the user to pick a category from a list
def choose_category():
    categories = ["All", "Accounting", "Corporate Finance", "Valuation", "Markets"]
    print()
    print(Fore.YELLOW + Style.BRIGHT + "Choose a category:")
    for i in range(len(categories)):
        print(Fore.CYAN + "  " + str(i + 1) + ". " + Fore.WHITE + categories[i])
    choice = read_integer_in_range("Your choice: ", 1, len(categories))
    return categories[choice - 1]


# Ask the user to pick a difficulty level
def choose_difficulty():
    difficulties = ["All", "Beginner", "Intermediate", "Expert"]
    print()
    print(Fore.YELLOW + Style.BRIGHT + "Choose a difficulty:")
    for i in range(len(difficulties)):
        print(Fore.CYAN + "  " + str(i + 1) + ". " + Fore.WHITE + difficulties[i])
    choice = read_integer_in_range("Your choice: ", 1, len(difficulties))
    return difficulties[choice - 1]


# Save the player's score to the CSV file
def save_score(player_name, category, difficulty, score, total):
    try:
        file = open("scores.csv", "a", newline="")
        writer = csv.writer(file)
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M")
        writer.writerow([date_string, player_name, category, difficulty, score, total])
        file.close()
    except IOError:
        print(Fore.YELLOW + "Warning: could not save the score.")


# Read all saved scores and display the top 5
# Uses medals 🥇🥈🥉 for the top 3 to make it more visual
def show_leaderboard():
    try:
        file = open("scores.csv", "r", newline="")
        reader = csv.reader(file)
        rows = list(reader)
        file.close()
    except FileNotFoundError:
        print(Fore.YELLOW + "No scores have been saved yet.")
        return

    if len(rows) == 0:
        print(Fore.YELLOW + "No scores have been saved yet.")
        return

    # Build a list of (percentage, row data) so we can sort by percentage
    scored_rows = []
    for row in rows:
        if len(row) != 6:
            continue
        try:
            score = int(row[4])
            total = int(row[5])
        except ValueError:
            continue
        if total == 0:
            continue
        percentage = (score / total) * 100
        scored_rows.append((percentage, row[0], row[1], row[2], row[3], score, total))

    scored_rows.sort(reverse=True)

    print_title("Top 5 Scores")
    # Medal symbols for the first three places, blank for the rest
    medals = ["🥇", "🥈", "🥉", "  ", "  "]
    for i in range(min(5, len(scored_rows))):
        percentage = scored_rows[i][0]
        date_string = scored_rows[i][1]
        player_name = scored_rows[i][2]
        category = scored_rows[i][3]
        difficulty = scored_rows[i][4]
        score = scored_rows[i][5]
        total = scored_rows[i][6]
        # Color based on rank: gold for 1st, silver for 2nd, bronze for 3rd, white for the rest
        if i == 0:
            color = Fore.YELLOW + Style.BRIGHT
        elif i == 1:
            color = Fore.WHITE + Style.BRIGHT
        elif i == 2:
            color = Fore.RED
        else:
            color = Fore.WHITE
        print(
            color
            + medals[i]
            + " "
            + player_name
            + " - "
            + category
            + " ("
            + difficulty
            + ")"
            + " - "
            + str(score)
            + "/"
            + str(total)
            + " ("
            + str(round(percentage, 1))
            + "%)"
            + "  "
            + Fore.BLUE
            + date_string
        )


# Run one full quiz game from start to finish
def play_quiz():
    clear_screen()
    print_title("New Game")

    # Ask the player for their name
    while True:
        try:
            player_name = input(Fore.GREEN + "Enter your name: ").strip()
        except EOFError:
            print(Fore.RED + "Error: no input received. Exiting.")
            exit()
        if player_name != "":
            break
        print(Fore.RED + "✗ Name cannot be empty.")

    # Welcome the player by name
    print(
        Fore.MAGENTA
        + "Welcome, "
        + Style.BRIGHT
        + player_name
        + Style.NORMAL
        + "! Let's get started."
    )

    # Let the player choose category and difficulty
    category = choose_category()
    difficulty = choose_difficulty()

    # Filter the question bank using the player's choices
    available_questions = filter_questions(category, difficulty)

    if len(available_questions) == 0:
        print(Fore.RED + "Sorry, no questions are available for this combination.")
        return

    # Let the player choose how many questions
    print()
    print(
        Fore.WHITE
        + "There are "
        + Style.BRIGHT
        + str(len(available_questions))
        + Style.NORMAL
        + " questions available with these filters."
    )
    number_of_questions = read_integer_in_range(
        "How many questions do you want? ", 1, len(available_questions)
    )

    # Shuffle and select the questions
    selected_questions = random.sample(available_questions, number_of_questions)

    # Track the score and missed questions
    score = 0
    missed = []

    # Loop through the selected questions
    for i in range(len(selected_questions)):
        question = selected_questions[i]
        display_question(question, i + 1, number_of_questions)
        answer = read_answer()

        if answer == question["correct"]:
            print(Fore.GREEN + Style.BRIGHT + "✓ Correct!")
            score = score + 1
        else:
            correct_letter = question["correct"]
            letters = "ABCD"
            correct_index = letters.index(correct_letter)
            print(
                Fore.RED
                + Style.BRIGHT
                + "✗ Wrong. "
                + Style.NORMAL
                + Fore.WHITE
                + "The correct answer was "
                + Fore.GREEN
                + Style.BRIGHT
                + correct_letter
                + Fore.WHITE
                + Style.NORMAL
                + ": "
                + question["options"][correct_index]
            )
            missed.append(question)

        # Show the running score in cyan
        print(Fore.CYAN + "Score so far: " + str(score) + "/" + str(i + 1))

    # End of game summary
    print_title("Game Over")

    # Final score in big colored letters depending on performance
    percentage = (score / number_of_questions) * 100

    if percentage == 100:
        color = Fore.YELLOW + Style.BRIGHT
        comment = "🌟 Perfect score! Excellent work."
    elif percentage >= 75:
        color = Fore.GREEN + Style.BRIGHT
        comment = "🎯 Great job!"
    elif percentage >= 50:
        color = Fore.CYAN
        comment = "👍 Not bad, keep practicing."
    else:
        color = Fore.RED
        comment = "📚 Time to review the basics."

    print(
        color
        + "Final score: "
        + str(score)
        + "/"
        + str(number_of_questions)
        + " ("
        + str(round(percentage, 1))
        + "%)"
    )
    print(color + comment)
    print()

    # Save the score
    save_score(player_name, category, difficulty, score, number_of_questions)

    # Offer a review of missed questions
    if len(missed) > 0:
        print()
        try:
            review = (
                input(Fore.GREEN + "Review the questions you missed? (y/n): ")
                .strip()
                .lower()
            )
        except EOFError:
            review = "n"
        if review == "y":
            print_title("Review")
            for i in range(len(missed)):
                question = missed[i]
                correct_letter = question["correct"]
                letters = "ABCD"
                correct_index = letters.index(correct_letter)
                print(Fore.YELLOW + "Q: " + Fore.WHITE + question["question"])
                print(
                    Fore.GREEN
                    + "Correct answer: "
                    + correct_letter
                    + ". "
                    + question["options"][correct_index]
                )
                print()


# The main menu
def main_menu():
    clear_screen()
    # ASCII-art style banner
    print(Fore.CYAN + Style.BRIGHT)
    print("╔══════════════════════════════════════════╗")
    print("║                                          ║")
    print("║               FINANCE  QUIZ              ║")
    print("║                                          ║")
    print("║   Test your knowledge in Accounting,     ║")
    print("║   Corporate Finance, Valuation & Markets ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print(Style.RESET_ALL)

    while True:
        print()
        print(Fore.YELLOW + Style.BRIGHT + "Main Menu:")
        print(Fore.CYAN + "  1. " + Fore.WHITE + "Play the quiz")
        print(Fore.CYAN + "  2. " + Fore.WHITE + "View leaderboard")
        print(Fore.CYAN + "  3. " + Fore.WHITE + "Quit")

        choice = read_integer_in_range("Your choice: ", 1, 3)

        if choice == 1:
            play_quiz()
        elif choice == 2:
            show_leaderboard()
        else:
            print()
            print(Fore.MAGENTA + Style.BRIGHT + "Thanks for playing! Goodbye 👋")
            break


# Start the program
main_menu()
