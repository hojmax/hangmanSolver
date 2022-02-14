# hangman_solver
This solver works by calcuating the expected number of remaining possible words for each possible guess (a-z) and choosing the character with the lowest expected value. The solver also takes word frequency into account, weighting more common words higher. When several options have the same expected value, the algorithm chooses the option with the highest probability of being a correct guess. This solver is currently configured for english, but the algorithm can be used for any language. It is also to be noted that this solver does not follow the safest hangman strategy, and will take riskier options if they have higher informational value. Another sidenote is that this solver is of course only as potent as its dictionary is expansive. As of now the dictionary contains 333.333 english words and their frequencies. Altough this a vast vocabulary, it may not at all times be sufficient ('jiujitsu' is for example not present). Therefore add to the dictionary as needed.
# Execution
You can call `evaluate()` from the command line as can be seen in the example below. The first argument is 'evaluate', the second the partially obfuscated word, with all the following arguments being ruled out characters. In the example the word 'programming' is unveiled in 5 guesses. 
```shell
hangman_solver % python script.py evaluate ___________
Number of Candidates: 17038
Expected Number of Candidates After Move: 1275.809674464681
Best Guess: e

hangman_solver % python script.py evaluate ___________ e
Number of Candidates: 3951
Expected Number of Candidates After Move: 260.3057366762242
Best Guess: i

hangman_solver % python script.py evaluate ________i__ e
Number of Candidates: 464
Expected Number of Candidates After Move: 39.26239664177368
Best Guess: o

hangman_solver % python script.py evaluate __o_____i__ e
Number of Candidates: 16
Expected Number of Candidates After Move: 2.3020667286964644
Best Guess: s

hangman_solver % python script.py evaluate __o_____i__ e s
Number of Candidates: 3
Expected Number of Candidates After Move: 0.9999999999999999
Best Guess: a

hangman_solver % python script.py evaluate __o__a__i__ e s
The answer is: programming
```
You can also simulate a game of hangman with a word of choice by running ```python script.py simulate **word_of_choice**```. This is primarily for testing and evaluating performance.
