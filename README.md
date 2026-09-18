# Depth-First Search

**a path, not the path**

The working code from the [@ByteAnimates](https://www.facebook.com/ByteAnimates) reel.

```bash
python3 main.py
python3 test_solution.py
```

No dependencies. Python 3.9+.

### As shown in the reel

The panel holds twelve lines, so `unseen` was named on screen but not written.
`solution.py` writes them, under those same names.

```python
def dfs(start, goal):
    stack = [start]
    while stack[-1] != goal:
        n = unseen(stack[-1])
        if n is None:
            stack.pop()
        else:
            stack.append(n)
    return stack
```

### Files

| | |
| --- | --- |
| `main.py` | run this — the demo, with real inputs and real output |
| `solution.py` | the working implementation, with the helpers the reel named |
| `test_solution.py` | the properties, checked — they survive a rewrite |

---

The snippet above is generated from the video itself — what you read is byte-for-byte
what was typed on screen. A fix to it belongs in the episode, so open an issue and the
next reel carries it. Everything else here is hand-written and welcome as a pull request.
