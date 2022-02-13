# hangmanSolver
This solver works by calcuating the expected number of remaining possible words for each possible guess (a-z) and choosing the character with the lowest expected value. This solver is currently configured for english, but the algorithm can be used for any language. It is also to be noted that this solver does not follow the safest hangman strategy, and will take riskier options if they have higher informational value. Another sidenote is that this solver is of course only as potent as its dictionary is expansive. As of now the dictionary contains 333.333 english words and their frequencies. Altough this a vast vocabulary, it may not at all times be sufficient ('jiujitsu' is for example not present). Therefore add to the dictionary as needed.
### Execution
```bash
hangmanSolver % python script.py evaluate ___________
Number of Candidates: 17038
Expected Number of Candidates After Move: 1275.809674464681
Best Guess: e
hangmanSolver % python script.py evaluate ___________ e
```
