"""
    Joseph Manifold
    Created on 08/10/2022

    This program is designed to translate numbers to alphabetical form and 
    vice versa, particularly for monetary transactions. It's capability is 
    limited to handling numbers up to and including 100 billion.

    To use the program, access it from the terminal and run it, appending
    the number or word you would like to translate.
    e.g. > python3 money_to_words.py "three hundred"

    Last modified on 09/10/2022

"""

import sys
import math

"""Dictionaries used for translation"""
NUMS_SINGLE_DIGIT_DICT = {"0":"zero ", "1":"one ", "2":"two ", "3":"three ", "4":"four ", 
                          "5":"five ", "6":"six ", "7":"seven ", "8":"eight ", "9":"nine "}
NUMS_TEENS_DICT = {"10":"ten ", "11":"eleven ", "12":"twelve ", "13":"thirteen ", "14":"fourteen ",
                   "15":"fifteen ", "16":"sixteen ", "17":"seventeen ", "18":"eighteen ", "19":"nineteen "}
# the value ten in the following dict might not get used. Same in the words dict
NUMS_DOUBLE_DIGIT_DICT = {"0":"", "1":"ten ", "2":"twenty ", "3":"thirty ", "4":"forty ", "5":"fifty ", 
                          "6":"sixty ", "7":"seventy ", "8":"eighty ", "9":"ninety "}
NUMS_LARGE_NUMS_DICT = {2:" thousand, ", 3:" million, ", 4:" billion, "}

WORDS_SINGLE_DIGIT_DICT = {"zero":0, "one":1, "two":2, "three":3, "four":4, 
                          "five":5, "six":6, "seven":7, "eight":8, "nine":9}
WORDS_TEENS_DICT = {"ten":10, "eleven":11, "twelve":12, "thirteen":13, "fourteen":14,
                   "fifteen":15, "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19}
WORDS_DOUBLE_DIGIT_DICT = {"ten":10, "twenty":20, "thirty":30, "forty":40, "fifty":50, 
                          "sixty":60, "seventy":70, "eighty":80, "ninety":90}
WORDS_LARGE_NUMS_DICT = {"thousand":10**3, "million":10**6, "billion":10**9}
WORDS_KEYWORDS_LIST = ["and", "dollar", "dollars", "cent", "cents"]


def main(input):
    """
    The main function for the program, which calls helper functions in order
    to translate the given input. Also checks for error messages from such 
    functions and prints those if present.
    """

    input = extract_input(input)

    # if message is not None:
    #     sys.exit(message)

    is_numerical, input = is_in_numerical_form(input)

    if is_number_too_big(input):
        sys.exit("ERROR: The number you have given is larger than 100 billion! Please pick a " + \
                 "number greater than or equal to zero and less than or equal to 100 billion.")
    
    if is_number_too_small(input):
        sys.exit("ERROR: The input received appears to be a negative number! Please enter a " + \
                 "number greater than or equal to zero and less than or equal to 100 billion.")
    
    if is_numerical is True:
        output = number_to_words(input)
    else:
        output = words_to_number(input)

    sys.exit(output)


def extract_input(input):
    """
    Takes the list from the sys.argv command and extracts the user's given
    input out of the list. Also modifies the input to be better suited for
    future use.
    """
    if len(input) > 1:
        sys.exit("ERROR: You have entered too many values. Please " \
                 "only enter one integer, float or string for translation.")
    
    input = input[0].replace(",","") 
    input = input.replace("  ", " ")
    input = input.strip("$")

    return input


def is_in_numerical_form(input):
    """
    Determines whether the given input is of numerical form or alphabetical form. If 
    the input is a number, the function returns true. Alternatively, if it is a string, it is 
    assumed to be in alphabetical form and the function returns False.
    """

    # if type(input[0]) == int or type(input[0]) == float:
    #     return True, input[0], None
    # elif type(input[0]) == str:
    #     return False, input[0], None
    # else:
    #     return None, input[0], "ERROR: Please enter a valid number (in numerical or" + \
    #                   " alphabetical form) as your input.\n"

    try:
        input = float(input)
        return True, input
    except ValueError:
        pass

    return False, input.lower().split(" ")


def is_number_too_big(number):
    """
    This function checks to determine whether the given number is above 100 
    billion.
    """

    if type(number) == float:        
        if number > 100000000000:
            return True

    else:
        if "billion" in number:
            # checks if the word "hundred" appears before the word "billion"
            if "hundred" in number[:number.index("billion")]:
                if "one" != number[0] and "a" != number[0]:
                    return True
                else:
                    if len(number) > 3:
                        return True

    return False


def is_number_too_small(number):
    """Checks if the number is negative. If so, returns True."""

    if type(number) == float:
        if number < 0:
            return True
    
    else:
        if "negative" in number:
            return True
    
    return False


def number_to_words(number):
    """This function converts a number given in numerical form into alphabetical form"""

    number = list(str(number))

    number_size = len(number[:number.index(".")])
    largeness_degree = math.ceil(number_size / 3)

    alphabetical_number = "\n"
    start_of_window = 0
    end_of_window = 3

    while len(number[:number.index(".")]) % 3 != 0:
        # this loop adjusts the length of the number by adding zeros in, making it easier to translate
        number.insert(0, "0")

    while largeness_degree > 1:

        next_chunk, was_just_zeros = triple_digit_num_to_words(number[start_of_window:end_of_window])
        if not was_just_zeros:
            alphabetical_number += next_chunk
            alphabetical_number += NUMS_LARGE_NUMS_DICT[largeness_degree]

        start_of_window += 3
        end_of_window += 3
        largeness_degree -= 1
    
    next_chunk, was_just_zeros = triple_digit_num_to_words(number[start_of_window:end_of_window], True)
    if "hundred" not in next_chunk:
        alphabetical_number = alphabetical_number.strip(", ")

    alphabetical_number += " " + next_chunk 
    alphabetical_number = alphabetical_number.strip(", ")

    if len(alphabetical_number) < 3:
        alphabetical_number = "\nzero"

    plural = "s "
    if alphabetical_number == "\n and one":
        plural = " "

    alphabetical_number += " dollar" + plural + cents_number_to_words(number[(number.index(".")+1):])
    alphabetical_number = alphabetical_number.replace("\n and ", "\n")
    alphabetical_number = alphabetical_number.replace("\n ", "\n")
    alphabetical_number = alphabetical_number.replace("  ", " ")



    return alphabetical_number + "\n"


def triple_digit_num_to_words(number, last_3_digits=False):
    """
    Takes a three digit long number (a number between 0 and 999) and converts it into
    alphabetical form.
    """
    was_just_zeros = True
    alphabetical_number = str()

    if number[0] != "0":
        alphabetical_number += NUMS_SINGLE_DIGIT_DICT[number[0]] + "hundred and "
        was_just_zeros = False
    elif last_3_digits:
        alphabetical_number += "and "


    if number[1] != "0":
        was_just_zeros = False

        if number[1] == "1":
            alphabetical_number +=  NUMS_TEENS_DICT[number[1]+number[2]]
            return alphabetical_number.rstrip(), was_just_zeros
        else:
            alphabetical_number += NUMS_DOUBLE_DIGIT_DICT[number[1]]

    if number[2] != "0":
        was_just_zeros = False
        alphabetical_number += NUMS_SINGLE_DIGIT_DICT[number[2]]

    if alphabetical_number.endswith("and "):# or alphabetical_number.startswith("and "):
        # alphabetical_number = alphabetical_number.lstrip("and ")
        alphabetical_number = alphabetical_number.rstrip("nd ")
        # this seemingly redundant double use of the rstrip function is to avoid the
        # 'd' in hundred from being removed as well as the 'and'.
        alphabetical_number = alphabetical_number.rstrip(" a")

    return alphabetical_number, was_just_zeros


def cents_number_to_words(cents):
    """This function deals with any cents left over in the number"""
    while len(cents) > 2:
        # the program rounds down to the nearest cent for simplicity
        cents.pop()

    if len(cents) == 1:
        cents.append("0")
    
    cents_in_words, was_just_zeros = triple_digit_num_to_words(["0"]+cents)

    if not was_just_zeros:
        if cents_in_words == "one ":
            return " and one cent"
        else:
            return "and " + cents_in_words + " cents"
    else:
        return ""


def words_to_number(words):
    print("Words to number function called on", words)

    # check that the input is valid
    for word in words:
        word = word.replace(".", "")

        if word not in WORDS_SINGLE_DIGIT_DICT and \
           word not in WORDS_TEENS_DICT and \
           word not in WORDS_DOUBLE_DIGIT_DICT and \
           word not in WORDS_LARGE_NUMS_DICT and \
           word != "hundred" and \
           word not in WORDS_KEYWORDS_LIST:
            sys.exit("ERROR: This input is not a valid number in word form.\n" + \
                     "Please make sure you have spelled each word correctly and don't use\n" + \
                     "'-' between words.\n\nThe unrecognised word was: {}\n".format(word))
    
    # parse the input and translate

    final_number = 0
    word_index = 0
    error_detected = False

    while word_index < len(words):
        current_number = 0

        if words[word_index] in WORDS_KEYWORDS_LIST:
            word_index += 1

        elif words[word_index] in WORDS_SINGLE_DIGIT_DICT:
            current_number = WORDS_SINGLE_DIGIT_DICT[words[word_index]]
            word_index += 1
            # print(current_number)
            try:
                if words[word_index] == "hundred":
                    current_number *= 100
                    # print("number times hundred", current_number)
                    word_index += 1
                    if words[word_index] in WORDS_LARGE_NUMS_DICT:
                        # print("words[word_index] is:"+ words[word_index]+":")
                        current_number *= WORDS_LARGE_NUMS_DICT[words[word_index]]
                        # print("The current number is now:", current_number)
                        # final_number += current_number
                        # print("word_index is", word_index)
                        word_index += 1
                
                elif words[word_index] in WORDS_LARGE_NUMS_DICT:
                    current_number *= WORDS_LARGE_NUMS_DICT[words[word_index]]
                    # final_number += current_number
                    word_index += 1
                
                else:
                    pass
                
                # final_number += current_number

            except IndexError:
                final_number += current_number
                break

        elif words[word_index] in WORDS_TEENS_DICT:
            current_number = WORDS_TEENS_DICT[words[word_index]]
            word_index += 1

            try:
                if words[word_index] in WORDS_LARGE_NUMS_DICT:
                    current_number *= WORDS_LARGE_NUMS_DICT[words[word_index]]
                    # final_number += current_number
                    word_index += 1
                else:
                    pass

                # final_number += current_number

            except IndexError:
                # could bring this out of all if statements potentially
                final_number += current_number
                break

        elif words[word_index] in WORDS_DOUBLE_DIGIT_DICT:
            current_number = WORDS_DOUBLE_DIGIT_DICT[words[word_index]]
            word_index += 1

            try:
                if words[word_index] in WORDS_SINGLE_DIGIT_DICT:
                    current_number += WORDS_SINGLE_DIGIT_DICT[words[word_index]]
                    word_index += 1

                if words[word_index] in WORDS_LARGE_NUMS_DICT:
                    current_number *= WORDS_LARGE_NUMS_DICT[words[word_index]]
                    # final_number += current_number
                    word_index += 1
                else:
                    pass

                # final_number += current_number

            except IndexError:                
                final_number += current_number
                break

        else:
            break

        final_number += current_number

    print("final number is", final_number)

    # for word in words[::]:
    #     if word in WORDS_KEYWORDS_LIST:
    #         continue
    #     elif word in WORDS_LARGE_NUMS_DICT:      




arguments = sys.argv
main(arguments[1:])

# NOTES:
# 
# In the words to number function, call another helper function that checks that the input is a valid string
# representing a number. e.g. it has no numbers in it, and all words are in the dictionaries. Use lower() function
# at beginning on input.
#
# Do error handling in number to words function that checks if there are more than two digits after the decimal
# point and rounds down if so. Use math.floor().
# negatives