import cProfile

import gym
import linecache
import tracemalloc

from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager, SolutionManager
from connect_four.problem import ConnectFourGroupManager
from connect_four.problem.problem_manager import ProblemManager

env = gym.make('connect_four-v0')

# noinspection SpellCheckingInspection
cfgm = ConnectFourGroupManager(env_variables=env.env_variables)
vsm = VictorSolutionManager(env_variables=env.env_variables)


def move_evaluate_undo(problem_manager: ProblemManager, solution_manager: SolutionManager):
    gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)

    gm.move(row=5, col=3)

    gm.undo_move()

gm = GraphManager(player=0, problem_manager=cfgm, solution_manager=vsm)

cProfile.run(
    'gm.move(row=5, col=3)',
    sort="cumtime",
)

# def display_top(snap_shot, key_type='lineno', limit=100):
#     ss = snap_shot.filter_traces((
#         tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
#         tracemalloc.Filter(False, "<unknown>"),
#     ))
#     top_stats = ss.statistics(key_type)
#
#     print("Top %s lines" % limit)
#     for index, s in enumerate(top_stats[:limit], 1):
#         frame = s.traceback[0]
#         print("#%s: %s:%s: %.1f KiB"
#               % (index, frame.filename, frame.lineno, s.size / 1024))
#         line = linecache.getline(frame.filename, frame.lineno).strip()
#         if line:
#             print('    %s' % line)
#
#     other = top_stats[limit:]
#     if other:
#         size = sum(stat.size for stat in other)
#         print("%s other: %.1f KiB" % (len(other), size / 1024))
#     total = sum(stat.size for stat in top_stats)
#     print("Total allocated size: %.1f KiB" % (total / 1024))
#
#
# tracemalloc.start()
#
# cProfile.run(
#     'move_evaluate_undo(problem_manager=cfgm, solution_manager=vsm)',
#     sort="cumtime",
# )
#
# snapshot = tracemalloc.take_snapshot()
# display_top(snapshot)
