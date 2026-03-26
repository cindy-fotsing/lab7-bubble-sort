import sys
import time
from typing import Iterable


DELAY_COMPARE = 0.15
DELAY_SWAP = 0.25
MAX_BAR_WIDTH = 30


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
                # TODO: Add an explicit "already sorted" frame for better UX.
                break

        draw_done_frame(arr)
        return arr
    finally:
        teardown_terminal_animation()


def setup_terminal_animation() -> None:
    """Initialize terminal state for in-place redraw."""
    # TODO: On Windows legacy terminals, add ANSI enabling fallback if needed.
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def teardown_terminal_animation() -> None:
    """Restore terminal state after animation."""
    sys.stdout.write("\033[?25h\n")
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
    redraw_header(len(arr), len(arr), "done")
    render_bars(arr, highlighted=set(), status="Sorting complete.")


def redraw_header(pass_idx: int, total_passes: int, action: str) -> None:
    """Move cursor to top-left and print frame header."""
    sys.stdout.write("\033[H")
    print(f"PASS {pass_idx + 1}/{total_passes} | ACTION: {action}")
    print("-" * 50)


def render_bars(arr: list[int], highlighted: set[int], status: str) -> None:
    """Render ASCII bars for the current array state."""
    # TODO: Consider dynamic scaling for very large values.
    max_val = max(arr) if arr else 1
    for idx, value in enumerate(arr):
        width = scaled_width(value, max_val)
        bar = "#" * width
        marker = "<" if idx in highlighted else " "
        print(f"{idx:02d} | {bar:<{MAX_BAR_WIDTH}} ({value:02d}) {marker}")
    print(f"\nStatus: {status}")
    sys.stdout.flush()


def scaled_width(value: int, max_value: int) -> int:
    """Convert values into bounded bar widths."""
    if max_value <= 0:
        return 0
    # TODO: Tune the minimum visible width policy for tiny values.
    return max(1, int((value / max_value) * MAX_BAR_WIDTH))


if __name__ == "__main__":
    demo_data = [12, 5, 18, 2, 9, 14]
    bubble_sort_in_place_redraw(demo_data)