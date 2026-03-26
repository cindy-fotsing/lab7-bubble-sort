# lab-7-bubble-sort

Python Bubble Sort project with two modes:

- a classic function for normal sorting usage
- an in-place terminal redraw mode to visualize sorting as an animation

## Features

- `bubble_sort(arr, in_place=True)` for regular sorting
- `bubble_sort_in_place_redraw(arr)` for terminal animation
- early-stop optimization when the list is already sorted
- terminal-width-aware ASCII bars
- basic `pytest` test suite

## Project Structure

- `main.py`: sorting logic + terminal visualization
- `tests/test_main.py`: unit tests for core bubble sort behavior
- `requirements.txt`: dependency list (`pytest`)
- `README.md`: project documentation
- `REPORT.md`: report template
- `JOURNAL.md`: chronological interaction log

## Requirements

- Python 3.10+
- `pip`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Run the terminal visualization demo:

```powershell
python main.py
```

Use classic bubble sort in code:

```python
from main import bubble_sort

data = [4, 1, 3, 10, 5, 16, 2]
result = bubble_sort(data, in_place=False)
print(result)
```

## Run Tests

```powershell
python -m pytest -q
```

Current tests validate:

- correct numeric sorting
- duplicate handling
- in-place mutation behavior
- non in-place behavior
- TypeError on non-comparable values

## Notes

- Bubble Sort time complexity is $O(n^2)$ in average and worst cases.
- The terminal animation uses ANSI escape sequences and includes a best-effort Windows ANSI enable step.
