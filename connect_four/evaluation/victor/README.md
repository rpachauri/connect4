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

# References
1. [Allis, L.. “A Knowledge-Based Approach of Connect-Four.” J. Int. Comput. Games Assoc. 11 (1988): 165.](https://api.semanticscholar.org/CorpusID:24540039)
2. [Kishimoto, Akihiro, M. Winands, Martin Müller and Jahn-Takeshi Saito. “Game-Tree Search Using Proof Numbers: The First Twenty Years.” J. Int. Comput. Games Assoc. 35 (2012): 131-156.](https://api.semanticscholar.org/CorpusID:18449585)
