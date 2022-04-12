
def wordle_agent(word, trial):
    assert len(word) == len(trial)
    black_id =[]
    black_char = ''
    yellow_id = []
    yellow_char =''
    green_id =[]
    green_char = ''

    for i in range(len(word)):
        if word[i] == trial[i]:
            green_id.append(i)
            green_char += trial[i]

    for i in range(len(word)):
        if (word[i] != trial[i]) & (trial[i] not in word ):
            black_id.append(i)
            black_char += trial[i]
        if (word[i] != trial[i]) &  (trial[i] in green_char ):
            black_id.append(i)
            black_char += trial[i]

    for i in range(len(word)):
        if (word[i] != trial[i]) & (trial[i] in word )  & (trial[i] not in green_char ):
            yellow_id.append(i)
            yellow_char += trial[i]
    
    #     elif (word[i] != trial[i]) & (trial[i] not in word ):
    #         black_id.append(i)
    #         black_char += trial[i]
    #     else:
    #         yellow_id.append(i)
    #         yellow_char += trial[i]
            

    return black_char, black_id, yellow_char, yellow_id, green_char, green_id


black_char,black_id, yellow_char, yellow_id, green_char, green_id = wordle_agent('spare', 'erase')
print( black_id, black_char)
print(yellow_char, yellow_id)
print(green_char, green_id)

black_and_yellow = ''.join(set(black_char).intersection(yellow_char))
black_and_green = ''.join(set(black_char).intersection(green_char))
black_and_color = black_and_yellow + black_and_green

print(black_and_yellow,black_and_green, black_and_color)     
print(black_id)