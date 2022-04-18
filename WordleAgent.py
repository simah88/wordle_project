
class WordleAgent(object):
    def __init__(self, word):
        """word needs to be the answer of a game."""
        self.word = word 
    
    def attempt_word(self, trial):
        """Finding black, yellow, green characters and indice"""
        assert len(self.word) == len(trial)
        black_id =[]
        black_char = ''
        yellow_id = []
        yellow_char =''
        green_id =[]
        green_char = ''

        for i in range(len(self.word)):
            if self.word[i] == trial[i]:
                green_id.append(i)
                green_char += trial[i]

        for i in range(len(self.word)):
            if (self.word[i] != trial[i]) & (trial[i] not in self.word ):
                black_id.append(i)
                black_char += trial[i]
            if (self.word[i] != trial[i]) &  (trial[i] in green_char ):
                black_id.append(i)
                black_char += trial[i]

        for i in range(len(self.word)):
            if (self.word[i] != trial[i]) & (trial[i] in self.word )  & (trial[i] not in green_char ):
                yellow_id.append(i)
                yellow_char += trial[i]
        
        return black_char, black_id, yellow_char, yellow_id, green_char, green_id

