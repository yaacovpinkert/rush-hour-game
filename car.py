from typing import Tuple, List, Dict

Coordinates = Tuple[int, int]


class Car:
    """
    Represents a car in the Rush Hour game.
    Handles coordinates, possible moves, movement requirements, executing moves,
    and name retrieval.
    """

    MOVE_OFFSETS = {
        'u': (-1, 0),
        'd': (1, 0),
        'l': (0, -1),
        'r': (0, 1)
    }

    ORIENT_ALLOWED = {
        0: {'u', 'd'},  # Vertical
        1: {'l', 'r'}   # Horizontal
    }

    def __init__(self, name: str, length: int, location: Coordinates, 
                 orientation: int) -> None:
        """
        A constructor for a Car object.
        :param name: A string representing the car's name.
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head location (row,col).
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL).
        """
        self.__name = name
        self.__length = length
        self.__loc = location
        self.__orient = orientation

    def car_coordinates(self) -> List[Coordinates]:
        """
        :return: A list of coordinates the car is in.
        """
        row, col = self.__loc
        if self.__orient == 0:  # Vertical
            return [(row + i, col) for i in range(self.__length)]
        else:  # Horizontal
            return [(row, col + i) for i in range(self.__length)]

    def possible_moves(self) -> Dict[str, str]:
        """
        :return: A dictionary of strings describing possible movements 
                 permitted by this car.
        """
        if self.__orient == 0:
            return {'u': "cause the car to move one step up",
                    'd': "cause the car to move one step down"}
        else:
            return {'r': "cause the car to move one step to the right",
                    'l': "cause the car to move one step to the left"}

    def movement_requirements(self, move_key: str) -> List[Coordinates]:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for 
                 this move to be legal.
        """
        if (move_key not in Car.MOVE_OFFSETS or
                move_key not in Car.ORIENT_ALLOWED[self.__orient]):
            return []
        row_offset, col_offset = Car.MOVE_OFFSETS[move_key]
        row, col = self.__loc
        if move_key in ('d', 'r'):
            row += row_offset * self.__length
            col += col_offset * self.__length
        else:
            row += row_offset
            col += col_offset
        return [(row, col)]

    def move(self, move_key: str) -> bool:
        """ 
        This function moves the car.
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if move_key not in Car.ORIENT_ALLOWED[self.__orient]:
            return False
        row_offset, col_offset = Car.MOVE_OFFSETS[move_key]
        row, col = self.__loc
        self.__loc = (row + row_offset, col + col_offset)
        return True

    def get_name(self) -> str:
        """
        :return: The name of this car.
        """
        return self.__name
