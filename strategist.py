from english_words import english_words_lower_alpha_set
from nltk.corpus import words
from collections import defaultdict
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

import random

import pandas as pd


def plot_probabilities(sorted_probabilities_comb):
    X = range(len(sorted_probabilities_comb))
    Y = []
    for item in sorted_probabilities_comb:
        Y.append(item[1])

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X, Y)
    plt.show()

class WordleStrategist(object):
    def __init__(self):
        guess_word_df = pd.read_csv('guesses.txt', header= None)
        guess_word_list = guess_word_df[0].tolist() 
        self.five_word_list = guess_word_list

        # for word in english_words_lower_alpha_set:
        #     if len(word)==5:
        #         self.five_word_list.append(word)

        print("Initial number of possible words:", len(self.five_word_list))

    def give_initial_suggestions(self, num_suggestions=5):
        raise NotImplementedError("give_initial_suggestions is needed for the child class of the wordlestrategist")

    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        raise NotImplementedError("give_suggestions_from_obs is needed for the child class of the wordlestrategist")


class OccurrenceWordleStrategist(WordleStrategist):
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

    def trim_word_list(self, black, black_pos, yellow, yellow_pos, green, green_pos):
    #   when triming the word list, considering both green and black is important.
    #   I found more easier way than considering both green and black. 
        # black_and_yellow = ''.join(set(black).intersection(yellow))
        # black_and_green = ''.join(set(black).intersection(green))
        # black_and_color = black_and_yellow + black_and_green
        # count_repeated = black.count(black_and_color)
        # print(count_repeated)
        # black_and_color_pos = []
        # for character2 in black_and_color:
        #     for character, pos in zip(black, black_pos):
        #         if character2 == character:
        #             black_and_color_pos.append(pos)
        
        # black_and_color = black_and_color*count_repeated
        # print('determine where is wrong', black_and_color, black_and_color_pos)

        trimmed_list = deepcopy(self.five_word_list)
        
        assert len(yellow) == len(yellow_pos)
        assert len(green) == len(green_pos)
        # assert len(black_and_color) == len(black_and_color_pos)
        assert len(np.intersect1d(yellow_pos, green_pos)) == 0
        


        for word in self.five_word_list:
            word_is_trimed = False
            
            for character in black:
                if (character in word) & (character not in green):
                    trimmed_list.remove(word)
                    word_is_trimed = True
                    break
            if word_is_trimed:
                continue

            # for character, pos in zip(black_and_color, black_and_color_pos):
            #     if word[pos] == character:
            #         trimed_list.remove(word)
            #         word_is_trimed = True
            #         break
            # if word_is_trimed:
            #     continue

            for character, pos in zip(green, green_pos):
                if word[pos] != character:
                    trimmed_list.remove(word)
                    word_is_trimed = True
                    break
            if word_is_trimed:
                continue

            for character, pos in zip(yellow, yellow_pos):
                if character not in word:
                    trimmed_list.remove(word)
                    break
                if word[pos] == character:
                    trimmed_list.remove(word)
                    break

        temp = list('qwert')

        for i, char in zip(black_pos, black):
            temp[i] = char
        for i, char in zip(yellow_pos, yellow):
            temp[i] = char        
        for i, char in zip(green_pos, green):
            temp[i] = char
        word_itself ="".join(temp)
        if word_itself in trimmed_list:
            trimmed_list.remove(word_itself)

        return trimmed_list
        
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        trimed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimed_list
            print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_initial_suggestions(self, num_suggestions=5):
        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)



class RandomWordleStrategist(WordleStrategist):
    def __init__(self):
        super().__init__()
    
    def give_suggestions_from_list(self, five_word_list, num_suggestions):
        if len(five_word_list) > num_suggestions:
            random_suggestions = random.sample(five_word_list, num_suggestions)
        else:
            random_suggestions = five_word_list
        print(random_suggestions) # suggestions
        return random_suggestions

    def trim_word_list(self, black, black_pos, yellow, yellow_pos, green, green_pos):
    #   when triming the word list, considering both green and black is important.
    #   I found more easier way than considering both green and black. 

        trimmed_list = deepcopy(self.five_word_list)
        
        assert len(yellow) == len(yellow_pos)
        assert len(green) == len(green_pos)
        assert len(np.intersect1d(yellow_pos, green_pos)) == 0
        
        for word in self.five_word_list:
            word_is_trimed = False
            
            for character in black:
                if (character in word) & (character not in green):
                    trimmed_list.remove(word)
                    word_is_trimed = True
                    break
            if word_is_trimed:
                continue

            for character, pos in zip(green, green_pos):
                if word[pos] != character:
                    trimmed_list.remove(word)
                    word_is_trimed = True
                    break
            if word_is_trimed:
                continue

            for character, pos in zip(yellow, yellow_pos):
                if character not in word:
                    trimmed_list.remove(word)
                    break
                if word[pos] == character:
                    trimmed_list.remove(word)
                    break

        temp = list('qwert')

        for i, char in zip(black_pos, black):
            temp[i] = char
        for i, char in zip(yellow_pos, yellow):
            temp[i] = char        
        for i, char in zip(green_pos, green):
            temp[i] = char
        word_itself ="".join(temp)
        if word_itself in trimmed_list:
            trimmed_list.remove(word_itself)

        return trimmed_list
        
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        trimed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimed_list
            print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_initial_suggestions(self, num_suggestions=5):
        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)


class MixedWordleStrategist(WordleStrategist):
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
        sorted_probabilities_comb = sorted(probabilities_comb.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_probabilities_comb[:num_suggestions]) # suggestions
        return sorted_probabilities_comb[:num_suggestions]

    def trim_word_list(self, black, black_pos, yellow, yellow_pos, green, green_pos):
 

        trimmed_list = deepcopy(self.five_word_list)
        
        assert len(yellow) == len(yellow_pos)
        assert len(green) == len(green_pos)
        assert len(np.intersect1d(yellow_pos, green_pos)) == 0
        

        for word in self.five_word_list:
            word_is_trimed = False
            
            for character in black:
                if (character in word) & (character not in green):
                    trimmed_list.remove(word)
                    word_is_trimed = True
                    break
            if word_is_trimed:
                continue

            for character, pos in zip(green, green_pos):
                if word[pos] != character:
                    trimmed_list.remove(word)
                    word_is_trimed = True
                    break
            if word_is_trimed:
                continue

            for character, pos in zip(yellow, yellow_pos):
                if character not in word:
                    trimmed_list.remove(word)
                    break
                if word[pos] == character:
                    trimmed_list.remove(word)
                    break

        temp = list('qwert')

        for i, char in zip(black_pos, black):
            temp[i] = char
        for i, char in zip(yellow_pos, yellow):
            temp[i] = char        
        for i, char in zip(green_pos, green):
            temp[i] = char
        word_itself ="".join(temp)
        if word_itself in trimmed_list:
            trimmed_list.remove(word_itself)

        return trimmed_list

    def give_random_from_list(self, five_word_list, num_suggestions):
        if len(five_word_list) > num_suggestions:
            random_suggestions = random.sample(five_word_list, num_suggestions)
        else:
            random_suggestions = five_word_list
        print(random_suggestions) # suggestions
        return random_suggestions

        
    def give_suggestions_from_obs(self, black, black_pos, yellow, yellow_pos, green,
                                  green_pos, num_suggestions=5, explore=False):
        trimed_list = self.trim_word_list(black, black_pos, yellow, yellow_pos, green, green_pos)

        if not explore:
            self.five_word_list = trimed_list
            print("Number of valid words remains:", len(self.five_word_list))

        return self.give_suggestions_from_list(self.five_word_list, num_suggestions)

    def give_initial_suggestions(self, num_suggestions=5):
        return self.give_random_from_list(self.five_word_list, num_suggestions)

