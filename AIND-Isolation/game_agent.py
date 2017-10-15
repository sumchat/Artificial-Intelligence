"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass




def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # the score is proportional to the weighted average of 
    # 1.difference between move count difference of the player and opposition player
    # 2.move that blocks one of the move of opposition player
    # 3.distance of the player from the center. The parameters are chosen by trial and error.
       
    
   
    own_moves = len(game.get_legal_moves(player))
    opp1_moves = game.get_legal_moves(game.get_opponent(player))
    opp_moves = len(opp1_moves)
    diff = own_moves - opp_moves  
    
    location = game.get_player_location(player)    
    val = 0
    if (location in opp1_moves):
        val = 1
    plyrdistcenter = math.sqrt((location[0] - game.width//2)**2 + (location[1] - game.height//2)**2)    
    score = 0.5 * diff + 0.1 * plyrdistcenter +  0.3 * val
    return float(score)
    
    



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    #find the distance between 2 player locations. Assign high score to near locations
    location = game.get_player_location(player)
    opponentplayerloc = game.get_player_location(game.get_opponent(player))
    distance = math.sqrt((location[0] - opponentplayerloc[0])**2 + (location[1] - opponentplayerloc[1])**2)
    val = (game.width * game.height)// distance
   
    return val
    



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # high score for blocking moves -i.e. if the current player position is among the moves of opposition
    # if not blocking, find the distance between 2 locations.high score to near locations
    location = game.get_player_location(player)    
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    val = 0
    if (location in opp_moves):
        val = float("inf")
    else:
        location = game.get_player_location(player)
        opponentplayerloc = game.get_player_location(game.get_opponent(player))
        distance = math.sqrt((location[0] - opponentplayerloc[0])**2 + (location[1] - opponentplayerloc[1])**2)
        val = (game.width * game.height)// distance
       
    return float(val)
   


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            val = self.minimax(game, self.search_depth)           
            return val

        except SearchTimeout:            
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def Actions(self,game):               
        actions = game.get_legal_moves()
        return actions
    
    def MAXVALUE(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:                       
            raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game,self)            
       
        v = float("-inf")
        for action in self.Actions(game):
            newgame = game.forecast_move(action)
            v = max(v,self.MINVALUE(newgame,depth - 1))                    
        return v           
                    
    def MINVALUE(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            #return self.score(game,self)            
            raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game,self)      
                    
        v = float("inf")
        for action in self.Actions(game):
            #forecast_move returns a copy of the board with the move applied        
            newgame = game.forecast_move(action)                    
            v = min(v,self.MAXVALUE(newgame,depth - 1))                    
        return v                  
                    
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        
        maxscore = float("-inf")
        bestmove = (-1,-1)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        # TODO: finish this function!
        #get all the legal moves for the active player            
        moves = game.get_legal_moves(self)
        
        #It now tries to see the next future moves of the opposition iteratively. As the next move will be min's turn 
        #min will try to select the node with the minimum score.So the max need to select the move                    
        #for which the score will be highest of all possible Min's moves.            
        for move in moves:
           #active_player and inactive_player alternates on forecast_move call         
            newgame = game.forecast_move(move)             
            val =  self.MINVALUE(newgame,depth-1)             
            if val > maxscore:
                maxscore = val
                bestmove= move            
                          
        return bestmove

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!       
        best_move = (-1, -1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            iterative_depth = 1
            while True:
                best_move = self.alphabeta(game, iterative_depth)
                iterative_depth += 1

        except SearchTimeout:              
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration       
        return best_move

    def Actions(self,game):        
        actions = game.get_legal_moves()
        return actions
                    
    
    # here we are looking one level backwards. if the previous move is of MIN and 
    #assuming MIN will select the node with minimum score(beta), so if we visit a node with value greater than
    #what is stored in beta we will  not explore that node further.                
    def MAXVALUE(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:            
            raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game,self)      
                        
        v = float("-inf")
        for action in self.Actions(game):
            newgame = game.forecast_move(action)
            v = max(v,self.MINVALUE(newgame,depth - 1,alpha,beta))
            if (v >= beta):
                return v
            alpha = max(alpha,v)
        return v           
                    
    def MINVALUE(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:            
            raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game,self)         
                          
        v = float("inf")
        for action in self.Actions(game):
            #forecast_move returns a copy of the board with the move applied        
            newgame = game.forecast_move(action)                    
            v = min(v,self.MAXVALUE(newgame,depth - 1,alpha,beta))
            if (v <= alpha):
                return v
            beta = min(beta,v)
        return v                    
                    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        bestmove = (-1, -1)
        maxscore = float("-inf")
        moves = game.get_legal_moves()
        for move in moves:
            #active_player and inactive_player alternates on forecast_move call         
            newgame = game.forecast_move(move)                    
            val =  self.MINVALUE(newgame,depth -1,alpha,beta) 
            alpha = max(alpha,val)           
            if val > maxscore:
                maxscore = val
                bestmove= move                 
        return bestmove            
        
