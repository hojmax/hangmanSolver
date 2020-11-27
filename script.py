dictionaryFile = open("insert file path for dictionary.txt", "r")
dictionary = dictionaryFile.read().split("\n")
dictionaryFile.close()

def getPossibleWords(incompleteWord, ruledOutCharacters, usedCharacters, candidates):
    output = []
    for word in candidates:
        if len(word)==len(incompleteWord):
            isCandidate = True
            i = 0
            while isCandidate and i < len(word):
                if (word[i] in ruledOutCharacters or
                   (incompleteWord[i] != '_' and incompleteWord[i] != word[i]) or
                   (incompleteWord[i] == '_' and word[i] in usedCharacters)):
                    isCandidate = False
                else:
                    i += 1
            if isCandidate:
                output.append(word)
    return output

def getUsedCharacters(incompleteWord):
    usedCharacters = set()
    for i in range(len(incompleteWord)):
        if incompleteWord[i] != '_':
            usedCharacters.add(incompleteWord[i])
    return usedCharacters

def getBestGuess(incompleteWord,ruledOutCharacters):
    usedCharacters = getUsedCharacters(incompleteWord)
    candidates = getPossibleWords(incompleteWord,ruledOutCharacters,usedCharacters,dictionary)
    if len(candidates)==0:
        print("Error: Either the word is not in the dictionary or there has been incorrect input.")
    elif len(candidates)==1:
        print("The answer is: %s"%candidates[0])
    else:
        bestCharacter = '_'
        bestExpectedValue = float('inf')
        for i in range(26):
            current = chr(97+i)
            if current in usedCharacters or current in ruledOutCharacters:
                continue
            positionCount = dict()
            for word in candidates:
                indices = tuple([pos for pos, char in enumerate(word) if char == current])
                if len(indices) > 0:
                    if indices in positionCount:
                        positionCount[indices] += 1
                    else:
                        positionCount[indices] = 1
            expectedValue = 0
            leftOverSum = len(candidates)
            for key, value in positionCount.items():
                expectedValue += value / len(candidates) * value
                leftOverSum -= value
            expectedValue += leftOverSum / len(candidates) * leftOverSum
            if expectedValue < bestExpectedValue:
                bestExpectedValue = expectedValue
                bestCharacter = current
        print("Candidates left: %s"%len(candidates))
        print("Best guess: " + bestCharacter)

# Words are written in small caps
# Unknown characters are denoted by '_'
# Example: "inf_rm_tion"
# The ruled out characters are represented by a set
# Example: {'b', 'y'}
# Example of function call: getBestGuess("inf_rm_tion", {'b', 'y'})
