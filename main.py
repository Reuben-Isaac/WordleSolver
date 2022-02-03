import string
import pandas as pd
import itertools

word_len = 5

# Import letter position probability csv
pos_prob_df = pd.read_csv('position_probability.csv', header=None)

# print(pos_prob_df)
letter_list = list(pos_prob_df.iloc[:][0])

# Import all Wordle words
with open('wordle_words.txt') as file:
    wordle_dict = file.read().splitlines()
    file.close()
    wordle_dict = set(wordle_dict)


def positional_prob(wordlist):
    """Returns a score for the likelihood of letters in a word occurring"""
    word_prob = {}
    for word in wordlist:
        prob = 1
        letter_count = 1
        for letter in word:
            if letter in word[0:letter_count - 1] and letter_count > 2:
                loc_prob = 1e-2
                # print('repeated letter')
            else:
                letter_index = letter_list.index(letter)
                loc_prob = pos_prob_df.iloc[letter_index][letter_count]
            prob = loc_prob * prob
            letter_count += 1
        word_prob[word] = prob
    return word_prob


def total_letter_prob(wordlist):
    letter_freq = {'e': 10.7,
                   'a': 8.5,
                   'r': 7.8,
                   'o': 6.5,
                   't': 6.3,
                   'l': 6.2,
                   'i': 5.8,
                   's': 5.8,
                   'n': 5.0,
                   'c': 4.1,
                   'u': 4.0,
                   'y': 3.7,
                   'd': 3.4,
                   'h': 3.4,
                   'p': 3.2,
                   'm': 2.7,
                   'g': 2.7,
                   'b': 2.4,
                   'f': 2.0,
                   'k': 1.8,
                   'w': 1.7,
                   'v': 1.3,
                   'z': 0.3,
                   'x': 0.3,
                   'q': 0.3,
                   'j': 0.2}

    word_prob = {}
    for word in wordlist:
        prob = 1
        for letter in word:
            prob = letter_freq[letter] * prob
        word_prob[word] = prob
    return word_prob


# def verify_word(test_word, dictionary):


def create_wordlist(removed_letters):
    """Create a 5-letter sequence, verifies if it is a word, and appends it to a list"""
    s = string.ascii_lowercase
    if removed_letters is not None:
        for letter in removed_letters:
            # print(letter)
            s = s.replace(letter, "")

    letter_combo = [''.join(i) for i in itertools.product(s, repeat=word_len)]
    wordlist = []
    # print(type(wordlist))

    for i in range(len(letter_combo)):
        if letter_combo[i] in wordle_dict:
            wordlist.append(letter_combo[i])

    return wordlist


def process_green_yellow(greens, yellows, wordlist):
    sing_filtered_wl = []
    dbl_filtered_wl = []

    if len(greens) > 0:
        has_greens = True
    else:
        has_greens = False
        sing_filtered_wl = wordlist

    if has_greens:
        for word in wordlist:
            append = None
            for i in range(len(greens)):
                green_letter = list(greens.keys())[i]
                for j in range(len(list(greens.values())[i])):
                    position = list(greens.values())[i][j]
                    if green_letter == word[position]:
                        append = True
                    else:
                        append = False
                        break
                if not append:
                    break
            if append:
                sing_filtered_wl.append(word)
                #print('appended', word)

    if len(yellows) > 0:
        has_yellows = True
    else:
        has_yellows = False
        dbl_filtered_wl = sing_filtered_wl

    if has_yellows:
        for word in sing_filtered_wl:
            append = None
            for i in range(len(yellows)):
                yellow_letter = list(yellows.keys())[i]
                for j in range(len(list(yellows.values())[i])):
                    position = list(yellows.values())[i][j]
                    if yellow_letter != word[position] and yellow_letter in word:
                        append = True
                    else:
                        append = False
                        break
                if not append:
                    break
            if append:
                dbl_filtered_wl.append(word)
                #print('appended', word)

    return dbl_filtered_wl


def main():
    removed = 'sarbmo'
    greens = {'i': [1], 'n': [2], 'g': [3], 'e': [4]}
    yellows = {}
    wordlist = create_wordlist(removed)
    wordlist = process_green_yellow(greens, yellows, wordlist)
    # scored_wordlist = total_letter_prob(wordlist)
    scored_wordlist = positional_prob(wordlist)
    scored_wordlist_df = pd.DataFrame(scored_wordlist.items())
    print(scored_wordlist_df.sort_values([1, 0], ascending=False))
    print(max(scored_wordlist, key=scored_wordlist.get))
    return None


if __name__ == "__main__":
    main()
