# Secure Password Generator

This is a command-line password generator written in Python that creates secure, customizable passwords.  It offers strong cryptographic randomness, configurable character sets, and adjustable probabilities for character types.

---

## License

This work is licensed under the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

**Author:** Michael C. Hernandez  
**Date:** August 3, 2025  
**Email:** michaelhern@hotmail.com

---

## Features

- **Cryptographically secure**: Uses Python’s [`secrets`](https://docs.python.org/3/library/secrets.html) module, not [`random`](https://docs.python.org/3/library/random.html)
- **Customizable length**: Default is 12 characters; minimum is 4
- **Character type toggles**:
  - Uppercase or lowercase letters
  - Numbers
  - Common, uncommon, and math-related special characters
- **Probability tuning**: Adjust character generation weights using bucket boundary arguments
- **Always includes at least one of each enabled character type**

---

## Usage

Run the script using Python 3:

```bash
python secure_password_generator.py [OPTIONS]
```

---

## Options

| Option                  | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `-l`, `--length`        | Length of the password (default: 12, min: 4)              |
| `--no_uppercase`        | Exclude uppercase letters                                 |
| `--no_lowercase`        | Exclude lowercase letters                                 |
| `--no_common_special`   | Exclude common special characters (`!@#$%^&*()`)          |
| `--no_uncommon_special` | Exclude uncommon special characters (`,.';:/<>[]{}\~|\`)  |
| `--no_math_chars`       | Exclude math-related special characters (`=+-`)           |
| `--no_numbers`          | Exclude digits                                            |
| `--low_bucket_boundry`  | Weight (0–100) for letter generation (default: 45)        |
| `--mid_bucket_boundry`  | Weight (0–100) for number generation (default: 66)        |

---

## Example: Generate a 16-character password with no numbers

python secure_password_generator.py -l 16 --no_numbers

---

## Example: Change probability weights

python secure_password_generator.py --low_bucket_boundry 60 --mid_bucket_boundry 80

---

## How It Works

1. Character buckets:

  * Letters: 0–low_bucket_boundry
  * Numbers: low_bucket_boundry–mid_bucket_boundry
  * Special characters: mid_bucket_boundry–100

2. Ensures compliance with common password policies:

  * At least one character of each selected type is inserted at a random position.
  * Remaining characters are randomly chosen based on weighted probabilities.

3. Final shuffle:

  * The password is shuffled after generation to avoid positional predictability.

---

## Requirements

  * Python 3.6 or later

---