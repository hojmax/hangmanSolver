import numpy as np
import sys


def get_dictionary():
    data = np.genfromtxt(
        'word_freq.csv',
        dtype=str,
        delimiter=',',
        skip_header=1
    )
    data = data.astype('object')

    def transform_distribution(x):
        '''Arbitrary transformation function of word frequencies to probabilistic weights.'''
        return np.log(x.astype('int64')) ** 3

    data[:, 1] = transform_distribution(data[:, 1])
    return data


def is_possible_word(word, incomplete_word, ruled_out_characters, used_characters):
    if len(word) != len(incomplete_word):
        return False
    for i, e in enumerate(word):
        if e in ruled_out_characters:
            return False
        if incomplete_word[i] != '_' and incomplete_word[i] != e:
            return False
        if incomplete_word[i] == '_' and e in used_characters:
            return False
    return True


def get_possible_words(incomplete_word, ruled_out_characters, used_characters, candidates):
    def word_filter(words):
        return np.vectorize(is_possible_word)(words, incomplete_word, ruled_out_characters, used_characters)
    return candidates[word_filter(candidates[:, 0])]


def get_used_characters(incomplete_word):
    used_characters = set(list(incomplete_word))
    used_characters.remove('_')
    return used_characters


def get_best_guess(candidates, used_characters, ruled_out_characters):
    best_character = ''
    best_expected_value = float('inf')
    total_weight = np.sum(candidates[:, 1])
    for i in range(26):
        current = chr(97+i)
        if current in used_characters or current in ruled_out_characters:
            continue
        position_count = dict()
        for word, weight in candidates:
            indices = tuple([
                pos for pos, char in enumerate(word) if char == current
            ])
            if len(indices) == 0:
                continue
            if indices in position_count:
                current_weight, current_count = position_count[indices]
                position_count[indices] = (
                    current_weight + weight,
                    current_count + 1
                )
            else:
                position_count[indices] = (weight, 1)
        if len(position_count) == 0:
            continue
        expected_value = 0
        remaining_weight = total_weight
        remaining_count = len(candidates)
        for weight, count in position_count.values():
            expected_value += weight / total_weight * count
            remaining_weight -= weight
            remaining_count -= count
        expected_value += remaining_weight / total_weight * remaining_count
        if expected_value < best_expected_value:
            best_expected_value = expected_value
            best_character = current
    return (best_character, best_expected_value)


def evaluate(incomplete_word, ruled_out_characters):
    dictionary = get_dictionary()
    used_characters = get_used_characters(incomplete_word)
    candidates = get_possible_words(
        incomplete_word,
        ruled_out_characters,
        used_characters,
        dictionary
    )
    if len(candidates) == 0:
        return print('No matches: Either the word is not in the dictionary or the input is incorrect.')
    if len(candidates) == 1:
        return print(f'The answer is: {candidates[0][0]}')
    guess, expected = get_best_guess(
        candidates,
        used_characters,
        ruled_out_characters
    )
    print(f'Number of Candidates: {len(candidates)}')
    print(f'Expected Number of Candidates After Move: {expected}')
    print(f'Best Guess: {guess}')


def simulate_game(hidden_word):
    word_set = set(list(hidden_word))
    guessed = set()
    candidates = get_dictionary()

    def obfuscate(word):
        return ''.join([e if e in guessed else '_' for e in word])

    while True:
        incomplete_word = obfuscate(hidden_word)
        used_characters = guessed.intersection(word_set)
        ruled_out_characters = guessed.difference(word_set)
        candidates = get_possible_words(
            incomplete_word,
            ruled_out_characters,
            used_characters,
            candidates
        )
        print(incomplete_word)
        print()
        if len(candidates) == 0:
            return print('No matches: Either the word is not in the dictionary or the input is incorrect.')
        if len(candidates) == 1:
            print(f'The answer is: {candidates[0][0]}')
            print(f'Incorrect guesses: {len(ruled_out_characters)}')
            return
        guess, expected = get_best_guess(
            candidates,
            used_characters,
            ruled_out_characters
        )
        print(f'Guess: {guess}')
        guessed.add(guess)


if __name__ == '__main__':
    operation = sys.argv[1]
    if operation == 'evaluate':
        incomplete_word = sys.argv[2]
        ruled_out_characters = set(sys.argv[3:])
        evaluate(incomplete_word, ruled_out_characters)
    if operation == 'simulate':
        hidden_word = sys.argv[2]
        simulate_game(hidden_word)
