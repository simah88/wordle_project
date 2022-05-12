from strategist import WordleStrategist, OccurrenceWordleStrategist, RandomWordleStrategist
from wordle_agent import WordleAgent
import numpy as np


# initial stategy based non-repeated english_words.english_words_lower_alpha_set
# "orate", "shiny" 
wordlistsetup = OccurrenceWordleStrategist()
word_list = wordlistsetup.five_word_list
attempt_count =[]
no_answer_words=[]
for word in word_list:
    helper = OccurrenceWordleStrategist()
    a = helper.give_initial_suggestions()
    # print(a[0][0])
    answer = WordleAgent(word)
    #answer = WordleAgent('watch')
    for i in range(20):
        
        black_char, black_id, yellow_char, yellow_id, green_char, green_id = answer.attempt_word(a[0][0])
        # print(black_char, black_id, yellow_char, yellow_id, green_char, green_id)
        a = helper.give_suggestions_from_obs(black_char, black_id, yellow_char, yellow_id, green_char, green_id)
        # print(i, a, answer.word)    
        
        if green_id == [0,1,2,3,4]: #answer.word == a[0][0]
            print('Win: within {0:2d} attempt(s)!'.format(i))
            attempt_count.append(i)
            break
        # if len(a) ==0:
        #     print('Not able to find solution from our word list')
        # if i == 8:
        #     print( 'answer word is', answer.word, ', last suggestion is ', a[0][0])
        #     no_answer_words.append(word)
        


# print(word_list[:100], attempt_count)
print(max(attempt_count), min(attempt_count))
mean_attempt = sum(attempt_count)/len(attempt_count)

difference_square = [ (count - mean_attempt)**2 for count in attempt_count ]
std_attempt = (sum(difference_square)/len(attempt_count))**0.5
print( 'mean:', mean_attempt, 'standard deviation:', std_attempt , 'length of attempt_count', len(attempt_count))
print( no_answer_words,'and length is', len(no_answer_words))

# no answer word list.  
# 
# ['funky', 'louse', 'winch', 'quilt', 'happy', 'spate', 'gaunt', 'shelf', 'monic', 'beige', 'greet', 'begun', 'track', 'bilge', 'colza', 'wyman', 'mousy', 'marie', 'great', 'dutch', 'hadnt', 'dolan', 'weary', 'vacuo', 'clark', 'plate', 'acton', 'baste', 'sweat', 'surah', 'liken', 'other', 'radio', 'roman', 'stung', 'butch', 'mambo', 'watch', 'pause', 'house', 'duane', 'boast', 'pitch', 'bract', 'alvin', 'touch', 'twist', 'tudor', 'smash', 'mangy', 'zomba', 'haunt', 'malay', 'thyme', 'delia', 'levin', 'wordy', 'marcy', 'benny', 'shock', 'radon', 'calve', 'canal', 'boyle', 'booky', 'riven', 'sting', 'akron', 'tampa', 'align', 'waldo', 'ready', 'nifty', 'elfin', 'tribe', 'dumpy', 'bater', 'stark', 'molly', 'revel', 'waltz', 'pater', 'boggy', 'muddy', 'clamp', 'gamma', 'frond', 'bunch', 'below', 'belie', 'gummy', 'talky', 'brian', 'munch', 'stink', 'dixon', 'marsh', 'hater', 'caper', 'stove', 'later', 'bulky', 'peaky', 'witch', 'algol', 'agent', 'front', 'greta', 'penny', 'rouse', 'begot', 'raise', 'delta', 'aspen', 'eaton', 'about', 'angel', 'began', 'crisp', 'haste', 'grasp', 'jumpy', 'estop', 'allyn', 'wrong', 'verge', 'carlo', 'foray', 'stage', 'douce', 'pasty', 'aster', 'bette', 'paste', 'goose', 'bread', 'bible', 'daffy', 'cilia', 'swept', 'taffy', 'stein', 'beaux', 'couch', 'pampa', 'stave', 'tardy', 'glide', 'punch', 'aback', 'ashen', 'focal', 'magna', 'allen', 'steal', 'olden', 'davit', 'tempo', 'clump', 'radix', 'holly', 'canto', 'verna', 'vouch', 'pupal', 'jolly', 'befog', 'amply', 'sprue', 'whatd', 'ascii', 'cater', 'dense', 'debby', 'caste', 'flush', 'aerie', 'heinz', 'apron', 'catch', 'bitch', 'brent', 'coset', 'decry', 'bundy', 'jorge', 'folly', 'pooch', 'gauze', 'alien', 'filly', 'finch', 'bride', 'bella', 'green', 'muggy', 'stomp', 'scout', 'honda', 'elgin', 'beefy', 'melon', 'maxim', 'hardy', 'podge', 'awoke', 'clasp', 'poach', 'verdi', 'radii', 'brave', 'wrack', 'paint', 'dolly', 'dwelt', 'creak', 'basil', 'tenon', 'bonze', 'harpy', 'manse', 'becky', 'ample', 'galen', 'scaly', 'ditch', 'sable', 'belch', 'bathe', 'adopt', 'nolan', 'shout', 'lousy', 'batch', 'stilt', 'clash', 'olsen', 'tough', 'plush', 'noise', 'gregg', 'servo', 'peril', 'billy', 'woman', 'slept', 'floyd', 'booze', 'scald', 'china', 'gunky', 'wally', 'wyeth', 'fitch', 'stead', 'begin', 'dream', 'mango', 'milky', 'hyman', 'vocal', 'blush', 'aisle', 'stake', 'grout', 'nerve', 'nasty', 'stunk', 'teach', 'hindu', 'mafia', 'hasty', 'roast', 'hodge', 'rinse', 'dylan', 'value', 'wormy', 'spend', 'shear', 'media', 'avery', 'pinch', 'crash', 'willa', 'poise', 'alden', 'merit', 'bumpy', 'alloy', 'coast', 'paulo', 'rivet', 'filth', 'bench', 'hefty', 'stalk', 'match', 'greek', 'belly', 'errol', 'bambi', 'trail', 'crate', 'canny', 'dummy', 'forge', 'pouch', 'scott', 'swish', 'betty', 'filmy', 'faint', 'byrne', 'waste', 'dough', 'dicta', 'pauli', 'tense', 'crock', 'curie', 'guise', 'acorn', 'debra', 'prong', 'train', 'hilly', 'basic', 'dandy', 'zesty', 'folic', 'bough', 'union', 'beady', 'ethyl', 'eldon', 'withe', 'liven', 'wilma', 'golly', 'booth', 'youth', 'tepid', 'lithe', 'skate', 'basel', 'guess', 'lathe', 'beech', 'mabel', 'patch', 'human', 'choke', 'fancy', 'boone', 'crown', 'pusan', 'mooch', 'culpa', 'crimp', 'chili', 'magog', 'peggy', 'colby', 'milan', 'genii', 'halve', 'candy', 'sulky', 'mater', 'spunk', 'amiss', 'those', 'cheek', 'mario', 'elton', 'tonal', 'being', 'kapok', 'droll', 'goode', 'anvil', 'verne', 'brash', 'mocha', 'alton', 'peach', 'water', 'final', 'daunt', 'araby', 'mouse', 'marin', 'flute', 'moldy', 'rocky', 'dater', 'terra', 'singe', 'banal', 'hanoi', 'mania', 'abbot', 'hurty', 'handy', 'strum', 'ponce', 'surge', 'lucre', 'salve', 'bugle', 'basin', 'annul', 'peony', 'lykes', 'carry', 'level', 'miaow', 'henry', 'butte', 'terry', 'beach', 'bulge', 'brice', 'babel', 'chore', 'bruno', 'guest', 'tenth', 'stair', 'inman', 'versa', 'flash', 'magma', 'three', 'borne', 'taper', 'mouth', 'scalp', 'burnt', 'begat', 'bronx']
# using these words, I am gonna explore why and where is wrong in my strategist
# in the temp.py file 

# after modification, no answer word list is reduced 9 first, then increased to 11 why it is increased???
#
#['weary', 'nudge', 'gerry', 'colby', 'garry', 'henry', 'later', 'carry', 'pater']

# ['weary', 'barry', 'henry', 'horde', 'parry', 'judge', 'colby', 'alcoa', 'hater', 'kerry', 'mater']




# helper.give_suggestions_from_obs('e',[0], 'rs', [1, 3], 'ae', [2,4]) 
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

# random_sug = RandomWordleStrategist()
# random_sug.give_initial_suggestions()
# random_sug.give_suggestions_from_obs('fungi', [0,1,2,3,4], '', [], '', [])
# random_sug.give_suggestions_from_obs('ldl', [0,2,3], 'a', [1], 'e', [4])
# random_sug.give_suggestions_from_obs('tk', [1,3], '', [], 'sae', [0,2,4])
# random_sug.give_suggestions_from_obs('p', [1], '', [], 'sare', [0,2,3,4])
# random_sug.give_suggestions_from_obs('h', [1], '', [], 'sare', [0,2,3,4])
# random_sug.give_suggestions_from_obs('lye', [0,1,3], 'c', [2], 'e', [4])
#black, black_pos, yellow, yellow_pos, green,green_pos, num_suggestions=5, explore=False)
# import random
# a = [1, 2, 3, 4, 5]
# print(random.sample(a, 3))

# try_wordleagent = WordleAgent('price')
# black_char, black_id, yellow_char, yellow_id, green_char, green_id = try_wordleagent.attempt_word('trial')
# print( black_char, black_id, yellow_char, yellow_id, green_char, green_id )