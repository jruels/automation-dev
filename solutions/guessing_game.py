import random

def play_guessing_game():
    # Get player name
    name = input("Welcome! Please enter your name: ")
    print(f"\nHello {name}! Let's play a number guessing game.")
    
    # Generate random target number between 1 and 50
    target = random.randint(1, 50)
    print("I've picked a number between 1 and 50.")
    
    # Initialize attempts counter
    attempts = 0
    max_attempts = 5
    
    # Main game loop
    while attempts < max_attempts:
        # Get player's guess
        guess = input(f"\nAttempt {attempts + 1}/{max_attempts}. Enter your guess (or 'q' to quit): ")
        
        # Check for quit condition
        if guess.lower() == 'q':
            print(f"\nThanks for playing, {name}! The number was {target}.")
            return
        
        # Validate input
        try:
            guess = int(guess)
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")
            continue
        
        # Increment attempts
        attempts += 1
        
        # Check guess
        if guess == target:
            print(f"\nCongratulations {name}! You win!")
            print(f"You found the number in {attempts} attempts!")
            return
        elif guess < target:
            print("Under")
        else:
            print("Over")
        
        # Check if player has run out of attempts
        if attempts == max_attempts:
            print(f"\nSorry {name}, you lost! The number was {target}.")
            return

# Start the game
if __name__ == "__main__":
    play_guessing_game()