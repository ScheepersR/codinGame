class TickTackToe:
    def __init__(self):
        self.board = [[None for x in range(3)] for y in range(3)]

    def play_move(self, player, pos):
        assert self.board[pos[0]][pos[1]] == None
        self.board[pos[0]][pos[1]] = player

    def backtrack_move(self, player, pos):
        assert self.board[pos[0]][pos[1]] == player
        self.board[pos[0]][pos[1]] = None
    
    def valid_moves(self):
        return [(x,y) for x in range(3) for y in range(3) if self.board[x][y] is None]
    
    def winner(self):
        #check rows
        for row in range(3):
            if self.board[row] == [1,1,1]:
                return 1
            elif self.board[row] == [0,0,0]:
                return 0
        
        #check cols
        transposed = list(zip(*self.board))
        for col in range(3):
            if transposed[col] == (1,1,1):
                return 1
            elif transposed[col] == (0,0,0):
                return 0
        
        #check diagonals
        diag1 = [self.board[x][x] for x in range(3)]
        diag2 = [self.board[2-x][x] for x in range(3)]

        for d in [diag1, diag2]:
            if d == [1,1,1]:
                return 1
            elif d == [0,0,0]:
                return 0
        
        return None

    def min(self, a, b):
        if self.winner() == 1:
            return 1, None
        if self.winner() == 0:
            return -1, None

        valid_moves = self.valid_moves()

        if not valid_moves:
            #draw
            return 0, None
        
        min_outcome = 2
        best_move = None
        for move in valid_moves:
            self.play_move(0, move)
            outcome, _ = self.max(a, b)
            if outcome < min_outcome:
                best_move = move
                min_outcome = outcome
            self.backtrack_move(0, move)

            #a,b pruning
            if min_outcome <= a:
                return (min_outcome, best_move)

            if min_outcome < b:
                b = min_outcome
    
        return (min_outcome, best_move)

    def max(self, a, b):
        if self.winner() == 1:
            return 1, None
        if self.winner() == 0:
            return -1, None

        valid_moves = self.valid_moves()

        if not valid_moves:
            #draw
            return 0, None

        max_outcome = -2
        best_move = None
        for move in valid_moves:
            self.play_move(1, move)
            outcome, _ = self.min(a, b)
            if outcome > max_outcome:
                best_move = move
                max_outcome = outcome
            self.backtrack_move(1, move)

            #a,b pruning
            if max_outcome >= b:
                return (max_outcome, best_move)

            if max_outcome > a:
                a = max_outcome

        return (max_outcome, best_move)

