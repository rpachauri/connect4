import gym

from connect_four.agents import RandomAgent
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
from connect_four.problem import ConnectFourGroupManager

env = gym.make('connect_four-v0')

for _ in range(100):
    obs = env.reset()
    env.render()

    random_agent = RandomAgent()
    cfgm = ConnectFourGroupManager(env_variables=env.env_variables)
    vsm = VictorSolutionManager(env_variables=env.env_variables)
    gm = GraphManager(player=0, problem_manager=cfgm, solution_manager=vsm)

    done = False
    last_action = None
    player_turn = 0
    moves = []
    env_variables_by_move = [env.env_variables]

    while not done:
        board = Board(env_variables=env.env_variables)
        # initial_gm = GraphManager(
        #     player=env.env_variables.player_turn,
        #     problem_manager=ConnectFourGroupManager(env_variables=env.env_variables),
        #     solution_manager=VictorSolutionManager(env_variables=env.env_variables),
        # )
        # initial_solutions = VictorSolutionManager(env_variables=env.env_variables).get_solutions()

        action = random_agent.action(env, last_action)
        _, reward, done, _ = env.step(action)
        print("action = ", action)
        env.render()

        if done:
            break
        placed_row = env._find_highest_token(column=action)
        moves.append((player_turn, placed_row, action))
        env_variables_by_move.append(env.env_variables)

        gm.move(row=placed_row, col=action)

        want_gm = GraphManager(
            player=player_turn,
            problem_manager=ConnectFourGroupManager(env_variables=env.env_variables),
            solution_manager=VictorSolutionManager(env_variables=env.env_variables),
        )
        assert want_gm.problem_to_solutions == gm.problem_to_solutions
        assert want_gm.solution_to_problems == gm.solution_to_problems
        assert want_gm.solution_to_solutions == gm.solution_to_solutions
        # final_solutions = VictorSolutionManager(env_variables=env.env_variables).get_solutions()

        # want_removed_solutions = initial_solutions - final_solutions
        # want_added_solutions = final_solutions - initial_solutions
        # got_removed_solutions, got_added_solutions = vsm.move(player=player_turn, row=placed_row, col=action)

        # assert want_removed_solutions == got_removed_solutions
        # assert want_added_solutions == got_added_solutions

        player_turn = 1 - player_turn

    env.reset(env_variables=env_variables_by_move.pop())
    while moves:
        # final_solutions = VictorSolutionManager(env_variables=env.env_variables).get_solutions()
        player, row, col = moves.pop()
        print("player, row, col =", player, row, col)
        env_variables = env_variables_by_move.pop()
        env.reset(env_variables)
        env.render()

        gm.undo_move()

        want_gm = GraphManager(
            player=player_turn,
            problem_manager=ConnectFourGroupManager(env_variables=env.env_variables),
            solution_manager=VictorSolutionManager(env_variables=env.env_variables),
        )
        assert want_gm.problem_to_solutions == gm.problem_to_solutions
        assert want_gm.solution_to_problems == gm.solution_to_problems
        assert want_gm.solution_to_solutions == gm.solution_to_solutions

        # want_added_solutions = initial_solutions - final_solutions
        # want_removed_solutions = final_solutions - initial_solutions
        # got_added_solutions, got_removed_solutions = vsm.undo_move()
        #
        # assert want_added_solutions == got_added_solutions
        # assert want_removed_solutions == got_removed_solutions
