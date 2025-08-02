import argparse
import random
import time
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

# Weights
LOW_BUCKET_BOUNDRY = 45 # Used to weight the probibility of generating a letter
MID_BUCKET_BOUNDRY = 66 # Used to weight the probibility of generating a number


def random_char_generator(char_type, special_char_list):
    """
    Returns a random char of a random type
    """
    if char_type == UPPER_CASE:
        rand_char = random.choice(ascii_letters).upper()
    if char_type == LOWER_CASE:
        rand_char = random.choice(ascii_letters).lower()
    if char_type == NUMBER:
        rand_char = random.randint(0,9)
    if char_type == SPECIAL_CHAR:
        rand_char = random.choice(special_char_list)

    return rand_char


def random_key(my_dict):
    """
    Returns a random key from a dictionary
    """
    return random.choice(list(my_dict))


def seed_generator():
    """
    Craetes a random seed based on the current time
    """
    # For very short periods of time, the initial seeds for feeding the pseudo-random generator will be hugely different between two successive calls.
    t = int(time.time() * 1000.0)
    seed = ((t & 0xff000000) >> 24) + ((t & 0x00ff0000) >>  8) + ((t & 0x0000ff00) <<  8) + ((t & 0x000000ff) << 24)

    return seed


def generate_password(
    length = 12,
    no_uppercase = False,
    no_lowercase = False,
    no_common_special = False,
    no_uncommon_special = False,
    no_math_chars = False,
    no_numbers = False
    ):
    """ 
    Generates a random password with the given parameters
    """
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

    # passwords generally require one upper case, one lower case, one number, and one special character, so we want to randomly assign each of those to a
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

    # Next we randomly assign each of our required_char_type to a position in the dictionary
    possible_manditory_positions = []
    for i in range(0, length):
        possible_manditory_positions.append(i)

    while len(required_char_type) != 0:
        random_required_char = random.choice(required_char_type)
        required_char_type.remove(random_required_char)

        rand_char = random_char_generator(random_required_char, usable_special_chars)

        key = random.choice(possible_manditory_positions)
        possible_manditory_positions.remove(key)
        
        position_dict[key] = rand_char
        
        random.seed(seed_generator())

    # Now we fill out the rest of the position dictionary
    while len(possible_manditory_positions) != 0:
        key = random.choice(possible_manditory_positions)
        possible_manditory_positions.remove(key)

        random_number = random.randint(0, 100)

        if random_number < LOW_BUCKET_BOUNDRY:
            assigned_char = random.choice(alphabet)
                
        elif LOW_BUCKET_BOUNDRY <= random_number and random_number < MID_BUCKET_BOUNDRY:
            if no_numbers == False:
                assigned_char = random.randint(0,9)
            else:
                if len(usable_special_chars) != 0:
                    if random.choice([0, 1]) == 1:
                        assigned_char = random.choice(usable_special_chars)
                    else:
                        assigned_char = random.choice(alphabet)
                else:
                    assigned_char = random.choice(alphabet)
        else:
            if len(usable_special_chars) != 0:
                assigned_char = random.choice(usable_special_chars)
            else:
                if no_numbers == False:
                    if random.choice([0, 1]) == 1:
                        assigned_char = random.randint(0,9)
                    else:
                        assigned_char = random.choice(alphabet)
                else:
                    assigned_char = random.choice(alphabet)
            
        position_dict[key] = assigned_char

    generated_string = '' 
    for i in range(0, length):
        if str(position_dict[i]) in alphabet:
            if no_lowercase == True:
                position_dict[i] = position_dict[i].upper()
            if no_uppercase == False and no_lowercase == False:
                if random.choice([0, 1]) == 1:
                    position_dict[i] = position_dict[i].upper()
        generated_string = generated_string + str(position_dict[i])

    return generated_string


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

    # Run the parser and places the extracted data in a argparse.Namespace object
    args = parser.parse_args()

    if args.no_uppercase == True and args.no_lowercase == True:
        print("You can't use both the --no_uppercase and --no_lowercase options together - they are mutually exclusive")
        return -1

    # Seed the randomizer
    
    random.seed(seed_generator())

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