"""
A simple dice rolling utility.
"""

import random
from typing import List


def roll_dice(num_dice: int = 1, sides: int = 6) -> List[int]:
    """Roll ``num_dice`` dice each with ``sides`` sides.

    Parameters
    ----------
    num_dice: int
        Number of dice to roll.
    sides: int
        Number of sides on each die.

    Returns
    -------
    List[int]
        A list containing the result of each die roll.
    """
    return [random.randint(1, sides) for _ in range(num_dice)]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dice roller")
    parser.add_argument("num_dice", type=int, help="Number of dice to roll")
    parser.add_argument("--sides", type=int, default=6, help="Number of sides per die")
    args = parser.parse_args()

    rolls = roll_dice(args.num_dice, args.sides)
    print(f"Rolled {args.num_dice}d{args.sides}: {rolls}")
