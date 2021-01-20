from collections import namedtuple

Branch = namedtuple("Branch", ["forced_square", "simple_plan"])
Fork = namedtuple("Fork", ["branches", "simple_plan"])
