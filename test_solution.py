"""
Run it: python3 test_solution.py   (or: pytest)
"""

import solution
from main import bfs_length
from solution import GOAL, START, WALLS, dfs, neighbours, trace


def test_it_returns_a_legal_route_with_no_repeats():
    route = dfs(START, GOAL)
    assert route[0] == START and route[-1] == GOAL
    assert all(b in neighbours(a) for a, b in zip(route, route[1:]))
    assert len(set(route)) == len(route), 'the stack should never hold a square twice'


def test_it_finds_a_path_and_not_the_shortest_one():
    # The whole point of running it on the same board as bfs-shortest-path.
    route = dfs(START, GOAL)
    assert len(route) - 1 == 19
    assert bfs_length(START, GOAL) == 13
    assert len(route) - 1 > bfs_length(START, GOAL)


def test_it_really_backtracks_here():
    # A board where nothing was ever taken back would be the wrong board for this episode.
    assert any(kind == 'back' for kind, _ in trace(START, GOAL))


def test_the_neighbour_order_decides_the_answer():
    # This is what "a path, not the path" actually means, and it is testable: reverse the
    # four directions and the same code returns a different, equally valid route.
    route = dfs(START, GOAL)
    original = solution.DIRECTIONS
    try:
        solution.DIRECTIONS = tuple(reversed(original))
        other = dfs(START, GOAL)
        assert other != route
        assert other[0] == START and other[-1] == GOAL
    finally:
        solution.DIRECTIONS = original


def test_no_route_ever_steps_on_a_wall():
    assert not (set(dfs(START, GOAL)) & WALLS)


if __name__ == '__main__':
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'  ok  {name}')
            passed += 1
    print(f'\n{passed} tests passed\n')
