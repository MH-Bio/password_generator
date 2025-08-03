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

    # Figure out which types characters are required in our password (upper case, lower case, numbers, special characters)
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

    # Pick the type of character you will genrate at random (e.g. upper case), then you remove the type of character
    # from the list of required characters.  Next randomly generate the character.  Then pick a random position
    # within your password and shove that character in there.  Repeat until all required types are gone.
    while len(required_char_type) != 0:
        secrets_required_char = secrets.choice(required_char_type)
        required_char_type.remove(secrets_required_char)

        if secrets_required_char == UPPER_CASE:
            rand_char = secrets.choice(ascii_letters).upper()
        if secrets_required_char == LOWER_CASE:
            rand_char = secrets.choice(ascii_letters).lower()
        if secrets_required_char == NUMBER:
            rand_char = secrets.randbelow(10)
        if secrets_required_char == SPECIAL_CHAR:
            rand_char = secrets.choice(usable_special_chars)

        key = secrets.choice(possible_manditory_positions)
        possible_manditory_positions.remove(key)
        
        position_dict[key] = rand_char

    # Now we fill out the rest of the position dictionary, but this time we are going to randomly
    # choose the type of character we are going to pick without getting rid of the possibility of
    # picking that type again (e.g. you can decide to use numbers 2+ times).
    # Generate a random number between 0 - 100, depending on which bucket that number falls within
    # will determine what type of character you generate (letter, number, or special character).
    #
    # |-----------LETTER-----------|-----------NUMBER-----------|------SPECIAL CHARACTER------|
    # 0                    LOW_BUCKET_BOUNDRY            MID_BUCKET_BOUNDRY                  100
    #
    # The bucket boundries can be adjusted as an input arguement to make it more or less likely 
    # to generate a particular type of character.
    while len(possible_manditory_positions) != 0:
        key = secrets.choice(possible_manditory_positions) # pick a random position in your dictionary to assign your char to
        possible_manditory_positions.remove(key) # remove the position from your list of possible positions

        # Generate a random number below 101 (i.e. 100 or less)
        secrets_number = secrets.randbelow(101) 

        # Assign a lower case letter if you fall in this bucket
        if secrets_number < LOW_BUCKET_BOUNDRY:
            assigned_char = secrets.choice(alphabet)
                
        # Assign a number if we fall in the middle bucket.  If numbers are not allowed, then 
        # assign either a lower case letter or a special character.  If special characters
        # are not allowed, then just assign a letter.
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
        
        # Assign a special character if we fall in the upper bucket.  If special characters
        # are not allowed then either assign a letter or a number.  If numbers are not allowed
        # then just assign a letter
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
        
        # Put the randomly generated character into your dictionary at the position which was
        # decided at the start of the loop.
        position_dict[key] = assigned_char

    # At this point all characters within your dictionary have been assigned, so next we
    # need to convert the individual dictionary values into a string.  All of our generated
    # letters are lower case (except for the one required upper case letter), so if upper
    # case letters are allowed, you have a 50/50 chance of converting a character to be 
    # upper case.  If lowercase is not allowed, then just convert all letters to upper case
    generated_string = '' 
    for i in range(0, length):
        if str(position_dict[i]) in alphabet:
            if no_lowercase == True:
                position_dict[i] = position_dict[i].upper()
            if no_uppercase == False and no_lowercase == False:
                if secrets.choice([0, 1]) == 1:
                    position_dict[i] = position_dict[i].upper()
        generated_string = generated_string + str(position_dict[i])

    # Give the password one final shuffle for additional randomness
    generated_string_list = list(generated_string)
    secrets.SystemRandom().shuffle(generated_string_list)
    
    return ''.join(generated_string_list)


def main():
    """
    The main function used to assign input arguements and call the generate_password() function.
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
    
    if args.length < 4:
        print("The minimum required number of characters is 4")
        return -1

    return generate_password(
        length = args.length,
        no_uppercase = args.no_uppercase,
        no_lowercase = args.no_lowercase,
        no_common_special = args.no_common_special,
        no_uncommon_special = args.no_uncommon_special,
        no_math_chars = args.no_math_chars,
        no_numbers = args.no_numbers,
        low_bucket_boundry = args.low_bucket_boundry,
        mid_bucket_boundry = args.mid_bucket_boundry
    )

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit