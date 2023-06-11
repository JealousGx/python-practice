import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the typing test!")
    stdscr.addstr("\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target_text, curr_text, wpm=0):
    stdscr.addstr(target_text)
    stdscr.addstr(1, 0, f"WPM: {wpm}", curses.color_pair(3))

    for i, char in enumerate(curr_text):
        if char == target_text[i]:
            stdscr.addstr(0, i, char, curses.color_pair(1))
        else:
            stdscr.addstr(0, i, char, curses.color_pair(2))


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def typing_test(stdscr):
    target_text = load_text()
    curr_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = int(round(len("".join(curr_text)) / 5 / (time_elapsed / 60)))

        stdscr.clear()
        display_text(stdscr, target_text, curr_text, wpm)
        stdscr.refresh()

        if curr_text == list(target_text):
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()
                continue
        elif len(curr_text) >= len(target_text):
            continue

        curr_text.append(key)


def main(stdscr):  # stdscr is the screen object that represents the terminal window & is standard name for it in curses library
    # Define the colors we'll use
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        typing_test(stdscr)

        stdscr.addstr(
            2, 0, "You finished the test! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
