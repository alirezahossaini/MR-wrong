from random import randrange

board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

center  =   (4,)
edge    =   (1,3,5,7)
corner  =   (0,2,6,8)

order = {'C': 'corner','K': 'center', 'K-K': 'edge', 'K-E': 'common', 'E': 'center', 'E-E': 'common', 'E-K': 'common'}

player_moves = player = computer = ''

player_first = flag = True

def print_board():
    x = 1
    for i in board:
        char = ' '
        end = " | "
        if x % 3 == 0: end = " \n----------\n"
        if x == 9: end = ''
        if i in ('X', 'O'): char = i
        x += 1
        print(char, end=end)

def select_nut():
    while 1:
        choose = input("\n Entekhab Konid X Ya O :  ")
        if choose in ('X', 'x'): return 'X', 'O'
        if choose in ('O', 'o'): return 'O', 'X'
        print("Vorodi Eshtebah Ast ! ")

def ask_player(word):
    while 1:
        choose = input(word + "Bazi Mikonid " + "? (B/N) :  ")
        if choose in ('B', 'b'): return True
        elif choose in ('N', 'n'): return False
        else: print("Vorodi Eshtebah Ast ! ")

def space_exist():
    return (board.count('X') + board.count('O') != 9)

def can_move(move):
    if board[move] not in ('X', 'O'): return True
    return False

def submit_player_move(move):
    global player_moves
    divider = '-'
    if player_moves == '': divider = ''
    current = ''
    if move in corner: current = 'K'
    elif move in edge: current = 'E'
    else: current = 'C'
    player_moves +=  divider + current

def find_common_point():
    points = [i for i in range(9) if board[i] == player]
    states = [[],[]]

    for i in range(2):
        point = points[i]
        for state in winners:
            if point in state:
                acceptable = True
                for j in state:
                    if board[j] == computer:
                        acceptable = False
                if acceptable:
                    states[i] += list(state)

    common_point = list(set(states[0]).intersection(set(states[1])))
    if common_point == []: return None
    return common_point[0]

def can_win(player):
    places = [i for i in board if i not in ('X', 'O')]

    for i in places:
        board[i] = player
        for state in winners:
            win = True
            for j in state:
                if board[j] != player:
                    win = False
                    break
            if win:
                return (True, i)
        board[i] = i

    return(False, -1)

def desired_move(domain = board):
    for state in winners:
        can_go = False
        positions = []
        for j in state:
            if board[j] == player:
                can_go = False
                break
            elif board[j] == computer:
                can_go = True
            else:
                positions.append(j)

        if can_go:
            points = [i for i in positions if i in domain]
            if len(points) > 0:
                return points[randrange(len(positions))]

    places = [i for i in board if i not in ('X', 'O')]
    return places[randrange(len(places))]

def computer_move():
    if player_first:
        if  player_moves in order:

            move_type = order[player_moves]

            if move_type == 'center':
                return make_move(4, computer, False)

            elif move_type == 'corner':
                move = corner[randrange(4)]
                return make_move(move, computer, False)

            elif move_type == 'edge':
                    winning = can_win(player)
                    if winning[0]:
                        return make_move(winning[1], computer, False)
                    return make_move(desired_move(edge), computer, False)

            elif move_type == 'common':
                winning = can_win(player)
                if winning[0]:
                    return make_move(winning[1], computer, False)
                point = find_common_point()
                if point != None:
                    return make_move(point, computer, False)
    
    if board.count(computer) == 0:
        moves = (0, 2, 4, 6, 8)
        while 1:
            move = moves[randrange(5)]
            if can_move(move):
                return make_move(move, computer, False)
                
    winning = can_win(computer)
    if winning[0]:
        return make_move(winning[1], computer, True)

    winning = can_win(player)
    if winning[0]:
        return make_move(winning[1], computer, False)

    else:
        return make_move(desired_move(), computer, False)

def has_player_won(move):
    board[move] = player
    for state in winners:
        win = True
        for j in state:
            if board[j] != player:
                win = False
                break
        if win:
            return True
    return False

def player_move():
    while 1:
        move = input("\nHarekat Shoma Beyne [1,9] :  ")
        if move not in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            print("Vorodi Eshtebah Ast ! ")
            continue

        move = int(move)-1
        if can_move(move):
            submit_player_move(move)
            return make_move(move, player, has_player_won(move))
        else:
            print("Khali Nist!")

def make_move(move, player, has_win):
    global board
    board[move] = player
    return "WIN" if has_win else False

while flag == True:
    print("\nPorozhe Dooz : Muhammad Mahdi Moghadassi"+"\n"+"Riyaziyyat Gosaste : Ostad MehrAli")
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    player, computer = select_nut()
    player_first = ask_player('Aval ')
    result = "Mosavi...!"
    you_win = "Tabrik Barande Shodid...!"
    you_lose = "Motasefam Bakhtid...!"

    if player_first:
        print_board()
        while space_exist():
            if player_move() == "WIN":
                result = you_win
                break
            if not space_exist(): break
            if computer_move() == "WIN":
                result = you_lose
                break
            print_board()
    else:
        while space_exist():
            if computer_move() == "WIN":
                result = you_lose
                break
            if not space_exist(): break
            print_board()
            if player_move() == "WIN":
                result = you_win
                break
    
    print_board()
    print("\n\n-----  || " + result + " ||  -----\n\n")

    flag = ask_player('Dobare ')

print("\n.......... $ Payan $ ..........\n")