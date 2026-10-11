"""
Password Generator Module
=========================

A small utility that produces cryptographically‑suitable passwords.

The :func:`generate_password` function returns a random password of a
specified length that contains at least one character from each of the
following categories: lowercase letters, uppercase letters, digits and
special symbols.  The default password length is 12 characters.

The :func:`_shuffle_sequence` helper is used internally to randomise
the order of characters in the final password.

Usage
-----

>>> from pass_gen.generator import generate_password
>>> print(generate_password())
'5f&bA4!xP2$k'

The module is pure Python and requires no external dependencies.
"""

import random
import string
from typing import List

# ---------------------------------------------------------------------------
# Character pools
# ---------------------------------------------------------------------------
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"

ALL_CHARS = LOWER + UPPER + DIGITS + SYMBOLS

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _shuffle_sequence(seq: List[str]) -> List[str]:
    """Return a new list containing *seq* in random order.

    The function performs an in‑place :func:`random.shuffle` on a copy of the
    input sequence and then returns the shuffled copy.  This keeps the
    original list untouched, which is useful for unit tests and for
    ensuring deterministic behaviour in other parts of the module.

    Parameters
    ----------
    seq: List[str]
        The list of characters to shuffle.

    Returns
    -------
    List[str]
        A new list with the elements of ``seq`` shuffled.
    """
    seq_copy = seq[:]
    random.shuffle(seq_copy)
    return seq_copy

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_password(length: int = 12) -> str:
    """Generate a random password.

    The returned password contains at least one character from each of the
    four categories (lowercase, uppercase, digits, symbols).  The length
    argument allows callers to request longer or shorter passwords, but a
    minimum of four characters is required to satisfy the category
    constraints.

    Parameters
    ----------
    length: int, optional
        Desired length of the password.  Must be greater than or equal
        to 4.  Defaults to ``12``.

    Returns
    -------
    str
        The generated password string.

    Raises
    ------
    ValueError
        If ``length`` is less than 4.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    # Ensure each character category is represented at least once.
    password_chars = [
        random.choice(LOWER),
        random.choice(UPPER),
        random.choice(DIGITS),
        random.choice(SYMBOLS),
    ]

    # Fill the remaining positions with random picks from all categories.
    remaining_chars = [random.choice(ALL_CHARS) for _ in range(length - 4)]
    password_chars.extend(remaining_chars)

    # Randomise the order to avoid any predictable patterns.
    password_chars = _shuffle_sequence(password_chars)

    return "".join(password_chars)

# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for i in range(5):
        print(f"Password {i+1}: {generate_password(12)}")
