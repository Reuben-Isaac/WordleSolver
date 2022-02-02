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
    filtered_wordlist = []
    print(wordlist)
    has_greens = None
    for word in wordlist:
        cond_met = None
        if len(greens) > 0:
            has_greens = True
            for i in range(len(greens)):
                cond_met = False
                green_letter = list(greens.keys())[i]
                print(word, "should have", green_letter, 'at', list(greens.values())[i], ". ", word, "has",
                      word[list(greens.values())[i]])
                if green_letter != word[list(greens.values())[i]]:
                    cond_met = True
                else:
                    break
        if cond_met:
            filtered_wordlist.append(word)
            wordlist.remove(word)
            print('removed', word)

    print(len(filtered_wordlist))
    print(len(wordlist))

    for word in wordlist:
        print(word)
        append = None
        remove = None
        if len(yellows) > 0:
            for i in range(len(yellows)):
                append = False
                remove = False
                yellow_letter = list(yellows.keys())[i]
                # print(word, "should not have", yellow_letter, 'at', list(yellows.values())[i], ". ", word, "has", word[list(yellows.values())[i]])

                if type(list(yellows.values())[i]) is list:
                    for position in list(yellows.values())[i]:
                        if has_greens:
                            if yellow_letter == word[position]:
                                remove = True
                        else:
                            if yellow_letter != word[position] and yellow_letter in word:
                                append = True
                else:
                    if has_greens:
                        if yellow_letter == word[list(yellows.values())[i]]:
                            remove = True
                        else:
                            break
                    else:
                        if yellow_letter != word[list(yellows.values())[i]] and yellow_letter in word:
                            append = True
                        else:
                            break
        if remove:
            wordlist.remove(word)
            print('removed', word)
        if append:
            wordlist.append(word)
            print('appended', word)

    return wordlist


def main():
    removed = 'an'
    greens = {'i': 2, 't': 4}
    yellows = {'s': 0}
    wordlist = create_wordlist(removed)
    wordlist = process_green_yellow(greens, yellows, wordlist)
    # scored_wordlist = total_letter_prob(wordlist)
    scored_wordlist = positional_prob(wordlist)
    print(scored_wordlist)
    scored_wordlist_df = pd.DataFrame(scored_wordlist.items())
    #print(scored_wordlist_df.sort_values([1, 0], ascending=False))
    #print(max(scored_wordlist, key=scored_wordlist.get))
    return None


if __name__ == "__main__":
    main()
