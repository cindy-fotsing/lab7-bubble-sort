from typing import List, Any

def bubble_sort(arr: List[Any], in_place: bool = True) -> List[Any]:
    """
    Sorts a list using the bubble sort algorithm.
    
    Args:
        arr: The list of comparable elements to sort.
        in_place: If True, mutates the original list. If False, returns a sorted copy.
    """
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

if __name__ == "__main__":
    test_data = [4, 1, 3, 10, 5, 16, 2]
    print(f"Original: {test_data}")
    print(f"Sorted:   {bubble_sort(test_data)}")