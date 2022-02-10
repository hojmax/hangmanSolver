dictionaryFile = open('dictionary.txt', 'r')
dictionary = dictionaryFile.read().split('\n')
dictionaryFile.close()


def getPossibleWords(incompleteWord, ruledOutCharacters, usedCharacters, candidates):
    possibleWords = []
    for word in candidates:
        if len(word) != len(incompleteWord):
            continue
        i = 0
        while i < len(word):
            if word[i] in ruledOutCharacters:
                break
            if incompleteWord[i] != '_' and incompleteWord[i] != word[i]:
                break
            if incompleteWord[i] == '_' and word[i] in usedCharacters:
                break
            i += 1
        passedTest = i == len(word)
        if passedTest:
            possibleWords.append(word)
    return possibleWords


def getUsedCharacters(incompleteWord):
    usedCharacters = set(list(incompleteWord))
    usedCharacters.remove('_')
    return usedCharacters


def getBestGuess(incompleteWord, ruledOutCharacters):
    usedCharacters = getUsedCharacters(incompleteWord)
    candidates = getPossibleWords(
        incompleteWord, ruledOutCharacters, usedCharacters, dictionary)
    if len(candidates) == 0:
        print('No matches: Either the word is not in the dictionary or the input is incorrect.')
    elif len(candidates) == 1:
        print('The answer is: %s' % candidates[0])
    else:
        bestCharacter = ''
        bestExpectedValue = float('inf')
        for i in range(26):
            current = chr(97+i)
            if current in usedCharacters or current in ruledOutCharacters:
                continue
            positionCount = dict()
            for word in candidates:
                indices = tuple(
                    [pos for pos, char in enumerate(word) if char == current])
                if len(indices) == 0:
                    continue
                if indices in positionCount:
                    positionCount[indices] += 1
                else:
                    positionCount[indices] = 1
            expectedValue = 0
            leftOverSum = len(candidates)
            for value in positionCount.values():
                expectedValue += value / len(candidates) * value
                leftOverSum -= value
            expectedValue += leftOverSum / len(candidates) * leftOverSum
            if expectedValue < bestExpectedValue:
                bestExpectedValue = expectedValue
                bestCharacter = current
        print(f'Candidates left: {len(candidates)}')
        print(f'Best guess: {bestCharacter}')


# Words are written in small caps
# Unknown characters are denoted by '_'
# Example: 'inf_rm_ti_n'
# The ruled out characters are represented by a set
# Example: {'b', 'y'}
# Example of function call: getBestGuess('inf_rm_ti_n', {'b', 'y'})
