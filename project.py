import curses
import time
import random
from curses import wrapper
def start_screen(stdscr):
     stdscr.clear()
     stdscr.addstr("Welcome to the speed typing test!")
     stdscr.addstr("\nRules are as follows:")
     stdscr.addstr("\n1. Correct text shows up in green colour, incorrect in red."
     "\n2. WPM count goes down with every backspace key pressed or seconds elapsed without "
     "any input to the screen. \n3. You may press Esc anytime to exit the game.")
     stdscr.addstr("\nPress any key to begin!")
     stdscr.refresh()
     stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
      stdscr.addstr(target)
      stdscr.addstr(1, 0, f"WPM: {wpm}")

      for i, char in enumerate(current):
               correct_char = target[i]
               color = curses.color_pair(1)
               if char != correct_char:
                    color = curses.color_pair(2)
              
               stdscr.addstr(0, i, char, color)

def load_text():
     with open("test.txt", "r") as f:
          lines = f.readlines()
          return random.choice(lines).strip()

def wpm_test(stdscr):
     target_text = load_text()
     current_text = []
     wpm=0
     start_time = time.time()
     stdscr.nodelay(True)

     while True:
           time_elapsed = max(time.time() - start_time, 1)
           wpm = round((len(current_text)/(time_elapsed/60))/5)
           stdscr.clear()
           display_text(stdscr, target_text, current_text, wpm)
           stdscr.refresh()

           if "".join(current_text) == target_text:
                stdscr.nodelay(False)
                break
                      
           try:
            key = stdscr.getkey()
           except:
                continue

           if ord(key) == 27:
               break
           if key in ("KEY_BACKSPACE", '\b', "\x7f"):
                if len(current_text) > 0:
                     current_text.pop()
           elif len(current_text) < len(target_text):       
            current_text.append(key)

     difference = wpm - 40
     if difference > 0:
          message = f"You completed the text! Great job! Your WPM is {difference} points higher than the average WPM of 40."
     elif difference < 0:
          message = f"You completed the text! Keep practicing! Your WPM is {abs(difference)} points lower than the average WPM of 40."
     else:
          message = "You completed the text! Impressive! Your WPM is exactly the average WPM of 40."

     if wpm < 20:
          category = "Slow typist"
     elif 20 <= wpm < 40:
          category = "Below-average typist"
     elif 40 <= wpm < 60:
          category = "Average typist"
     elif 60 <= wpm < 80:
          category = "Fast typist"
     else:
          category = "Pro-level typist"

     stdscr.addstr(2, 0, message)
     stdscr.addstr(4, 0, f"Category: {category}")

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(6, 0, "Press any key to play again or Esc to end the game...")
        key = stdscr.getkey()
        if ord(key) == 27:
             break

wrapper(main)