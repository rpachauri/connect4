import gym

from connect_four.agents import RandomAgent
from connect_four.evaluation.board import Board
from connect_four.evaluation.incremental_victor.graph.graph_manager import GraphManager
from connect_four.evaluation.incremental_victor.solution.victor_solution_manager import VictorSolutionManager
from connect_four.problem import ConnectFourGroupManager

env = gym.make('connect_four-v0')

for _ in range(0):
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
