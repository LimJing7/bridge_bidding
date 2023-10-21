class Contract(): 
    def __init__(self, level, suit, doubles, vuln): 
        self.level = level # str: '1' - '7'
        self.par = int(self.level) + 6
        self.suit = suit # str: 'C', 'D', 'H', 'S', 'NT'
        self.trick_score = {
            'C': 20,
            'D': 20,
            'H': 30,
            'S': 30,
            'NT': 30
        }
        self.doubles = doubles # str: '', 'x', 'xx'
        self.vuln = vuln # int: 0: not vuln, 1: vuln
        self.double_mult = {'': 1, 'x': 2, 'xx': 4}
        self.penalty_score = {
            0: { # not vuln
                1: 100,
                2: 200,
                3: 200, 
                4: 300
            }, 
            1: { # vuln
                1: 200, 
                2: 300, 
                3: 300,
                4: 300
            }
        }
        self.bonus_score = {
            0: { # not vuln
                'part': 50,
                'game': 300,
                'slam': 800,
                'grand': 1300,
            }, 
            1: { # vuln
                'part': 50,
                'game': 500,
                'slam': 1250,
                'grand': 2000,
            }
        }

    def score(self, tricks): # tricks is str: '0' - '13'
        
        self.tricks = int(tricks)
        if self.tricks < self.par: # you are down! 
            if self.doubles == '': # not doubled
                return -(self.par - self.tricks)*50*(self.vuln+1)

            else: # doubled or redoubled
                pen = 0
                for undertrick in range(1, self.par-self.tricks+1): 
                    try: 
                        pen += self.penalty_score[self.vuln][undertrick]
                    except KeyError: 
                        pen += self.penalty_score[self.vuln][4]
                if self.doubles == 'x': 
                    return -pen
                else: # redoubled score is just twice of doubled
                    return -2*pen

        else: # you made! 
            
            if self.suit == 'NT': 
                base_score = (int(self.level)*30 + 10)*self.double_mult[self.doubles]
            else: 
                base_score = int(self.level)*self.trick_score[self.suit]*self.double_mult[self.doubles]
            
            if self.par == 13: # grand slam
                if self.doubles == '': # you are not doubled
                    return base_score + self.bonus_score[self.vuln]['grand'] # cant have overtricks in a grand slam
                else: 
                    return base_score + self.bonus_score[self.vuln]['grand'] + 25*self.double_mult[self.doubles]
            elif self.par == 12: # small slam
                bonus_score = self.bonus_score[self.vuln]['slam']
            elif base_score >= 100: # game
                bonus_score = self.bonus_score[self.vuln]['game']
            else: # partscore
                bonus_score = 50

            overtricks = self.tricks - self.par # can be 0
            if self.doubles == '': # you are not doubled
                return base_score + bonus_score + overtricks*self.trick_score[self.suit]
            else: # you are doubled or redoubled
                return base_score + bonus_score + overtricks*50*self.double_mult[self.doubles]*(self.vuln+1) + 25*self.double_mult[self.doubles]


        