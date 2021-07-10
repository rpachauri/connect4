import gym

from connect_four.agents import difficult_connect_four_positions
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.dbm_transposition_table import DBMTranspositionTable
from connect_four.transposition.sqlite_transposition_table import SQLiteTranspositionTable

env = gym.make('connect_four-v0')

env.reset(env_variables=difficult_connect_four_positions.diagram_13_6)

diagram_13_6_transposition = ConnectFourHasher(env=env).hash()


dbm_tt = DBMTranspositionTable(phi_file="connect_four_phi", delta_file="connect_four_delta")
sqlite_tt = SQLiteTranspositionTable(database_file="connect_four.db")

i = 0
for transposition in dbm_tt.phi_db.keys():
    transposition = transposition.decode(encoding='utf-8')
    if transposition == diagram_13_6_transposition:
        print(transposition)
    # It's possible for a transposition to exist in phi_db and not delta_db.
    if transposition in dbm_tt:
        phi, delta = dbm_tt.retrieve(transposition=transposition)
        sqlite_tt.save(transposition=transposition, phi=phi, delta=delta)
        i = i + 1
        print(i)

dbm_tt.close()
sqlite_tt.close()
