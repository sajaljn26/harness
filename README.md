# Dice Roller

A simple command-line tool to roll dice using standard dice notation (e.g., `2d6+3`).

## Installation

This project uses Python 3.8+. No external dependencies are required.

```bash
# Clone the repo
git clone <repo-url>
cd dice_roller

# Optional: create a virtual environment
python -m venv .venv
.
.venv\Scripts\activate
```

## Usage

Run the script and follow the prompts:

```bash
python main.py
```

You can also specify a roll directly via command line:

```bash
python main.py roll 2d6+3
```

The script supports:
- Standard dice notation `NdM` (N dice of M sides)
- Optional modifiers `+X` or `-Y`
- Multiple dice rolls in one expression (e.g., `d8+1 d6-2`).

## Example

```text
Enter dice notation (e.g., 2d6+3): 4d8-2
Result: 4d8-2 => 23 (Rolls: 6, 5, 7, 5)
```

## License

MIT License.

---

Happy rolling! 🎲