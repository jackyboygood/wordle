#
# Wordle harness file.
# Use this to bootstrap your solution.
#

import copy
from typing import Any, Dict, Optional

POSITIONAL_FACTOR = 1
OVERALL_FACTOR = 1

def is_possible(word, greens, yellows, greys):
    for grey in greys:
        if grey in word:
            return False
    
    # green / yellow format: {pos: letter}
    for green in greens.items():
        if word[green[0]] != green[1]:
            return False
        
    for yellow in yellows.items():
        if not yellow[1] in word:
            return False
        
        if word[yellow[0]] == yellow[1]:
            return False

    return True


def purge_list(word_list, guessed_word, guess_response):
    # interpret response
    greens = {}
    yellows = {}
    greys = []

    pos = 0
    for item in guess_response:
        if item == "o":
            greens[pos] = guessed_word[pos]
        elif item == "_":
            yellows[pos] = guessed_word[pos]
        elif item == "x":
            greys.append(guessed_word[pos])
        pos += 1

    # check if possible
    new_list = []
    for word in word_list:
        if is_possible(word, greens, yellows, greys):
            new_list.append(word)
    
    return new_list


def create_guess(word_list):
    # calculate frequency (both in pos and overall)
    frequency_list = [{}, {}, {}, {}, {}]
    overall_frequency = {}
    for word in word_list:
        for i in range (0,5):
            letter = word[i]
            if not letter in frequency_list[i]:
                frequency_list[i][letter] = 0
            frequency_list[i][letter] += 1

            if not letter in overall_frequency:
                overall_frequency[letter] = 0
            overall_frequency[letter] += 1
            

    # calculate commonality
    word_score = {}
    for word in word_list:
        score = 0
        # positional word score
        for i in range (0,5):
            score += POSITIONAL_FACTOR * frequency_list[i][word[i]]

        # overall word score
        letter_set = set()
        for letter in word:
            letter_set.add(letter)

        for uniq_letter in letter_set:
            score += OVERALL_FACTOR * overall_frequency[uniq_letter]
        word_score[word] = score

    # sort words by commonality
    score_sort = dict(sorted(word_score.items(), key=lambda item: item[1], reverse=True))

    # how do I do this better
    for word in score_sort.items():
        return word[0]


def wordle_init(context: Dict[str, Any]):
    """Called once to initialize solver.

    `context` will contain a member `dictionary`, containing a dictionary
    of all possible English words that can be used in the puzzle.

    Args:
        context: Context passed from wordle puzzle runner.
    """
    pass


def wordle_begin(context: Dict[str, Any]):
    """Called at the beginning of each new wordle puzzle.

    This can be used to initialize or reset any state attached to the context.

    Args:
        context: Context passed from wordle puzzle runner.
    """

    # copy dict
    context["remaining_words"] = copy.deepcopy(context["dictionary"])
    context["guesses"] = []


def wordle_guess(
    context: Dict[str, Any], guess_num: int, last_guess: Optional[str]) -> str:
    """Called by game to request a guess.

    Args:
        context: Context passed from wordle puzzle runner.
        guess_num: Current guess number (out of 6).
        last_guess: Response to the last guess (None if guess number is 0).

    Returns:
        Solver's guess word. Must be a 5 letter word present in the game
        dictionary.
    """

    # purge incorrect words
    if guess_num > 0:
        last_guess_word = context["guesses"][guess_num - 1]
        context["remaining_words"] = purge_list(context["remaining_words"], last_guess_word, last_guess)

    guessed_word = create_guess(context["remaining_words"])

    context["guesses"].append(guessed_word)
    return guessed_word
