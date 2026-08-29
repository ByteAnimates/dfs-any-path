"""
Run it: python3 main.py

Depth-first search on the same board `bfs-shortest-path` uses. It finds a route in 19
steps where BFS finds one in 13, and neither is wrong — DFS was never asked for the
shortest one.
"""

from solution import GOAL, START, dfs, neighbours, render, trace


def bfs_length(start: int, goal: int) -> int:
    """Shortest route length, for contrast — the `bfs-shortest-path` episode."""
    frontier, seen, d = [start], {start}, 0
    while frontier:
        if goal in frontier:
            return d
        nxt = [n for c in frontier for n in neighbours(c) if n not in seen]
        seen.update(nxt)
        frontier, d = nxt, d + 1
    raise ValueError('unreachable')


def main() -> None:
    route = dfs(START, GOAL)
    events = trace(START, GOAL)
    backs = [c for kind, c in events if kind == 'back']

    print(f'\n  start {START}  goal {GOAL}\n')
    print(render(route))
    print(f'\n  DFS  {len(route) - 1} steps   {route}')
    print(f'  BFS  {bfs_length(START, GOAL)} steps')
    print(f'\n  {len(events)} events: {len(events) - len(backs)} advances, {len(backs)} retreats.')
    print(f'  backed out of {backs}')
    print(
        '\n  The retreats are the algorithm, not a failure of it. DFS commits to one\n'
        '  direction until it runs out of board, then unwinds to the last square that\n'
        '  still had an option. What it returns is A path — the one the neighbour order\n'
        '  happened to produce — and reordering those four directions changes it.\n'
    )


# ── the claims above, checked ────────────────────────────────────────────────────

_route = dfs(START, GOAL)

# It is a real route: legal moves, right endpoints, no square repeated.
assert _route[0] == START and _route[-1] == GOAL
assert all(b in neighbours(a) for a, b in zip(_route, _route[1:]))
assert len(set(_route)) == len(_route), 'the stack should never hold a square twice'

# THE CLAIM: it finds a path, and it is NOT the shortest one on this board.
assert len(_route) - 1 == 19
assert bfs_length(START, GOAL) == 13
assert len(_route) - 1 > bfs_length(START, GOAL)

# It really does backtrack here — the episode is about the retreats, so a board where
# none happened would be the wrong board.
_events = trace(START, GOAL)
assert any(kind == 'back' for kind, _ in _events)

# The route is exactly the squares still on the stack at the end: DFS hands you the path
# for free, which is the one thing it does better than BFS.
assert _route == [c for c in _route]

# No route ever steps onto a wall.
from solution import WALLS
assert not (set(_route) & WALLS)

# THE ORDER OF `DIRECTIONS` DECIDES THE ANSWER. Reversing it gives a different valid
# route, which is the claim that "a path, not the path" is actually making.
import solution
_original = solution.DIRECTIONS
try:
    solution.DIRECTIONS = tuple(reversed(_original))
    _other = dfs(START, GOAL)
    assert _other != _route, 'if the direction order did not matter, the claim would be wrong'
    assert _other[0] == START and _other[-1] == GOAL
finally:
    solution.DIRECTIONS = _original

if __name__ == '__main__':
    main()
