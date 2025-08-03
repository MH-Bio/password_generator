"""
This work is licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/

Date: August 3, 2025
Author: Michael C. Hernandez
email: michaelhern@hotmail.com

This program generates a randomized password.  By default it is 12 characters, but it can be
made longer or shorter (4 chars is minimum).  User can adjust probibilities of generating a 
letter, number, or special character using input arguements, but the default is a 45% chance 
of a letter of some sort, a 21% chance of a number, and a 34% chance of generating a special
character.
"""
import argparse
import secrets
import sys
from string import ascii_letters

# Special characters we can use
_COMMON_SPECIAL_CHARS=['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
_UNCOMMON_SPECIAL_CHARS = [',', '.', '\'', ';', ':', '/', '<', '>', '[', ']', '{', '}', '~', '|']
_MATH_CHARS = ['=', '+', '-']

# Dictionary Keys
UPPER_CASE = 'Upper Case'
LOWER_CASE = 'Lower Case'
NUMBER = 'Number'
SPECIAL_CHAR = 'Special Char'


def generate_password(
    length = 12,
    no_uppercase = False,
    no_lowercase = False,
    no_common_special = False,
    no_uncommon_special = False,
    no_math_chars = False,
    no_numbers = False,
    low_bucket_boundry = 45,
    mid_bucket_boundry = 66
    ):
    """ 
    Generates a secrets password with the given parameters
    """
    # Bucket weights
    LOW_BUCKET_BOUNDRY = low_bucket_boundry # Used to weight the probibility of generating a letter
    MID_BUCKET_BOUNDRY = mid_bucket_boundry # Used to weight the probibility of generating a number

    # Create a list of alphabet characters
    alphabet = []
    for i in range(97, 123):
        alphabet.append(chr(i))

    # Create a list of special characters
    usable_special_chars = []

    if no_common_special != True:
        for char in _COMMON_SPECIAL_CHARS:
            usable_special_chars.append(char)
    if no_uncommon_special != True:
        for char in _UNCOMMON_SPECIAL_CHARS:
            usable_special_chars.append(char)
    if no_math_chars != True:
        for char in _MATH_CHARS:
            usable_special_chars.append(char)

    # passwords generally require one upper case, one lower case, one number, and one special character, so we want to secretsly assign each of those to a
    # position in our password so it will satifify our requirement
    # First we need to find out what special characters we need

    required_chars = {
        UPPER_CASE: False if no_uppercase else True,
        LOWER_CASE: False if no_lowercase else True,
        NUMBER: False if no_numbers else True,
        SPECIAL_CHAR: False if len(usable_special_chars) == 0 else True
    }

    required_char_type = []
    for key in required_chars.keys():
        if required_chars[key] == True:
            required_char_type.append(key)


    # create a dictionary to store what type of variable you will have each character in
    position_dict = dict()
    for i in range(0, length):
        position_dict[i] = None

    # Next we secretsly assign each of our required_char_type to a position in the dictionary
    possible_manditory_positions = []
    for i in range(0, length):
        possible_manditory_positions.append(i)

    while len(required_char_type) != 0:
        secrets_required_char = secrets.choice(required_char_type)
        required_char_type.remove(secrets_required_char)

        rand_char = secrets_char_generator(secrets_required_char, usable_special_chars)

        key = secrets.choice(possible_manditory_positions)
        possible_manditory_positions.remove(key)
        
        position_dict[key] = rand_char

    # Now we fill out the rest of the position dictionary
    while len(possible_manditory_positions) != 0:
        key = secrets.choice(possible_manditory_positions)
        possible_manditory_positions.remove(key)

        secrets_number = secrets.randbelow(101)

        if secrets_number < LOW_BUCKET_BOUNDRY:
            assigned_char = secrets.choice(alphabet)
                
        elif LOW_BUCKET_BOUNDRY <= secrets_number and secrets_number < MID_BUCKET_BOUNDRY:
            if no_numbers == False:
                assigned_char = secrets.randbelow(10)
            else:
                if len(usable_special_chars) != 0:
                    if secrets.choice([0, 1]) == 1:
                        assigned_char = secrets.choice(usable_special_chars)
                    else:
                        assigned_char = secrets.choice(alphabet)
                else:
                    assigned_char = secrets.choice(alphabet)
        else:
            if len(usable_special_chars) != 0:
                assigned_char = secrets.choice(usable_special_chars)
            else:
                if no_numbers == False:
                    if secrets.choice([0, 1]) == 1:
                        assigned_char = secrets.randbelow(10)
                    else:
                        assigned_char = secrets.choice(alphabet)
                else:
                    assigned_char = secrets.choice(alphabet)
            
        position_dict[key] = assigned_char

    generated_string = '' 
    for i in range(0, length):
        if str(position_dict[i]) in alphabet:
            if no_lowercase == True:
                position_dict[i] = position_dict[i].upper()
            if no_uppercase == False and no_lowercase == False:
                if secrets.choice([0, 1]) == 1:
                    position_dict[i] = position_dict[i].upper()
        generated_string = generated_string + str(position_dict[i])

    # Give the password one final shuffle
    generated_string_list = list(generated_string)
    secrets.SystemRandom().shuffle(generated_string_list)
    
    return ''.join(generated_string_list)


def main():
    """
    The main function
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--length', type=int, default=12, help="The length of your password as an int, default is 12")
    parser.add_argument('--no_uppercase', action='store_true', default=False, help="Forces all generated char type characters to be lowercase")
    parser.add_argument('--no_lowercase', action='store_true', default=False, help="Forces all generated char type characters to be UPPERCASE")
    parser.add_argument('--no_common_special', action='store_true', default=False, help="Excludes common special characters in the generated password")
    parser.add_argument('--no_uncommon_special', action='store_true', default=False, help="Excludes uncommon special characters in the generated password")
    parser.add_argument('--no_math_chars', action='store_true', default=False, help="Excludes uncommon special characters in the generated password")
    parser.add_argument('--no_numbers', action='store_true', default=False, help="Excludes numbers in the generated password")
    parser.add_argument('--low_bucket_boundry', type=int, default=45, help="Sets the low bucket boundry for generating alphabet characters for your password")
    parser.add_argument('--mid_bucket_boundry', type=int, default=66, help="Sets the middle bucket boundry for generating numbers characters for your password")

    # Run the parser and places the extracted data in a argparse.Namespace object
    args = parser.parse_args()

    if args.no_uppercase == True and args.no_lowercase == True:
        print("You can't use both the --no_uppercase and --no_lowercase options together - they are mutually exclusive")
        return -1

    return generate_password(
        length = args.length,
        no_uppercase = args.no_uppercase,
        no_lowercase = args.no_lowercase,
        no_common_special = args.no_common_special,
        no_uncommon_special = args.no_uncommon_special,
        no_math_chars = args.no_math_chars,
        no_numbers = args.no_numbers
    )


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit