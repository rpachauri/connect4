# Victor

Victor is an evaluator for Connect Four. It is based off of Victor Allis' work: A Knowledge-Based Approach of Connect-Four.

## Problems

In any given position, there are groups of four that the opponent can use to win. These are known as "problems", "threats" or just "groups". In an empty 6x7 board, each player has 69 such groups (even though neither player can immediately win with them).

## Solutions

There are 9 rules:
1. Claimeven
2. Baseinverse
3. Vertical
4. Aftereven
5. Lowinverse
6. Highinverse
7. Baseclaim
8. Before
9. Specialbefore

See Allis (1988) for how these rules are defined. In any given position, we can turn instances of these rules into "solutions" that can solve problems.
- In a position with White to move, Black tries to use a subset of the solutions available to them in order to refute all of White's threats.
- In a position with Black to move, White tries to use a subset of the solutions available to them in order to refute all of Black's threats AND somehow guarantee themselves a win.

In order to guarantee a win, White tries to employ "win conditions." Essentially, they are the same thing as rules; however, White can only use one win condition in a position.
- In fact, White *must* be able to use exactly one win condition in order for Victor to prove a position.

Note that not all solutions can be used together. In order to disprove/prove a position, the idea is:
- For Black: to find a subset of solutions that can all be used together and refute all of the opponents threats
- For White: to find a subset of solutions that can all be used together and with exactly one win condition and refute all of the opponents threats

# Improvements

## Dynamic Programming

Something I had a lot of fun with was the algorithm from Section 9.2 of “A Knowledge-Based Approach of Connect-Four” used to find a chosen set of solutions. It is a recursive backtracking algorithm that I was able to improve with dynamic programming. I've reproduced the algorithm below with some modifications for clarity. 

```{python}
def find_chosen_set(
        problem_to_solutions: Dict[Problem, Set[Solution]],    # All Problems mapped to all Solutions that solve them, unchanged.
        solution_to_problems: Dict[Solution, Set[Problem]],    # All Solutions mapped to all Problems they solve, unchanged.
        solution_to_solutions: Dict[Solution, Set[Solution]],  # All Solutions mapped to all Solutions they cannot be used with. Starts off as empty.
        problems_to_solve: Set[Problem],                       # All Problems that need to be solved.
        disallowed_solutions: Set[Solution],                   # All Solutions that cannot be combined with one of the Solutions in used_solutions.
        used_solutions: Set[Solution]                          # All Solutions that have already been used 
      ) -> Optional[Set[Solution]]:
    # Base Case.
    if not problems_to_solve:
        # If there are no problems, return the set of Solutions are currently using.
        return used_solutions.copy()
    
    # Recursive Case.
    most_difficult_problem = problem_with_fewest_solutions(
        problem_to_solutions=problem_to_solutions,  # All Problems and all Solutionst that solve them.
        problems_to_solve=problems_to_solve,        # All Problems that need to be solved.
        disallowed_solutions=disallowed_solutions,  # Exclude these solutions when counting.
    )
    usable_solutions = problem_to_solutions[most_difficult_problem].difference(disallowed_solutions)

    for solution in usable_solutions:
        # Dynamic Programming! Build solution_to_solutions incrementally and only when we need it.
        if solution not in solution_to_solutions:
            solution_to_solutions[solution] = find_disallowed_solutions(solution=solution, solutions=solution_to_problems.keys())

        # Choose.
        used_solutions.add(solution)
        # Recurse.
        chosen_set = find_chosen_set_dynamic_programming(
            problem_to_solutions=problem_to_solutions,
            solution_to_problems=solution_to_problems,
            solution_to_solutions=solution_to_solutions,
            problems_to_solve=problems_to_solve - solution_to_problems[solution],
            disallowed_solutions=disallowed_solutions.union(solution_to_solutions[solution]),
            used_solutions=used_solutions,
        )
        # Unchoose.
        used_solutions.remove(solution)

        if chosen_set is not None:
            return chosen_set
```
The first three parameters are what make up the Node Graph (explained in Section 9.2 of “A Knowledge-Based Approach of Connect-Four”). Essentially, we connect all Problems to all Solutions that solve them, connect all Solutions to all Problems they solve and connect all Solutions that cannot be combined with each other. Since the number of Solutions is the dominating factor, the true bottleneck is in connecting Solutions to each other. In addition, the search is usually quite fast because lots of positions can't be solved (i.e. we quickly find a subset of Problems that cannot be solved using any combination of the Solutions avaiable).

My algorithm takes advantage of this by only connecting Solutions to each other when we need to. Since most evaluations will be able to stop early, we end up not having to build the entire graph is those positions. 

# References
1. [Allis, L.. “A Knowledge-Based Approach of Connect-Four.” J. Int. Comput. Games Assoc. 11 (1988): 165.](https://api.semanticscholar.org/CorpusID:24540039)
2. [Kishimoto, Akihiro, M. Winands, Martin Müller and Jahn-Takeshi Saito. “Game-Tree Search Using Proof Numbers: The First Twenty Years.” J. Int. Comput. Games Assoc. 35 (2012): 131-156.](https://api.semanticscholar.org/CorpusID:18449585)
