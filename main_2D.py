import sys
import time
import os
import random
import shutil

# Try to import Windows-specific keyboard check
if os.name == 'nt':
    import msvcrt
else:
    import select

# Constants
C_BLUE = "\033[38;5;75m"
C_ORANGE = "\033[38;5;209m"
C_GREEN = "\033[38;5;121m"
C_WHITE = "\033[38;5;255m"
C_RESET = "\033[0m"

DELAY = 0.6  # Slowed down for readability
is_paused = False

def check_input():
    """Checks for keyboard hits: Space to pause, Q/Esc to quit."""
    global is_paused
    char = ""
    
    if os.name == 'nt':
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
    else:
        # Unix non-blocking read
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            char = sys.stdin.read(1).lower()

    if char == ' ':
        is_paused = not is_paused
    elif char in ['q', '\x1b']:  # 'q' or Escape
        teardown_terminal()
        print("\nExited by user.")
        sys.exit(0)

def handle_pause():
    """Stop execution until space is pressed again."""
    while is_paused:
        check_input()
        sys.stdout.write("\033[H\033[K") # Clear top line
        print(f"{C_ORANGE}⏸  PAUSED (Press SPACE to Resume or Q to Quit){C_RESET}")
        time.sleep(0.1)

def render_frame(arr, highlights, stats):
    sys.stdout.write("\033[H") # Home
    max_h = max(arr) if arr else 1
    
    # 1. Header
    print(f"{C_WHITE}Bubble Sort | Comps: {stats['c']} | Swaps: {stats['s']}{C_RESET}")
    print(f"{C_WHITE}[Space]: Pause | [Q]: Quit{C_RESET}")
    print("—" * (len(arr) * 4))

    # 2. Vertical Bars
    output = []
    for y in range(max_h, 0, -1):
        line = []
        for x, val in enumerate(arr):
            color = highlights.get(x, C_BLUE)
            char = "█" if val >= y else " "
            line.append(f" {color}{char}{C_RESET} ")
        output.append("".join(line))
    
    # 3. Floor & Labels
    label_line = [f"{highlights.get(x, C_WHITE)}{val:^3}{C_RESET}" for x, val in enumerate(arr)]
    
    print("\n".join(output))
    print("—" * (len(arr) * 3))
    print("".join(label_line))
    sys.stdout.flush()

def bubble_sort_interactive(arr):
    setup_terminal()
    n = len(arr)
    stats = {'c': 0, 's': 0}
    
    try:
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # Check for Pause/Quit before every step
                check_input()
                handle_pause()

                stats['c'] += 1
                render_frame(arr, {j: C_GREEN, j+1: C_GREEN}, stats)
                time.sleep(DELAY)

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    stats['s'] += 1
                    render_frame(arr, {j: C_ORANGE, j+1: C_ORANGE}, stats)
                    time.sleep(DELAY)
                    swapped = True
            
            if not swapped: break
        
        # PERSISTENCE: Keep window open until 'q'
        render_frame(arr, {}, stats)
        print(f"\n{C_GREEN}✨ Finished! Press 'Q' to exit.{C_RESET}")
        while True:
            check_input()
            time.sleep(0.1)
            
    finally:
        teardown_terminal()

def setup_terminal():
    if os.name == 'nt': os.system('')
    sys.stdout.write("\033[2J\033[H\033[?25l") # Clear and hide cursor
    sys.stdout.flush()

def teardown_terminal():
    sys.stdout.write("\033[?25h\n") # Restore cursor

if __name__ == "__main__":
    data = [random.randint(2, 12) for _ in range(12)]
    bubble_sort_interactive(data)