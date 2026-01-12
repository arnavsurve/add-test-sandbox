#!/usr/bin/env python3
"""
Simple script to print the Fibonacci sequence.
"""


def fibonacci(n):
    """Generate and print the first n numbers of the Fibonacci sequence."""
    if n <= 0:
        return
    
    # Initialize the first two numbers
    a, b = 0, 1
    
    print(f"Fibonacci sequence (first {n} numbers):")
    for i in range(n):
        print(f"{i + 1}: {a}")
        a, b = b, a + b


def main():
    """Print the Fibonacci sequence up to 100 numbers."""
    fibonacci(100)


if __name__ == "__main__":
    main()
