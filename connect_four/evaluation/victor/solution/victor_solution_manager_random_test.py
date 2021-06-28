import gym

from connect_four.agents import RandomAgent
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.solution import VictorSolutionManager

env = gym.make('connect_four-v0')

for _ in range(100):
    obs = env.reset()
    env.render()

    random_agent = RandomAgent()
    vsm = VictorSolutionManager(env_variables=env.env_variables)

    done = False
    last_action = None
    player_turn = 0
    moves = []
    env_variables_by_move = [env.env_variables]

    while not done:
        board = Board(env_variables=env.env_variables)
        initial_solutions = VictorSolutionManager._find_all_solutions(board=board)

        action = random_agent.action(env, last_action)
        _, reward, done, _ = env.step(action)
        print("action = ", action)
        env.render()

        if done:
            break
        placed_row = env._find_highest_token(column=action)
        moves.append((player_turn, placed_row, action))
        env_variables_by_move.append(env.env_variables)

        board = Board(env_variables=env.env_variables)
        final_solutions = VictorSolutionManager._find_all_solutions(board=board)

        want_removed_solutions = initial_solutions - final_solutions
        want_added_solutions = final_solutions - initial_solutions
        got_removed_solutions, got_added_solutions = vsm.move(player=player_turn, row=placed_row, col=action)

        assert want_removed_solutions == got_removed_solutions
        assert want_added_solutions == got_added_solutions

        player_turn = 1 - player_turn

    while moves:
        player, row, col = moves.pop()
        env_variables = env_variables_by_move.pop()
        env.reset(env_variables)
        env.render()
        print("player, row, col =", player, row, col)
        board = Board(env_variables=env_variables)

        final_solutions = VictorSolutionManager._find_all_solutions(board=board)
        board.state[player][row][col] = 0
        initial_solutions = VictorSolutionManager._find_all_solutions(board=board)

        want_added_solutions = initial_solutions - final_solutions
        want_removed_solutions = final_solutions - initial_solutions
        got_added_solutions, got_removed_solutions = vsm.undo_move()

        assert want_added_solutions == got_added_solutions
        assert want_removed_solutions == got_removed_solutions

