# agents

## Minimax

Found in the `minimax_agent.py` file.

[Minimax](https://en.wikipedia.org/wiki/Minimax) is a fairly popular algorithm for zero-sum 2-player games. Minimax is a "planning" algorithm, which means it thinks about the possible states that could arise after taking an action. This is similar to how you might think about all the possible moves in a game state, how your opponent would respond to each move, how you would respond to your opponent's move, and so on. True Minimax requires searching the entire tree to find the best move for each state.

My implementation is H-Minimax (a more thorough explanation can be found in Chapter 5.4 of *Artificial Intelligence: A Modern Approach*, the textbook by Peter Norvig and Stuart J. Russell). Realistically, we cannot search the entire game tree because it would take too long. So, we use a maximum depth variable instead. If we find a terminal state before we reach the maximum depth, we can use the true value of that state (e.g. win == +1, lose == -1, draw == 0). If we haven't found a terminal state by the time we reach the maximum depth, we stop searching along that game trajectory and come up with an estimate for the value of that game state (some number in the range [-1, 1]). If you don't have a very good "estimate" function, you'll notice that the agent doesn't play very well in the beginning, but it'll play as best it can towards the end of the game.

At each state, Minimax selects an action with a time complexity of `O(b^d * e(s))`, where `b` is the number of branches, `d` is the max_depth, and `e(s)` is the cost of our estimate function for a state `s`. Note that the estimated state-values are all at the max depth. This means we can't reuse our calculations the next time we want to select an action because we want to estimate the value of states at a different depth.
