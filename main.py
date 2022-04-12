from strategist import WordleStrategist, OccurrenceWordleStrategist, RandomWordleStrategist

# initial stategy based non-repeated english_words.english_words_lower_alpha_set
# "orate", "shiny" 
helper = OccurrenceWordleStrategist()
helper.give_initial_suggestions()

helper.give_suggestions_from_obs('e',[0], 'rs', [1, 3], 'ae', [2,4]) 
# first, color and black haven't been account for. 
# second, the word list is not enough. problem of english_word library????

# helper.give_suggestions_from_obs('si', 'hny', [1, 3, 4], '', [], '', [])
# helper.give_suggestions_from_obs('a', 'mn', [0, 2], 'yh', [1,4], '', [])
# helper.give_suggestions_from_obs('bn', '', [], 'eoy', [0,2,4], '', [])


# helper.give_suggestions_from_obs('', [], '', [], '', [])
# helper.give_suggestions_from_obs('', [], '', [], '', [])
# helper.give_suggestions_from_obs('', [], '', [], '', [])
# helper.give_suggestions_from_obs('', [], '', [], '', [])
# helper.give_suggestions_from_obs('', [], '', [], '', [])

random_sug = RandomWordleStrategist()
random_sug.give_initial_suggestions()
random_sug.give_suggestions_from_obs('fungi', [0,1,2,3,4], '', [], '', [])
random_sug.give_suggestions_from_obs('ldl', [0,2,3], 'a', [1], 'e', [4])
random_sug.give_suggestions_from_obs('tk', [1,3], '', [], 'sae', [0,2,4])
random_sug.give_suggestions_from_obs('p', [1], '', [], 'sare', [0,2,3,4])
random_sug.give_suggestions_from_obs('h', [1], '', [], 'sare', [0,2,3,4])
# random_sug.give_suggestions_from_obs('lye', [0,1,3], 'c', [2], 'e', [4])
#black, black_pos, yellow, yellow_pos, green,green_pos, num_suggestions=5, explore=False)
# import random
# a = [1, 2, 3, 4, 5]
# print(random.sample(a, 3))