from english_words import english_words_lower_alpha_set
from nltk.corpus import words
from collections import defaultdict
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

import random

import pandas as pd
import itertools
from tqdm import tqdm


def plot_probabilities(sorted_probabilities_comb):
    X = range(len(sorted_probabilities_comb))
    Y = []
    for item in sorted_probabilities_comb:
        Y.append(item[1])

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X, Y)
    plt.show()

def color_pattern_to_char_position(word, pattern):
    """
    inputs : word is string, pattern is list of string, consisting of 'k' for black,'y' for yellow,'g' for green
    """
    assert len(word) == len(pattern)
    black_char = ''
    black_pos = []
    yellow_char = ''
    yellow_pos = []
    green_char = ''
    green_pos = []
    for i in range(len(word)):
        if pattern[i] =='b':
            black_char+=word[i]
            black_pos.append(i)
        elif pattern[i] == 'y':
            yellow_char+=word[i]
            yellow_pos.append(i)
        else:
            green_char+=word[i]
            green_pos.append(i)
    return black_char, black_pos, yellow_char, yellow_pos, green_char, green_pos

class WordleStrategist(object):
    def __init__(self):
        guess_word_df = pd.read_csv('answers.txt', header= None)
        guess_word_list = guess_word_df[0].tolist() 
        self.five_word_list = guess_word_list

        # print("Initial number of possible words:", len(self.five_word_list))

    def trim_word_list(self, black, black_pos, yellow, yellow_pos, green, green_pos):

        trimmed_list = deepcopy(self.five_word_list)
        
        assert len(yellow) == len(yellow_pos)
        assert len(green) == len(green_pos)
        assert len(np.intersect1d(yellow_pos, green_pos)) == 0

        for word in self.five_word_list:
            word_is_trimmed = False
            
            for character in black:
                if (character in word) and (character not in green) and (character not in yellow):
                    trimmed_list.remove(word)
                    word_is_trimmed = True
                    break
            if word_is_trimmed:
                continue
            
            for character, pos in zip(black, black_pos):
                if (word[pos] == character):
                    trimmed_list.remove(word)
                    word_is_trimmed = True
                    break
            if word_is_trimmed:
                continue

            for character, pos in zip(green, green_pos):
                if word[pos] != character:
                    trimmed_list.remove(word)
                    word_is_trimmed = True
                    break
            if word_is_trimmed:
                continue

            for character, pos in zip(yellow, yellow_pos):
                if character not in word:
                    trimmed_list.remove(word)
                    break
                if word[pos] == character:
                    trimmed_list.remove(word)
                    break

        return trimmed_list

    def give_suggestion_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                 green_pos, explore=False):
        raise NotImplementedError("give_suggestions_from_obs is needed for the child class of the wordlestrategist")


class OccurrenceBasedStrategist(WordleStrategist):
    def __init__(self):
        super().__init__()

    def give_suggestions_from_list(self, five_word_list, num_suggestions):

        probabilities_alpha = defaultdict(lambda : 0)
        for word in five_word_list:
            for alphabet in word:
                probabilities_alpha[alphabet] +=1
        # print( dict(counts_alpha_all))
        # print( sum( counts_alpha_all.values()) )
        total_counts = len(five_word_list) * 5
        # sorted_probabilities_alphabet = sorted(counts_alpha_all.items(), key=lambda x: x[1], reverse=True)
        for alphabet in probabilities_alpha.keys():
            probabilities_alpha[alphabet] /= total_counts

        probabilities_comb = defaultdict(lambda : 0)
        for word in five_word_list:
            probability = 1
            for alphabet in word:
                probability *= probabilities_alpha[alphabet]
            probabilities_comb[word] = probability

        # print(len(probabilities_comb))
        sorted_probabilities_comb = sorted(probabilities_comb.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_probabilities_comb[:num_suggestions]) # suggestions
        return sorted_probabilities_comb[:num_suggestions]
      
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        
        trimmed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimmed_list
            # print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_suggestion_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                 green_pos, explore=False):
        suggestions = self.give_suggestions_from_obs(black, black_pos, yellow, yellow_pos, green,
                                  green_pos, 1, explore)
        return suggestions[0][0]


class RandomStrategist(WordleStrategist):
    def __init__(self):
        super().__init__()
    
    def give_suggestions_from_list(self, five_word_list, num_suggestions):
        if len(five_word_list) > num_suggestions:
            random_suggestions = random.sample(five_word_list, num_suggestions)
        else:
            random_suggestions = five_word_list
        # print(random_suggestions) # suggestions
        return random_suggestions
      
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        trimmed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimmed_list
            # print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_suggestion_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                 green_pos, explore=False):
        suggestions = self.give_suggestions_from_obs(black, black_pos, yellow, yellow_pos, green,
                                  green_pos, 1, explore)
        return suggestions[0]


class MixedStrategist(WordleStrategist):
    """
    Give initial suggestion as random
    Give rest suggestion as based on Occurence
    """
    def __init__(self):
        super().__init__()

    def give_suggestions_from_list(self, five_word_list, num_suggestions):

        probabilities_alpha = defaultdict(lambda : 0)
        for word in five_word_list:
            for alphabet in word:
                probabilities_alpha[alphabet] +=1

        total_counts = len(five_word_list) * 5

        for alphabet in probabilities_alpha.keys():
            probabilities_alpha[alphabet] /= total_counts

        probabilities_comb = defaultdict(lambda : 0)
        for word in five_word_list:
            probability = 1
            for alphabet in word:
                probability *= probabilities_alpha[alphabet]
            probabilities_comb[word] = probability

        # print(len(probabilities_comb))
        sorted_probabilities_comb = sorted(probabilities_comb.keys(), key=lambda x: x[1], reverse=True)
        # print(sorted_probabilities_comb[:num_suggestions]) # suggestions
        return sorted_probabilities_comb[:num_suggestions]

    def give_random_from_list(self, five_word_list, num_suggestions):
        if len(five_word_list) > num_suggestions:
            random_suggestions = random.sample(five_word_list, num_suggestions)
        else:
            random_suggestions = five_word_list
        # print(random_suggestions) # suggestions
        return random_suggestions
   
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        trimmed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimmed_list
            # print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_suggestion_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                 green_pos, explore=False):
        suggestions = self.give_suggestions_from_obs(black, black_pos, yellow, yellow_pos, green,
                                  green_pos, 1, explore)
        return suggestions[0]


class EntropyBasedStrategist(WordleStrategist):
    def __init__(self):
        super().__init__()

    def give_suggestions_from_list(self, five_word_list, num_suggestions):

        color_list = ['k', 'y', 'g'] 
        entropy = defaultdict(lambda : 0.0)
        for word in tqdm(five_word_list, desc = 'entropy check'):
            
            for pattern in itertools.product(color_list, repeat=5):
                black_char, black_pos, yellow_char, yellow_pos, green_char, green_pos = color_pattern_to_char_position(word, pattern)
        
                trimmed_list = self.trim_word_list(black_char, black_pos, yellow_char, yellow_pos, green_char, green_pos)
                prob = len(trimmed_list)/len(five_word_list)
                if prob > 0:
                    entropy[word] -= prob*np.log2(prob) 
            
        sorted_entropy = sorted(entropy.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_entropy[:num_suggestions])
        return sorted_entropy[:num_suggestions]
      
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        if len(black) == 0 and len(yellow) == 0 and len(green) == 0:
            return [('rarer', 1.5348546467182962)]
        trimmed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimmed_list
            # print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_suggestion_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                 green_pos, explore=False):
        suggestions = self.give_suggestions_from_obs(black, black_pos, yellow, yellow_pos, green,
                                  green_pos, 1, explore)
        return suggestions[0][0]
