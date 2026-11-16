#!/usr/bin/env python3
"""Community Connect Four for the GitHub profile README.

Run by .github/workflows/connect4.yml when someone opens an issue titled
"connect4|drop|<column>". Reads the move from the TITLE and PLAYER environment
variables, updates connect4/state.json, rewrites the game section of README.md,
and prints a reply for the issue comment.

Run with no TITLE set to just re-render the README from the saved state.
"""
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "connect4" / "state.json"
README = ROOT / "README.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "SmaranKudapa/SmaranKudapa")

ROWS, COLS = 6, 7
START, END = "<!-- C4:START -->", "<!-- C4:END -->"
# Stop one person from playing both sides back to back.
BLOCK_CONSECUTIVE = True

NAME = {"R": "🔴 Red", "Y": "🟡 Yellow"}
PIECE = {"": "⚪", "R": "🔴", "Y": "🟡"}
WIN_PIECE = {"R": "🟥", "Y": "🟨"}
MOVE_RE = re.compile(r"^connect4\|drop\|([1-7])$", re.IGNORECASE)


def empty_board():
    return [["" for _ in range(COLS)] for _ in range(ROWS)]


def new_state():
    return {
        "board": empty_board(),
        "turn": "R",
        "moves": [],
        "game": 1,
        "last_game": None,
        "stats": {"R": 0, "Y": 0, "draw": 0, "total_moves": 0},
        "players": {},
    }


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return new_state()


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def drop(board, col):
    """Drop a piece into col (0-based). Returns the row it lands in, or None if full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == "":
            return row
    return None


def find_win(board, row, col):
    """Return the winning cells through (row, col), or None."""
    color = board[row][col]
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        cells = [(row, col)]
        for sign in (1, -1):
            r, c = row + dr * sign, col + dc * sign
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == color:
                cells.append((r, c))
                r, c = r + dr * sign, c + dc * sign
        if len(cells) >= 4:
            return cells
    return None


def play(state, title, player):
    """Apply a move. Returns the reply text for the issue."""
    match = MOVE_RE.match(title.strip())
    if not match:
        return (
            f"Sorry @{player}, I didn't understand `{title}`. "
            f"Go back to the [profile](https://github.com/{REPO.split('/')[0]}) "
            "and click a column number to play."
        )

    col = int(match.group(1)) - 1
    moves = state["moves"]
    if BLOCK_CONSECUTIVE and moves and moves[-1]["player"] == player:
        return (
            f"@{player}, you made the last move, so someone else has to go next. "
            "Ask a friend to play, then come back!"
        )

    board = state["board"]
    row = drop(board, col)
    if row is None:
        return f"@{player}, column {col + 1} is full. Pick another column!"

    color = state["turn"]
    board[row][col] = color
    moves.append({
        "player": player,
        "color": color,
        "col": col + 1,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    })
    state["stats"]["total_moves"] += 1
    state["players"][player] = state["players"].get(player, 0) + 1

    profile = f"https://github.com/{REPO.split('/')[0]}"
    win = find_win(board, row, col)
    draw = not win and all(cell for cell in board[0])
    if win or draw:
        final = [list(r) for r in board]
        if win:
            for r, c in win:
                final[r][c] = "W" + color
        state["stats"][color if win else "draw"] += 1
        state["last_game"] = {
            "number": state["game"],
            "winner": color if win else None,
            "winning_player": player if win else None,
            "moves": len(moves),
            "players": sorted({m["player"] for m in moves}),
            "board": final,
        }
        state["board"] = empty_board()
        state["moves"] = []
        state["turn"] = "R"
        state["game"] += 1
        if win:
            return (
                f"🎉 @{player} dropped {NAME[color]} into column {col + 1} "
                f"and **won game #{state['game'] - 1}**! A new game has started. "
                f"[See the board]({profile})"
            )
        return f"Column {col + 1} filled the board. It's a draw! A new game has started. [See the board]({profile})"

    state["turn"] = "Y" if color == "R" else "R"
    return (
        f"Nice move, @{player}! You dropped {NAME[color]} into column {col + 1}. "
        f"It's now {NAME[state['turn']]}'s turn. [See the board]({profile})"
    )


def move_link(col):
    title = urllib.parse.quote(f"connect4|drop|{col}")
    body = urllib.parse.quote(
        "Just click **Create** (or **Submit new issue**). You don't need to change anything.\n\n"
        "A GitHub Action will play your move and update the board in about a minute."
    )
    return f"https://github.com/{REPO}/issues/new?title={title}&body={body}"


def board_table(board, headers):
    lines = ["| " + " | ".join(headers) + " |", "|" + ":-:|" * COLS]
    for row in board:
        cells = [WIN_PIECE[c[1]] if c.startswith("W") else PIECE[c] for c in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def user_link(name):
    return f"[@{name}](https://github.com/{name})"


def render(state):
    board = state["board"]
    headers = [
        f"[**{c + 1}**]({move_link(c + 1)})" if board[0][c] == "" else "✖️"
        for c in range(COLS)
    ]
    out = [
        "## 🎮 Community Connect Four",
        "",
        f"**Game #{state['game']}**: it's **{NAME[state['turn']]}'s** turn. "
        "Anyone can play! Click a column number to drop a piece there.",
        "",
        board_table(board, headers),
        "",
        "<sub>Clicking a number opens a new issue with your move filled in. Submit it, "
        "and a GitHub Action plays the move and updates this board in about a minute. "
        "You can't move twice in a row, so bring a friend.</sub>",
        "",
    ]

    if state["moves"]:
        out += ["**Recent moves**", "", "| Player | Move | When |", "|---|---|---|"]
        for m in reversed(state["moves"][-5:]):
            out.append(f"| {user_link(m['player'])} | {PIECE[m['color']]} column {m['col']} | {m['at']} |")
        out.append("")
    else:
        out += ["*No moves yet this game. Make the first one!*", ""]

    last = state["last_game"]
    if last:
        if last["winner"]:
            w = last['winning_player']
            result = f"{NAME[last['winner']]} won in {last['moves']} moves (winning move by <a href='https://github.com/{w}'>@{w}</a>)"
        else:
            result = f"Draw after {last['moves']} moves"
        out += [
            "<details>",
            f"<summary><b>Last game (#{last['number']}):</b> {result}</summary>",
            "",
            board_table(last["board"], [str(c + 1) for c in range(COLS)]),
            "",
            "Players: " + ", ".join(user_link(p) for p in last["players"]),
            "",
            "</details>",
            "",
        ]

    s = state["stats"]
    out.append(
        f"**All-time wins:** 🔴 Red {s['R']} · 🟡 Yellow {s['Y']} · 🤝 Draws {s['draw']} · "
        f"{s['total_moves']} moves by {len(state['players'])} players"
    )
    top = sorted(state["players"].items(), key=lambda kv: (-kv[1], kv[0]))[:5]
    if top:
        out += ["", "**Top players:** " + " · ".join(f"{user_link(p)} ({n})" for p, n in top)]
    return "\n".join(out)


def update_readme(state):
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"README.md is missing the {START} / {END} markers")
    section = f"{START}\n{render(state)}\n{END}"
    README.write_text(pattern.sub(lambda _: section, text), encoding="utf-8")


def main():
    state = load_state()
    title = os.environ.get("TITLE")
    if title:
        print(play(state, title, os.environ.get("PLAYER", "someone")))
    save_state(state)
    update_readme(state)


if __name__ == "__main__":
    main()
