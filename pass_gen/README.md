# Password Generator

This is a small utility that generates a random 12‑character password containing
uppercase letters, lowercase letters, digits, and symbols.

## Usage

```bash
# From the command line, you can run the script directly:
python -m pass_gen.generator
```

Or import it into your own Python code:

```python
from pass_gen.generator import generate_password

# Generate a password of default length (12)
print(generate_password())

# Or generate a longer password
print(generate_password(16))
```

The function will raise a `ValueError` if the requested length is less than 4,
since at least one character from each category is required.

## Requirements

Python 3.8+ is required. No external dependencies.

## License

MIT
