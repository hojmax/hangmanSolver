import numpy as np


def getDictionary():
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


def isPossibleWord(word, incompleteWord, ruledOutCharacters, usedCharacters):
    if len(word) != len(incompleteWord):
        return False
    for i, e in enumerate(word):
        if e in ruledOutCharacters:
            return False
        if incompleteWord[i] != '_' and incompleteWord[i] != e:
            return False
        if incompleteWord[i] == '_' and e in usedCharacters:
            return False
    return True


def getPossibleWords(incompleteWord, ruledOutCharacters, usedCharacters, candidates):
    def word_filter(words):
        return np.vectorize(isPossibleWord)(words, incompleteWord, ruledOutCharacters, usedCharacters)
    return candidates[word_filter(candidates[:, 0])]


def getUsedCharacters(incompleteWord):
    usedCharacters = set(list(incompleteWord))
    usedCharacters.remove('_')
    return usedCharacters


def getBestGuess(candidates, usedCharacters, ruledOutCharacters):
    bestCharacter = ''
    bestExpectedValue = float('inf')
    totalWeight = np.sum(candidates[:, 1])
    for i in range(26):
        current = chr(97+i)
        if current in usedCharacters or current in ruledOutCharacters:
            continue
        positionCount = dict()
        for [word, weight] in candidates:
            indices = tuple([
                pos for pos, char in enumerate(word) if char == current
            ])
            if len(indices) == 0:
                continue
            if indices in positionCount:
                currentWeight, currentCount = positionCount[indices]
                positionCount[indices] = (
                    currentWeight + weight,
                    currentCount + 1
                )
            else:
                positionCount[indices] = (weight, 1)
        if len(positionCount) == 0:
            continue
        expectedValue = 0
        remainingWeight = totalWeight
        remainingCount = len(candidates)
        for weight, count in positionCount.values():
            expectedValue += weight / totalWeight * count
            remainingWeight -= weight
            remainingCount -= count
        expectedValue += remainingWeight / totalWeight * remainingCount
        if expectedValue < bestExpectedValue:
            bestExpectedValue = expectedValue
            bestCharacter = current
    return (bestCharacter, bestExpectedValue)


def evaluate(incompleteWord, ruledOutCharacters):
    dictionary = getDictionary()
    usedCharacters = getUsedCharacters(incompleteWord)
    candidates = getPossibleWords(
        incompleteWord,
        ruledOutCharacters,
        usedCharacters,
        dictionary
    )
    if len(candidates) == 0:
        return print('No matches: Either the word is not in the dictionary or the input is incorrect.')
    if len(candidates) == 1:
        return print(f'The answer is: {candidates[0][0]}')
    guess, expected = getBestGuess(
        candidates,
        usedCharacters,
        ruledOutCharacters
    )
    print(candidates)
    print(f'Number of Candidates: {len(candidates)}')
    print(f'Expected Number of Candidates After Move: {expected}')
    print(f'Best Guess: {guess}')


def simulate_game(hidden_word):
    word_set = set(list(hidden_word))
    guessed = set()
    candidates = getDictionary()

    def obfuscate(word):
        return ''.join([e if e in guessed else '_' for e in word])

    while True:
        incompleteWord = obfuscate(hidden_word)
        usedCharacters = guessed.intersection(word_set)
        ruledOutCharacters = guessed.difference(word_set)
        candidates = getPossibleWords(
            incompleteWord,
            ruledOutCharacters,
            usedCharacters,
            candidates
        )
        print(incompleteWord)
        print()
        if len(candidates) == 0:
            return print('No matches: Either the word is not in the dictionary or the input is incorrect.')
        if len(candidates) == 1:
            print(f'The answer is: {candidates[0][0]}')
            print(f'Incorrect guesses: {len(ruledOutCharacters)}')
            return
        guess, expected = getBestGuess(
            candidates,
            usedCharacters,
            ruledOutCharacters
        )
        print(f'Guess: {guess}')
        guessed.add(guess)


# Words are written in small caps
# Unknown characters are denoted by '_'
# Example: 'i__o_m__io_'
# The ruled out characters are represented by a set
# Example: {'c', 'e'}
# Example of function call: evaluate('i__o_m__io_', {'c', 'e'})
