from board import Board
from car import Car
import sys
from helper import *


class Game:
    """
    Handles the main game loop for Rush Hour.
    Manages user turns, validates input, and moves cars on the board.
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.
        """
        # Check if game is finished
        if self.__board.cell_content(self.__board.target_location()) is not None:
            return False

        # Display possible moves to the user
        moves = self.__board.possible_moves()
        print("\nPossible moves for this turn:")
        for idx, (car, key, desc) in enumerate(moves, start=1):
            print(f" {idx}. {car},{key}: {desc}")

        # Get user input
        input_user = input("\nEnter car and direction (e.g., R,r) or '!' to quit: ")
        if input_user == "!":
            return False

        # Validate user input
        while (len(input_user) != 3 or input_user[0] not in "YBOGWR" or
               input_user[1] != ',' or input_user[2] not in "udrl"):
            if "!" == input_user:
                return False
            input_user = input("Invalid input. Enter car and direction (e.g., R,r): ")

        car_name, move_key = input_user[0], input_user[2]

        # Attempt to move car
        if not self.__board.move_car(car_name, move_key):
            print("\nImpossible move! Try again.")
            print(self.__board)
            return

        print(f"\nMove '{car_name} -> {move_key}' executed successfully!")
        print("=========================================================")
        print("=========================================================")
        print("\nCurrent board:\n")
        print(self.__board)
        return

    def play(self) -> None:
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print("Welcome to the Rush Hour Game!\n")
        print(self.__board)
        while self.__single_turn() is not False:
            continue
        print("\nGame over!")


def validate_cars(dictionary, board):
    # Iterate over each car in the loaded configuration
    for car in dictionary:

        # Skip cars with invalid names
        if car not in "YBOGWR" or len(car) != 1:
            continue

        # Skip cars with invalid lengths
        elif dictionary[car][0] < 2 or dictionary[car][0] > 4:
            continue

        # Extract car attributes from the configuration
        length = dictionary[car][0]
        location = tuple(dictionary[car][1])
        orient = dictionary[car][2]

        # Add the car to the board
        board.add_car(Car(car, length, location, orient))


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    # implement your code and erase the "pass"
    file_name = sys.argv[1]
    board1 = Board()
    cars_dict = load_json(file_name)
    validate_cars(cars_dict, board1)
    Game(board1).play()
