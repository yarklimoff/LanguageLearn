import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        if from_x == to_x and from_y == to_y:
            return None #invalid move
        # todo more validation here
        if to_y >= from_y:
            return None

        if (to_x != from_x - 1 or to_y != from_y - 1) and (to_x != from_x + 1 or to_y != from_y -1):   #
            return None
        result = self.copy()
        result.board[to_y, to_x] = result.board[from_y, from_x]
        result.board[from_y, from_x] = 0

        return result

    def get_possible_moves(self) -> List['BoardState']:
        return [] # todo

    @property
    def is_game_finished(self) -> bool:
        ... # todo

    @property
    def get_winner(self) -> Optional[int]:
        ... # todo

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)

        for i in range(3):
            for j in range(1, 8, 2):
                board[i, (i + j) % 8] = -1
        for i in range(7, 4, -1):
            for j in range(0, 8, 2):
                board[i, (i + j + 1) % 8] = 1

        return BoardState(board, 1)
