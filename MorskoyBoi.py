import random

class Ship:
    def __init__(self, start_row, start_col, end_row, end_col):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col

class Board:
    def __init__(self):
        self.size = 6
        self.ships = []

    def add_ship(self, ship):
        for s in self.ships:
            if self.is_overlap(ship, s):
                raise Exception("Не удается разместить корабль здесь, обнаружено перекрытие")
        self.ships.append(ship)

    def is_overlap(self, ship1, ship2):
        if (ship1.start_row <= ship2.start_row <= ship1.end_row or
            ship1.start_row <= ship2.end_row <= ship1.end_row) and \
           (ship1.start_col <= ship2.start_col <= ship1.end_col or
            ship1.start_col <= ship2.end_col <= ship1.end_col):
            return True
        return False

    def print_board(self):
        print("   | 1 | 2 | 3 | 4 | 5 | 6|")
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                row += "| " + self.get_cell_symbol(i, j) + " "
            print(row + "|")

    def get_cell_symbol(self, row, col):
        for ship in self.ships:
            if ship.start_row <= row <= ship.end_row and ship.start_col <= col <= ship.end_col:
                return "■"
        return "О"

def player_turn(board, target_board):
    row = int(input("Введите строку (1-6): ")) - 1
    col = int(input("Введите столбец (1-6): ")) - 1
    if target_board.get_cell_symbol(row, col) == "X":
        raise Exception("Вы уже стреляли в эту точку!")

    if target_board.get_cell_symbol(row, col) == "■":
        target_board.set_cell_symbol(row, col, "X")
        print("Ты попал!")
    else:
        target_board.set_cell_symbol(row, col, "T")
        print("Ты промахнулся!")

def computer_turn(board, target_board):
    row = random.randint(0, 5)
    col = random.randint(0, 5)

    if target_board.get_cell_symbol(row, col) == "X":
        computer_turn(board, target_board)

    if target_board.get_cell_symbol(row, col) == "■":
        target_board.set_cell_symbol(row, col, "X")
        print("Компьютер попал!")
    else:
        target_board.set_cell_symbol(row, col, "T")
        print("Компьютер промахнулся!")

def play_game():
    player_board = Board()
    computer_board = Board()

    # Place ships on boards
    player_board.add_ship(Ship(0, 0, 0, 2)) # 1 ship of length 3
    player_board.add_ship(Ship(1, 4, 1, 5)) # 2 ships of length 2
    player_board.add_ship(Ship(3, 0, 3, 0)) # 4 ships of length 1

    computer_board.add_ship(Ship(0, 0, 0, 2))
    computer_board.add_ship(Ship(1, 4, 1, 5))
    computer_board.add_ship(Ship(3, 0, 3, 0))

    while True:
        print("Поле игрока:")
        player_board.print_board()
        print("Поле противника:")
        computer_board.print_board()

        try:
            player_turn(player_board, computer_board)
            if check_winner(computer_board):
                print("Игрок победил")
                break

            computer_turn(computer_board, player_board)
            if check_winner(player_board):
                print("Компьютер победил")
                break
        except Exception as e:
            print("Error:", str(e))

def check_winner(board):
    for ship in board.ships:
        for row in range(ship.start_row, ship.end_row + 1):
            for col in range(ship.start_col, ship.end_col + 1):
                if board.get_cell_symbol(row, col) == "■":
                    return False
    return True

play_game()