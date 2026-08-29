"""
The working version of what the reel shows.

The reel's `dfs()` names one thing it does not write: `unseen`, the first neighbour of a
square that the search has not already entered. It is here, under that name.

`unseen` IS THE ALGORITHM, and the order it returns things in is the answer. Depth-first
search has no opinion about which way to go — it takes whatever the neighbour list hands
back and commits to it until it fails. Reorder the four directions below and you get a
different path, of a different length, on the same board. That is not a flaw to hide: it
is precisely why what DFS returns is "a" path and never "the" path.

The board is identical to `bfs-shortest-path` on purpose. Both episodes run on it, and
the comparison is the point: 19 steps here against BFS's 13.
"""

COLS = 8
ROWS = 4
WALLS = frozenset({2, 10, 18, 13, 21, 29})
START = 8
GOAL = 15

#: Up, down, left, right — and this order decides the route. See the note above.
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def neighbours(i: int) -> list[int]:
    r, c = divmod(i, COLS)
    out = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            n = nr * COLS + nc
            if n not in WALLS:
                out.append(n)
    return out


def dfs(start: int, goal: int) -> list[int]:
    """
    Line for line what is on screen, with `unseen` filled in.

    `seen` lives here rather than in the snippet because the panel had no room for it,
    and without it the search walks in circles forever. Every square entered is marked,
    including ones later backed out of: a dead end is dead however you arrive at it.
    """
    seen = {start}
    stack = [start]

    def unseen(cell: int) -> int | None:
        """The first neighbour of `cell` never entered. None means a dead end."""
        for n in neighbours(cell):
            if n not in seen:
                seen.add(n)
                return n
        return None

    while stack[-1] != goal:
        n = unseen(stack[-1])
        if n is None:
            stack.pop()
            if not stack:
                raise ValueError(f'{goal} is unreachable from {start}')
        else:
            stack.append(n)
    return stack


def trace(start: int, goal: int) -> list[tuple[str, int]]:
    """Every advance and every retreat, in order — what the reel animates."""
    seen = {start}
    stack = [start]
    events: list[tuple[str, int]] = []
    while stack[-1] != goal:
        nxt = next((n for n in neighbours(stack[-1]) if n not in seen), None)
        if nxt is None:
            events.append(('back', stack.pop()))
        else:
            seen.add(nxt)
            stack.append(nxt)
            events.append(('step', nxt))
    return events


def render(route: list[int]) -> str:
    marks = {c: str(i % 10) for i, c in enumerate(route)}
    rows = []
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            i = r * COLS + c
            cells.append('##' if i in WALLS else f'{marks.get(i, " ."):>2}')
        rows.append(' '.join(cells))
    return '\n'.join(rows)
