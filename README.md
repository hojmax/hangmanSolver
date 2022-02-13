# hangman_solver
This solver works by calcuating the expected number of remaining possible words for each possible guess (a-z) and choosing the character with the lowest expected value. This solver is currently configured for english, but the algorithm can be used for any language. It is also to be noted that this solver does not follow the safest hangman strategy, and will take riskier options if they have higher informational value. Another sidenote is that this solver is of course only as potent as its dictionary is expansive. As of now the dictionary contains 333.333 english words and their frequencies. Altough this a vast vocabulary, it may not at all times be sufficient ('jiujitsu' is for example not present). Therefore add to the dictionary as needed.
# Execution
You can call `evaluate()` from the command line as can be seen in the example below. The first argument is 'evaluate', the second the partially obfuscated word, with all the following arguments being ruled out characters. In the example the word 'information' is unveiled in 5 guesses. 
```shell
hangmanSolver % python script.py evaluate ___________
Number of Candidates: 17038
Expected Number of Candidates After Move: 1275.809674464681
Best Guess: e

hangmanSolver % python script.py evaluate ___________ e
Number of Candidates: 3951
Expected Number of Candidates After Move: 260.3057366762242
Best Guess: i

hangmanSolver % python script.py evaluate i_______i__ e
Number of Candidates: 44
Expected Number of Candidates After Move: 7.985458094476008
Best Guess: o

hangmanSolver % python script.py evaluate i__o____io_ e
Number of Candidates: 11
Expected Number of Candidates After Move: 2.005721347970188
Best Guess: m

hangmanSolver % python script.py evaluate i__o_m__io_ e
Number of Candidates: 2
Expected Number of Candidates After Move: 1.0
Best Guess: c

hangmanSolver % python script.py evaluate i__o_m__io_ e c
The answer is: information
```
You can also simulate a game of hangman by running ```python script.py simulate **word_of_choice**```.
