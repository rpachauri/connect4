# agents

## General Planning Agents

### Flat Monte Carlo

Found in the `flat_monte_carlo.py` file.

Flat Monte Carlo is an algorithm that estimates the action-values for the current state by performing rollouts using uniform random selection. Essentially, the agent selects an action to find a sample estimate for. It then obtains the sample estimate by playing the game using random moves. It does this `num_rollouts` times and then selects the action with the highest action-value estimate.

### Flat UCB

Found in the `flat_ucb.py` file.

Flat UCB is an algorithm similar to Flat Monte Carlo that estimates the action-values for the current state by performing rollouts. However, it selects actions for each rollout using the UCB algorithm. This allows it to better balance the exploration-exploitation tradeoff. I found that for this environment, the agent performed reasonably well when setting the exploration constant to 4. You can try a smaller exploration constant (which will make the agent more greedy) or a higher exploration constant (which will make it more like a uniform random selection policy).

I did some play testing with the Flat UCB Agent setting the number of rollouts to 1000 and the exploration constant to 4 to figure out how well the UCB action selection policy worked. There are 7 actions to choose from for every state in Connect Four. This means that if we used a uniform random policy to select actions for rollouts, each action would be visited ~142 times. Towards the beginning of the game, I found that the agent selected actions nearly uniformly. This makes sense because it's hard to distinguish stronger moves from weaker moves towards the beginning of the game. I noticed that towards the end of the game, Flat UCB explored losing moves much less than winning moves. If a column became full, then UCB figured out that placing a token in that column was losing and would redistribute rollouts among the remaining actions (e.g. visiting the full columns ~30 times while visiting the remaining columns ~200 times).

I pitted the Flat UCB agent against the Flat Monte Carlo agent with the following parameters 10 times:
- Flat Monte Carlo
  - num_rollouts: 1000
- Flat UCB:
  - num_rollouts: 1000
  - exploration constant: 4
  
These were the results:
- Flat UCB won 6 games
- Flat Monte Carlo won 2 games
- The agents drew 2 games

## Combinatorial Agents

### Minimax

Found in the `minimax_agent.py` file.

[Minimax](https://en.wikipedia.org/wiki/Minimax) is a fairly popular algorithm for zero-sum 2-player games. Minimax is a "planning" algorithm, which means it thinks about the possible states that could arise after taking an action. This is similar to how you might think about all the possible moves in a game state, how your opponent would respond to each move, how you would respond to your opponent's move, and so on. True Minimax requires searching the entire tree to find the best move for each state.

My implementation is H-Minimax (a more thorough explanation can be found in Chapter 5.4 of *Artificial Intelligence: A Modern Approach*, the textbook by Peter Norvig and Stuart J. Russell). Realistically, we cannot search the entire game tree because it would take too long. So, we use a maximum depth variable instead. If we find a terminal state before we reach the maximum depth, we can use the true value of that state (e.g. win == +1, lose == 0, draw == 1/2). If we haven't found a terminal state by the time we reach the maximum depth, we stop searching along that game trajectory and come up with an estimate for the value of that game state (some number in the range [0, 1]). If you don't have a very good "estimate" function, you'll notice that the agent doesn't play very well in the beginning, but it'll play as best it can towards the end of the game.

At each state, Minimax selects an action with a time complexity of `O(b^d * e(s))`, where `b` is the number of branches, `d` is the max_depth, and `e(s)` is the cost of our estimate function for a state `s`. Note that the estimated state-values are all at the max depth. This means we can't reuse our calculations the next time we want to select an action because we want to estimate the value of states at a different depth.