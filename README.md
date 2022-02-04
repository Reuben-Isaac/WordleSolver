# WordleSolver 
#### Created by Reuben Isaac
##### Description
The `main.py` script allows users to input the grey, yellow, and green letters from a Wordle game. The result is a
dataframe with the best possible words to use. User judgement is required to assess if the "best" word is a plausible word.

The algorithm works by using the probability that a letter is to occur in a certain position of the word. The possible word guesses are associated with a "score" (shown in pandas DataFrame). Each word's "score" reflects the combined probability of all the letters in the word.

    

    
##### Instructions
* The `removed` variable should be a string of all the letters not present in the word. 
* The `greens` and `yellows` variables should be dictionaries where each key is a separate green/yellow letter as a string. The values of each dictionary are lists corresponding to the positions of the green/yellow letters.

```
removed = 'abcde'
greens = {'f': [0], 'g': [1, 2]}
yellows = {'h': [3, 4]}
```
 
**Note: 1st to 5th letter positions are from indexed 0 to 4**
