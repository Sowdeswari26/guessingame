import streamlit as sl
import random

def guessing_game(mode):
    if mode == "User Guessing":
        sl.title("User Guessing Mode")
        sl.subheader("Rules:")
        sl.write("1) The computer has chosen a random three-digit number.")
        sl.write("2) You have 10 attempts to guess the number correctly.")

        target_number = random.randint(100, 999)
        attempts = 10

        if 'attempts_left' not in sl.session_state:
            sl.session_state.attempts_left = attempts
            sl.session_state.success = False

        guess = sl.number_input("Enter your guess (three-digit number):", min_value=100, max_value=999, step=1)

        if sl.button("Submit Guess") and not sl.session_state.success and sl.session_state.attempts_left > 0:
            sl.session_state.attempts_left -= 1

            if guess == target_number:
                sl.success("Congratulations! You've guessed the correct number!")
                sl.session_state.success = True
            elif guess < target_number:
                sl.warning("Too low! Try a higher number.")
            else:
                sl.warning("Too high! Try a lower number.")

            if sl.session_state.attempts_left == 0 and not sl.session_state.success:
                sl.error(f"Game over! The correct number was {target_number}.")

        sl.write(f"Attempts left: {sl.session_state.attempts_left}")

    elif mode == "Computer Guessing":
        sl.title("Computer Guessing Mode")
        sl.subheader("Rules:")
        sl.write("1) You choose a three-digit number (keep it secret).")
        sl.write("2) The computer will try to guess your number within 10 attempts.")

        user_number = sl.number_input("Enter a number between 100 and 999 for the computer to guess:", min_value=100, max_value=999, step=1)

        if 'low' not in sl.session_state:
            sl.session_state.low = 100
            sl.session_state.high = 999
            sl.session_state.attempts_left = 10
            sl.session_state.computer_guess = None

        if sl.session_state.attempts_left > 0 and user_number:
            sl.session_state.computer_guess = random.randint(sl.session_state.low, sl.session_state.high)
            sl.write(f"Computer's guess: {sl.session_state.computer_guess}")

            if sl.session_state.computer_guess == user_number:
                sl.success("The computer guessed your number correctly!")
                sl.session_state.attempts_left = 0  
            else:
                feedback = sl.radio("Is the computer's guess too high or too low?", ["Too Low", "Too High"])
                if feedback == "Too Low":
                    sl.session_state.low = sl.session_state.computer_guess + 1
                elif feedback == "Too High":
                    sl.session_state.high = sl.session_state.computer_guess - 1
                sl.session_state.attempts_left -= 1

            
            sl.write(f"Attempts left for the computer: {sl.session_state.attempts_left}")

        if sl.session_state.attempts_left == 0 and sl.session_state.computer_guess != user_number:
            sl.error(f"The computer couldn't guess your number in 10 attempts. Your number was {user_number}.")

# Main application
sl.title("Three-Digit Guessing Game")
mode = sl.radio("Choose Mode", ["User Guessing", "Computer Guessing"])

if sl.button("Start Game"):
    sl.session_state.clear()  
    guessing_game(mode)