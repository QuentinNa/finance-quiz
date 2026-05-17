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
# Function to ask the user to pick a category from a predefined list
def choose_category():
    # List of all available categories
    categories = ["All", "Accounting", "Corporate Finance", "Valuation", "Markets"]

    print()
    # Print the category selection prompt in yellow and bold
    print(Fore.YELLOW + Style.BRIGHT + "Choose a category:")

    # Loop through each category and print it with its corresponding number
    for i in range(len(categories)):
        print(Fore.CYAN + "  " + str(i + 1) + ". " + Fore.WHITE + categories[i])

    # Ask the user to enter a number between 1 and the total number of categories
    # read_integer_in_range handles validation and loops until a valid number is entered
    choice = read_integer_in_range("Your choice: ", 1, len(categories))

    # Return the category name at the index of the user's choice
    # (We subtract 1 because lists start at index 0 but our menu starts at 1)
    return categories[choice - 1]


# Function to ask the user to pick a difficulty level
# Works exaclty as the previous function but for difficulty
def choose_difficulty():

    # List of all available difficulty levels
    difficulties = ["All", "Beginner", "Intermediate", "Expert"]
    print()

    # Print the difficulty selection prompt
    print(Fore.YELLOW + Style.BRIGHT + "Choose a difficulty:")

    # Loop through each difficulty and print it with its corresponding number
    for i in range(len(difficulties)):
        print(Fore.CYAN + "  " + str(i + 1) + ". " + Fore.WHITE + difficulties[i])

    # Ask the user to enter a number between 1 and the total number of difficulties
    choice = read_integer_in_range("Your choice: ", 1, len(difficulties))

    # Return the difficulty name at the index of the user's choice
    return difficulties[choice - 1]


# Function to save the player's score to the scores.csv file
# Takes the player's name, category, difficulty, score and total as parameters
def save_score(player_name, category, difficulty, score, total):
    try:
        # Open the scores.csv file in append mode ("a") so we don't overwrite existing scores
        file = open("scores.csv", "a", newline="")
        writer = csv.writer(file)

        # Get the current date and time and format it as "YYYY-MM-DD HH:MM"
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Write one row with all the information about this game
        writer.writerow([date_string, player_name, category, difficulty, score, total])
        file.close()
        
    # If something goes wrong (file is locked, no permission, etc.) we just show a warning
    except IOError:
        print(Fore.YELLOW + "Warning: could not save the score.")


# Function to read all saved scores and display the top 5
# Uses medal emojis for the top 3 to make it more visual
def show_leaderboard():
    # Try to open and read the scores file
    try:
        file = open("scores.csv", "r", newline="")
        reader = csv.reader(file)
        # Store all the rows in a list so we can close the file straight away
        rows = list(reader)
        file.close()
    # If the file doesn't exist yet, no game has been played
    except FileNotFoundError:
        print(Fore.YELLOW + "No scores have been saved yet.")
        return

    # If the file is empty, no game has been played either
    if len(rows) == 0:
        print(Fore.YELLOW + "No scores have been saved yet.")
        return

    # Build a list of tuples with the percentage and row data so we can sort by score
    scored_rows = []
    for row in rows:
        # Skip any row that doesn't have exactly 6 columns (malformed data)
        if len(row) != 6:
            continue
        try:
            # Convert score and total to integers so we can do math with them
            score = int(row[4])
            total = int(row[5])
        # Skip the row if score or total can't be converted to an integer
        except ValueError:
            continue
        # Skip the row if total is 0 to avoid dividing by zero
        if total == 0:
            continue
        # Calculate the percentage and add all the data as a tuple to the list
        percentage = (score / total) * 100
        scored_rows.append((percentage, row[0], row[1], row[2], row[3], score, total))

    # Sort the list by percentage in descending order so the best score is first
    scored_rows.sort(reverse=True)

    print_title("Top 5 Scores")
    # Medal emojis for the first three places, blank for the rest
    medals = ["🥇", "🥈", "🥉", "  ", "  "]

    # Loop through the top 5 scores (or less if there aren't 5 yet)
    for i in range(min(5, len(scored_rows))):
        # Extract each piece of data from the tuple using its index
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

        # Print the full leaderboard row with medal, name, category, score and date
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


# Finally the function that runs one full game from start to finish
# It coordinates all the other functions in the right order
def play_quiz():
    clear_screen()
    print_title("New Game")

    # Ask the player for their name and keep asking until it's not empty
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

    # If no questions match the filters, we stop the game and go back to the menu
    if len(available_questions) == 0:
        print(Fore.RED + "Sorry, no questions are available for this combination.")
        return

    # Show how many questions are available with the selected filters
    print()
    print(
        Fore.WHITE
        + "There are "
        + Style.BRIGHT
        + str(len(available_questions))
        + Style.NORMAL
        + " questions available with these filters."
    )
    # Ask how many questions the player wants
    number_of_questions = read_integer_in_range(
        "How many questions do you want? ", 1, len(available_questions)
    )

    # Randomly pick the right number of questions so each game is different
    selected_questions = random.sample(available_questions, number_of_questions)

    # score counts correct answers, missed stores questions the player got wrong
    score = 0
    missed = []

    # Main game loop, we go through each selected question one by one
    for i in range(len(selected_questions)):
        # Get the current question and display it on screen
        question = selected_questions[i]
        display_question(question, i + 1, number_of_questions)
        answer = read_answer()

        # Compare the player's answer to the correct answer stored in the question dictionary
        if answer == question["correct"]:
            print(Fore.GREEN + Style.BRIGHT + "✓ Correct!")
            score = score + 1
        else:
            # We need the index of the correct letter to find the correct answer text
            # Example: if correct is "B", index is 1, so we get options[1]
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
            # Add the question to the missed list for the review at the end
            missed.append(question)

        # Show the running score in cyan
        print(Fore.CYAN + "Score so far: " + str(score) + "/" + str(i + 1))

    # ── END OF GAME ──────────────────────────────────────────────────────────
    print_title("Game Over")

    # Calculate the percentage to decide which comment to show
    percentage = (score / number_of_questions) * 100

    # Pick a color and comment based on the player's performance
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

    # Print the final score and comment in the appropriate color
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

    # Save the score to the csv file by calling save_score
    save_score(player_name, category, difficulty, score, number_of_questions)

    # ── REVIEW SECTION ───────────────────────────────────────────────────────
    # Only offer a review if the player got at least one question wrong
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

        # If the player says yes, loop through the missed questions and show the correct answer for each
        if review == "y":
            print_title("Review")
            for i in range(len(missed)):
                question = missed[i]
                correct_letter = question["correct"]
                letters = "ABCD"
                # Find the index of the correct letter to get the full answer text
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
