import random
from user import User
from hangman_game import HangmanGame
from motivational_api import MotivationalAPI

def reset_game(game):
    game.guessed_letters.clear()
    game.wrong_guesses = 0
    game.choose_word(random.choice(game.categories))  # Choisir un nouveau mot

def main():
    print("Do you want to play a little game?")

    # Connexion initiale avec plusieurs tentatives
    attempts = 3  # Nombre de tentatives avant d'abandonner
    user = None
    while attempts > 0:
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Essayer de se connecter ou d'enregistrer l'utilisateur
        user = User.check_login(username, password)

        if user:
            print(f"Welcome, {username}!")
            break
        else:
            attempts -= 1
            print(f"Invalid credentials, {attempts} attempts remaining.")
    
    if not user:
        print("Too many failed attempts. Exiting...")
        return

    # Afficher les utilisateurs et leurs informations
    print("\nUsers in the database:")
    users = User.get_all_users()
    for u in users:
        print(f"ID: {u[0]}, Username: {u[1]}, Password: {u[2]}, Score: {u[3]}")

    game = HangmanGame()

    while True:
        # Choisir une catégorie par défaut ou selon l'utilisateur
        category = random.choice(game.categories)  # Choisir une catégorie par défaut
        print("Available categories:")
        for idx, cat in enumerate(game.categories):
            print(f"{idx + 1}. {cat}")

        category_choice = input("Choose a category by number or press Enter to random: ")
        if category_choice.isdigit() and 1 <= int(category_choice) <= len(game.categories):
            category = game.categories[int(category_choice) - 1]
        print(f"Category chosen: {category}")
        
        game.choose_word(category)  # Choisir un mot
        print(f"Category: {category}")

        while True:
            print(game.display_word())
            guess = input("Guess a letter: ").lower()
            result = game.guess(guess)

            if result is True:
                print("You won!")
                user.save_score(game.win_count)  # Save score after win
                print(MotivationalAPI.fetch_quote())  # Display motivational quote
                game.win_count += 1  # Increment win count

                if game.win_count == 5:
                    print("Congrats! You've won 5 times!")
                    print("You're a true champion! You managed to defeat The Cruel Jigsaw !")  # Funny winner message
                    break

                reset_game(game)
                break  # Retourner à la sélection de catégorie pour un nouveau jeu

            elif result is False:
                print("Game over! You lost.")
                game.print_jigsaw_face()  # Show Jigsaw face after losing
                reset_game(game)  # Reset the game for the next round
                break  # Break out of the current game loop and ask if they want to play again

            else:
                print("Keep guessing but be careful you might regret it...")

        # Ask to play again
        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != 'y':
            print("Thanks for playing!")
            break  # Quitter le jeu si l'utilisateur répond 'n'
        else:
            reset_game(game)  # Réinitialiser le jeu pour une nouvelle partie

if __name__ == "__main__":
    main()





