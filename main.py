import sys
import time
import shutil
import os


try:
    import ctypes
except ImportError:
    ctypes = None


DELAY_COMPARE = 0.15
DELAY_SWAP = 0.25
MAX_BAR_WIDTH = 30
MIN_BAR_WIDTH = 10

ANSI_CLEAR_AND_HOME = "\033[2J\033[H"
ANSI_HOME = "\033[H"
ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"


def bubble_sort(arr: list, in_place: bool = True) -> list:
    """Classic bubble sort used by tests and non-visual flows."""
    working_arr = arr if in_place else arr[:]

    n = len(working_arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if working_arr[j] > working_arr[j + 1]:
                working_arr[j], working_arr[j + 1] = working_arr[j + 1], working_arr[j]
                swapped = True
        if not swapped:
            break
    return working_arr


def bubble_sort_in_place_redraw(arr: list[int]) -> list[int]:
    """Bubble sort with in-place terminal redraw hooks."""
    setup_terminal_animation()
    try:
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                draw_compare_frame(arr, i, j)
                time.sleep(DELAY_COMPARE)

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    draw_swap_frame(arr, i, j)
                    time.sleep(DELAY_SWAP)

            if not swapped:
                draw_already_sorted_frame(arr, i)
                time.sleep(DELAY_COMPARE)
                break

        draw_done_frame(arr)
        return arr
    finally:
        teardown_terminal_animation()


def setup_terminal_animation() -> None:
    """Initialize terminal state for in-place redraw."""
    enable_windows_ansi_if_possible()

    sys.stdout.write(ANSI_CLEAR_AND_HOME)
    sys.stdout.write(ANSI_HIDE_CURSOR)
    sys.stdout.flush()


def enable_windows_ansi_if_possible() -> None:
    """Best-effort ANSI enabling for older Windows terminals."""
    if os.name != "nt" or ctypes is None:
        return

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    if handle == 0 or handle == -1:
        return

    mode = ctypes.c_ulong()
    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)) == 0:
        return

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(handle, new_mode)


def teardown_terminal_animation() -> None:
    """Restore terminal state after animation."""
    sys.stdout.write(f"{ANSI_SHOW_CURSOR}\n")
    sys.stdout.flush()


def draw_compare_frame(arr: list[int], pass_idx: int, left_idx: int) -> None:
    """Draw a frame while comparing arr[left_idx] and arr[left_idx + 1]."""
    redraw_header(pass_idx, len(arr), f"compare {left_idx} and {left_idx + 1}")
    render_bars(arr, highlighted={left_idx, left_idx + 1}, status="Checking order...")


def draw_swap_frame(arr: list[int], pass_idx: int, left_idx: int) -> None:
    """Draw a frame immediately after a swap."""
    redraw_header(pass_idx, len(arr), f"swap {left_idx} <-> {left_idx + 1}")
    render_bars(arr, highlighted={left_idx, left_idx + 1}, status="Swapped.")


def draw_done_frame(arr: list[int]) -> None:
    """Draw final sorted state."""
    total_passes = max(1, len(arr))
    redraw_header(total_passes - 1, total_passes, "done")
    render_bars(arr, highlighted=set(), status="Sorting complete.")


def draw_already_sorted_frame(arr: list[int], pass_idx: int) -> None:
    """Draw frame when no swaps occur in a pass."""
    redraw_header(pass_idx, len(arr), "already sorted")
    render_bars(arr, highlighted=set(), status="No swaps in this pass. Stopping early.")


def redraw_header(pass_idx: int, total_passes: int, action: str) -> None:
    """Move cursor to top-left and print frame header."""
    sys.stdout.write(ANSI_HOME)
    print(f"PASS {pass_idx + 1}/{total_passes} | ACTION: {action}")
    print("-" * 50)


def render_bars(arr: list[int], highlighted: set[int], status: str) -> None:
    """Render ASCII bars for the current array state."""
    max_val = max(arr) if arr else 1
    bar_width = terminal_bar_width()
    for idx, value in enumerate(arr):
        width = scaled_width(value, max_val, bar_width)
        bar = "#" * width
        marker = "<" if idx in highlighted else " "
        print(f"{idx:02d} | {bar:<{bar_width}} ({value:02d}) {marker}")
    print(f"\nStatus: {status}")
    sys.stdout.flush()


def terminal_bar_width() -> int:
    """Compute bar width from terminal size with safe limits."""
    columns = shutil.get_terminal_size(fallback=(80, 24)).columns
    candidate = columns - 18
    return max(MIN_BAR_WIDTH, min(MAX_BAR_WIDTH, candidate))


def scaled_width(value: int, max_value: int, bar_width: int) -> int:
    """Convert values into bounded bar widths."""
    if max_value <= 0:
        return 0
    if value <= 0:
        return 0
    return max(1, int((value / max_value) * bar_width))


if __name__ == "__main__":
    demo_data = [12, 5, 18, 2, 9, 14]
    bubble_sort_in_place_redraw(demo_data)