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

### Monte Carlo Tree Search

Found in the `mcts.py` file.

Monte Carlo Tree Search is an algorithm similar to Flat Monte Carlo. It estimates the action-values for the current state by performing rollouts using uniform random selection. However, it also uses the rollouts to estimate the action-values for states along the rollout trajectory. This allows it to reuse the data gathered from previous rollout batches.

It does this by creating a tree where each node is a state in the Markov Decision Process. Each node keeps track of the number of times each action was visited from a rollout and the total value of all of those rollouts. For a more thorough understanding of how the MCTS algorithm works, see Browne, C., E. Powley, D. Whitehouse, S. Lucas, P. Cowling, Philipp Rohlfshagen, Stephen Tavener, Diego Perez Liebana, Spyridon Samothrakis and S. Colton. “A Survey of Monte Carlo Tree Search Methods.” IEEE Transactions on Computational Intelligence and AI in Games 4 (2012): 1-43.

I pitted the MCTS Agent against the Flat UCB agent with the following parameters 10 times:
- Flat UCB:
  - num_rollouts: 1000
  - exploration constant: 4
- MCTS:
  - num_rollouts: 1000
  
These were the results:
- MCTS won 3 games
- Flat UCB won 5 games
- The agents drew 2 games

These results can be explained by looking at the number of visits to each action after performing rollouts. Note that every time either agent is requested to select an action, it performs 1000 rollouts. The MCTS agent is able to reuse rollouts from previous batches of rollouts; however, the Flat UCB agent tries to select actions for rollouts to balance the exploration-exploitation tradeoff.

First, let's look at MCTS. If the root is the first state of a game, then nodes at depth=1 are the states resulting from the first action from the agent. The nodes at depth=2 are the states resulting from the first action from the agent and then the first action from the opponent. Note that since there are 7 actions to choose from for every state in Connect Four, with 1000 rollouts each node at depth=1 would be visited ~142 times if we used a uniform random policy to select actions. Each node at depth=2 would be visited ~20 times. This means that the next time we select an action (the second action from the agent) and need to perform 1000 rollouts, we've already performed ~20 rollouts from the state we're currently in (where both players have played a single action), so we have a total of ~1020 to estimate the action-values of that state. Since this isn't a huge increase in the number of rollouts, we're not going to see a much better performance than Flat Monte Carlo.

Now, recall that Flat UCB is able to discern between stronger and weaker moves by balancing the exploration-exploitation tradeoff. Since it visits weaker moves fewer times, it's able to use the extra rollouts to produce more accurate estimates of stronger moves (e.g. by ignoring 1 or 2 moves, it's able to visit remaining moves ~200 times). This is how it's able to do better than MCTS; it visits stronger moves more often than MCTS does and is thus able to discern between the best and second-best move more often.

### Upper Confidence Bounds for Trees (UCT)

Found in the `uct.py` file.

Upper Confidence Bounds for Trees (UCT) is essentially the same as MCTS. However, it applies the Upper Confidence Bound algorithm for move selection while traversing the tree in order to balance the exploration-exploitation tradeoff (this is known as the selection policy). Note that during rollouts, it still selects moves uniformly randomly (this is known as the default policy).

Recall that MCTS is able to use rollouts from previous batches to improve the estimate of action-values. UCT gets the same benefit; however it should have a slight improvement because it also balances the exploration-exploitation tradeoff.

I pitted the UCT agent against the Flat UCB agent with the following parameters 10 times:
- Flat UCB:
  - num_rollouts: 1000
  - exploration constant: 4
- UCT:
  - num_rollouts: 1000
  - exploration constant: 4
  
These were the results:
- Flat UCB won 4 games
- UCT won 4 games
- The agents drew 2 games

One possible explanation for these results is that just like MCTS, UCT is not able to utilize the extra rollouts very well since it only selects actions at every other level in the tree. This means that it has to throw away many of the rollouts. However, these results were quite inconsistent, so it is possible more tests need to be performed in order to better compare the two algorithms.


## Combinatorial Agents

### Minimax

Found in the `minimax_agent.py` file.

[Minimax](https://en.wikipedia.org/wiki/Minimax) is a fairly popular algorithm for zero-sum 2-player games. Minimax is a "planning" algorithm, which means it thinks about the possible states that could arise after taking an action. This is similar to how you might think about all the possible moves in a game state, how your opponent would respond to each move, how you would respond to your opponent's move, and so on. True Minimax requires searching the entire tree to find the best move for each state.

My implementation is H-Minimax (a more thorough explanation can be found in Chapter 5.4 of *Artificial Intelligence: A Modern Approach*, the textbook by Peter Norvig and Stuart J. Russell). Realistically, we cannot search the entire game tree because it would take too long. So, we use a maximum depth variable instead. If we find a terminal state before we reach the maximum depth, we can use the true value of that state (e.g. win == +1, lose == 0, draw == 1/2). If we haven't found a terminal state by the time we reach the maximum depth, we stop searching along that game trajectory and come up with an estimate for the value of that game state (some number in the range [0, 1]). If you don't have a very good "estimate" function, you'll notice that the agent doesn't play very well in the beginning, but it'll play as best it can towards the end of the game.

At each state, Minimax selects an action with a time complexity of `O(b^d * e(s))`, where `b` is the number of branches, `d` is the max_depth, and `e(s)` is the cost of our estimate function for a state `s`. Note that the estimated state-values are all at the max depth. This means we can't reuse our calculations the next time we want to select an action because we want to estimate the value of states at a different depth.

### Monte Carlo Proof Number Search

Found in the `mc_pns.py` file.

Monte Carlo Proof Number Search is a variation of Monte Carlo Tree Search that uses game-theory to limit search. It does this by assigning one of the following statuses to a game state:
1. Winning
2. Losing
3. Drawing
4. Exploring

If a game state is not "exploring", then it must be one of "winning", "losing," or "drawing." The agent performs a rollout like normal MCTS then and assigns a status to each node during the Backup Phase of Monte Carlo Tree Search. It uses the following rules to determine a status for a state:
1. If there is a single action in the current state that guarantees a win for the opponent, then the current state is considered "losing" for the player.
2. If there isn't an action that has been determined to be "winning" for the opponent but there is a single action that still needs to be explored, then the current state is considered "exploring" for the player. This makes sense because if all actions are losing but the one remaining action that still needs to be explored could guarantee a win, then we'd want to keep exploring.
3. If all actions lead to either a loss or a draw for the opponent, then the current state is considered "drawing." This is because an optimal agent would select the action that guarantees themselves a draw.
4. If all actions from a state lead to a loss for the opponent, then the current state is a guaranteed win for the agent. This is because no matter what action the opponent selects, it will result in their loss.

Once an agent has deemed an action as either winning, losing or drawing, it no longer needs to explore that action. This allows the agent to use its rollouts for any remaining actions.

After performing a number of rollouts, the agent must select an action. If it determines that an action is winning, then it immediately selects that action. Otherwise, it selects the action with the highest estimated action-value.

For a more thorough understanding of Monte Carlo Proof Number Search, see Section 5.4.2 entitled "Monte Carlo Proof-Number Search (MC-PNS)" of Browne, C., E. Powley, D. Whitehouse, S. Lucas, P. Cowling, Philipp Rohlfshagen, Stephen Tavener, Diego Perez Liebana, Spyridon Samothrakis and S. Colton. “A Survey of Monte Carlo Tree Search Methods.” IEEE Transactions on Computational Intelligence and AI in Games 4 (2012): 1-43. The authors state that using these game-theoretic guarantees allows the algorithm to 