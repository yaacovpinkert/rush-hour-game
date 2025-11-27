from typing import Tuple, List, Optional
from car import Car

Coordinates = Tuple[int, int]


class Board:
    """
    The Board class represents the physical game board for the Rush Hour game,
    including: game environment, layout and structure, game state, interaction
    area, visual representation.
    """

    NUM_ROWS = 7
    NUM_COL = 7
    TARGET = (3, 7)

    def __init__(self) -> None:
        """
        A constructor for a Board object.
        """
        self.__board = [['_'] * Board.NUM_COL for i in range(Board.NUM_ROWS)]
        self.__board[Board.TARGET[0]].append('_')
        self.__cars_list = []
        return

    def __str__(self) -> str:
        """
        This function is called when a board object is to be printed.
        :return: A string representing the current status of the board.
        """
        rows = []
        for i in range(Board.NUM_ROWS):
            if i != Board.TARGET[0]:
                rows.append(" ".join(self.__board[i]))
            else:
                base = " ".join(self.__board[i][:Board.NUM_COL])
                target_val = self.__board[Board.TARGET[0]][Board.TARGET[1]]
                rows.append(base + " " + (target_val if target_val != '_' else 'E'))
        return "\n".join(rows)

    def cell_list(self) -> List[Coordinates]:
        """
        This function returns the coordinates of cells in this board.
        :return: list of coordinates.
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        return [(i, j) for i in range(Board.NUM_ROWS) for j in range(Board.NUM_COL)] + [Board.TARGET]


    def is_valid_move1(self, car: Car, direction: str) -> bool:
        """
        Helper function to check if a move is valid for a given car.
        :param car: The car for which to check the move.
        :param direction: The direction of the move.
        :return: True if the move is valid, False otherwise.
        """
        for row, col in car.movement_requirements(direction):
            if (row < 0 or col < 0 or
                row >= Board.NUM_ROWS or
                col >= Board.NUM_COL or
                self.__board[row][col] != "_"):
                if (row, col) == Board.TARGET:
                    return True
                return False
        return True

    def is_valid_move2(self, car: Car, move_key: str) -> (
            Optional)[List[Coordinates]]:
        """
        Helper function to check if a move is valid for a given car.
        :param car: The car for which to check the move.
        :param move_key: The direction of the move.
        :return: True if the move is valid, False otherwise.
        """
        moves = car.movement_requirements(move_key)

        for location in moves:
            if location == Board.TARGET:
                continue

            row, col = location
            if row < 0 or col < 0 or row >= Board.NUM_ROWS or col >= Board.NUM_COL:
                return False

            if self.cell_content(location) is not None:
                return False

        return moves

    def possible_moves(self) -> List[Tuple[str, str, str]]:
        """
        This function returns the legal moves of all cars in this board.
        :return: list of tuples of the form (name, move_key, description)
                 representing legal moves. The description should briefly
                 explain what is the movement represented by move_key.
        """
        legal = []
        for car in self.__cars_list:
            moves_dict = car.possible_moves()
            for direction, desc in moves_dict.items():
                if self.is_valid_move1(car, direction):
                    legal.append((car.get_name(), direction, desc))
        return legal

    def target_location(self) -> Coordinates:
        """
        This function returns the coordinates of the location that should be 
        filled for victory.
        :return: (row, col) of the goal location.
        """
        return Board.TARGET

    def cell_content(self, coordinates: Coordinates) -> Optional[str]:
        """
        Checks if the given coordinates are empty.
        :param coordinates: tuple of (row, col) of the coordinates to check.
        :return: The name of the car in "coordinates", None if it's empty.
        """
        row, col = coordinates
        return None if self.__board[row][col] == "_" else self.__board[row][col]


    def add_car(self, car: Car) -> bool:
        """
        Adds a car to the game.
        :param car: car object to add.
        :return: True upon success, False if failed.
        """
        # Unique name check
        if any(existing.get_name() == car.get_name() for existing in self.__cars_list):
            return False

        car_coor = car.car_coordinates()
        first = car_coor[0]
        last = car_coor[-1]

        # Boundary check
        if not (0 <= first[0] < Board.NUM_ROWS and
                0 <= first[1] < Board.NUM_COL):
            return False

        if not (0 <= last[0] < Board.NUM_ROWS and last[1] >= 0):
            return False

        if last[1] >= Board.NUM_COL and last != Board.TARGET:
            return False

        # Collision check
        for r, c in car_coor:
            if self.__board[r][c] != "_":
                return False

        # Insert
        self.__cars_list.append(car)
        name = car.get_name()
        for r, c in car_coor:
            self.__board[r][c] = name

        return True

    def find_car_by_name(self, name: str) -> Optional[Car]:
        """
        Finds a car object in __cars_list by its name.
        :param name: The name of the car to find.
        :return: The Car object if found, None otherwise.
        """
        for car in self.__cars_list:
            if name == car.get_name():
                return car
        return None

    def move_car(self, name: str, move_key: str) -> bool:
        """
        Moves car one step in a given direction.
        :param name: name of the car to move.
        :param move_key: the key of the required move.
        :return: True upon success, False otherwise.
        """
        # Check if the move_key is valid
        if move_key not in "udrl":
            return False

        # Find the car object with the given name
        car = self.find_car_by_name(name)
        if car is None:
            return False

        # Check if the car can make the specified move
        moves = self.is_valid_move2(car, move_key)
        if not moves:
            return False

        if not car.move(move_key):
            return False

        # Update board
        car_coor = car.car_coordinates()
        length = len(car_coor)

        for r, c in moves:
            self.__board[r][c] = name
            if move_key == 'd':
                self.__board[r - length][c] = '_'
            elif move_key == 'u':
                self.__board[r + length][c] = '_'
            elif move_key == 'r':
                self.__board[r][c - length] = '_'
            else:
                self.__board[r][c + length] = '_'

        return True
