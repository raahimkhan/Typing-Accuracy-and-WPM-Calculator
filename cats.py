from utils import *
from ucb import main, interact, trace
from datetime import datetime
import functools

def choose(paragraphs, select, k):
    filtered = list(filter(select, paragraphs))
    length = len(filtered)
    if k < length:
        s = filtered[k]
        return s
    else:
        return ''

def about(topic):
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    return lambda paragraph: any(word in lower(remove_punctuation(paragraph)) for word in topic)

def accuracy(typed, reference):
    typed_words = split(typed)
    reference_words = split(reference)
    if typed == '':
        return 0.0
    else:
        length_typed = len(typed_words)
        length_ref = len(reference_words)
        if length_typed == length_ref:
            correct = 0
            i = 0
            for w in typed_words:
                if w == reference_words[i]:
                    correct = correct + 1
                i = i + 1
            return (correct / length_ref) * 100
        elif length_typed < length_ref:
            correct = 0 
            for i in range(length_typed):
                if typed_words[i] == reference_words[i]:
                    correct = correct + 1
            return (correct / length_typed) * 100
        else:
            correct = 0
            for i in range(length_typed):
                if i < length_ref:
                    if typed_words[i] == reference_words[i]:
                        correct = correct + 1
                else:
                    break
            return (correct / length_typed) * 100

def wpm(typed, elapsed):
    assert elapsed > 0, 'Elapsed time must be positive'
    total = 0
    for i in typed:
        total = total + 1
        
    wordsPM = float((total / 5) / (elapsed / 60))
    return wordsPM

def autocorrect(user_word, valid_words, diff_function, limit):
    if user_word in valid_words:
        return user_word
    
    else:
        diff = 10000
        current = ''
        lst = []
        for word in valid_words:
            if diff_function(user_word, word, limit) < diff:
                diff = diff_function(user_word, word, limit)
                current = word
                if len(word) != len(lst[0]):
                    lst.clear()
                    lst.append(current)
                else:
                    lst.append(current)
            else:
                continue
        if len(lst) == 1:
            if len(lst[0]) < limit:
                return lst[0]
            else:
                return user_word
        else:
            return valid_words[0]


def final_diff(start, goal, limit):
    return lambda start, goal, limit: abs(len(goal) - len(start))


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True after being implemented


def memo(f):
    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
