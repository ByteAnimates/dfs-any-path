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



if __name__ == '__main__':
    main()
