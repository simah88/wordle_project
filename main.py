from strategist import OccurrenceBasedStrategist, RandomStrategist, MixedStrategist
from wordle_agent import WordleAgent
import numpy as np
import pandas as pd
from tqdm import tqdm


answer_word_df = pd.read_csv('answers.txt', header= None)
answer_word_list = answer_word_df[0].tolist()

for strategist in [OccurrenceBasedStrategist, RandomStrategist, MixedStrategist]:
    attempt_count =[]
    no_answer_words=[]
    for word in tqdm(answer_word_list):
        helper = strategist()
        suggestion = helper.give_suggestion_from_obs('', [], '', [], '', [])
        agent = WordleAgent(word)
        for i in range(6):
            
            black_char, black_id, yellow_char, yellow_id, green_char, green_id = agent.attempt_word(suggestion)
            # print(black_char, black_id, yellow_char, yellow_id, green_char, green_id)
            
            if green_id == [0,1,2,3,4]: #answer.word == a[0][0]
                # print('Win: within {0:2d} attempt(s)!'.format(i))
                attempt_count.append(i+1)
                break
            # if len(a) ==0:
            #     print('Not able to find solution from our word list')
            if i == 5:
                # print( 'answer word is', answer.word, ', last suggestion is ', a[0][0])
                # print('LOST! Fail to complete')
                no_answer_words.append(word)
                break
            
            suggestion = helper.give_suggestion_from_obs(black_char, black_id, yellow_char, yellow_id, green_char, green_id)
            # print(i, a, answer.word)    
            
    print('strategist name', strategist )
    print('maximum attempts to win:', max(attempt_count))
    print('minimum attempts to win:', min(attempt_count))
    mean_attempt = sum(attempt_count)/len(attempt_count)

    difference_square = [ (count - mean_attempt)**2 for count in attempt_count ]
    std_attempt = (sum(difference_square)/len(attempt_count))**0.5
    print( 'mean:', mean_attempt, 'standard deviation:', std_attempt , 'length of attempt_count', len(attempt_count))
    print('Number of no answer words :', len(no_answer_words))
    
    # print( no_answer_words,'and length is', len(no_answer_words))
