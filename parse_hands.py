from google.colab import drive
drive.mount('/content/drive')

import json


def get_hands(lines, board):

    seek = 21*(board-1)
    north = {}
    for row in range(seek+3,seek+7):
        suit = ''.join(lines[row].split(' '))[:-1]
        if suit[1:] == '-----':
            north[suit[0]] = ''
        else:
            north[suit[0]] = suit[1:]
    south = {}
    for row in range(seek+11, seek+15):
        suit = ''.join(lines[row].split(' '))[:-1]
        if suit[1:] == '-----':
            south[suit[0]] = ''
        else:
            south[suit[0]] = suit[1:]


    west, east = {}, {}
    for row in range(seek+7, seek+11):
        suits = ''.join(lines[row].split(' '))[:-1]
        if suits.split(suits[0])[1] == '-----':
            west[suits[0]] = ''
        else:
            west[suits[0]] = suits.split(suits[0])[1]
        if suits.split(suits[0])[2] == '-----':
            east[suits[0]] = ''
        else:
            east[suits[0]] = suits.split(suits[0])[2]

    return {'N': north, 'S': south, 'W': west, 'E': east}



def get_scores(lines, board):

    seek = 21*(board-1)
    north, south, west, east = {}, {}, {}, {}

    ns_scores = lines[seek+15][:-1].split(' ')[1:]
    for score in ns_scores:
        if '-' in score:
            continue
        else:
            suit = ''.join([i for i in score if i.isalpha()])
            tricks = score.split(suit)
        if tricks[0] == '': # number is on the right, so it is number of tricks
            if '/' in tricks[1]: # N/S scores
                north[suit] = tricks[1].split('/')[0]
                south[suit] = tricks[1].split('/')[1]
            else:
                north[suit] = tricks[1]
                south[suit] = tricks[1]
        elif tricks[1] == '': # number is on the left, so have to add 6
            if '/' in tricks[0]: # N/S scores
                north[suit] = str(int(tricks[0].split('/')[0])+6)
                south[suit] = str(int(tricks[0].split('/')[1])+6)
            else:
                north[suit] = str(int(tricks[0])+6)
                south[suit] = str(int(tricks[0])+6)
        else:
            raise ValueError(f'incorrect score detected on board {board}')

    ew_scores = lines[seek+16][:-1].split(' ')[1:]
    for score in ew_scores:
        if '-' in score:
            continue
        else:
            suit = ''.join([i for i in score if i.isalpha()])
            tricks = score.split(suit)
        if tricks[0] == '': # number is on the right, so it is number of tricks
            if '/' in tricks[1]: # E/W scores
                east[suit] = tricks[1].split('/')[0]
                west[suit] = tricks[1].split('/')[1]
            else:
                east[suit] = tricks[1]
                west[suit] = tricks[1]
        elif tricks[1] == '': # number is on the left, so have to add 6
            if '/' in tricks[0]: # E/W scores
                east[suit] = str(int(tricks[0].split('/')[0])+6)
                west[suit] = str(int(tricks[0].split('/')[1])+6)
            else:
                east[suit] = str(int(tricks[0])+6)
                west[suit] = str(int(tricks[0])+6)
        else:
            raise ValueError(f'incorrect score detected on board {board}')

    return {'N': north, 'S': south, 'W': west, 'E': east}


if __name__ == '__main__': 
    ranges = input('Enter initial and final hand range as str (e.g. 1000001_1250000): ------')

    fname = '/content/drive/MyDrive/RL Bridge/data/BridgeComposer_'+ranges+'.txt'
    #fname = '/content/drive/MyDrive/RL Bridge/data/test256.txt'
    f = open(fname,"r+", encoding='latin')
    lines = f.readlines()
    n_boards = len(lines)//21

    hands = {}
    scores = {}
    for board in range(1, n_boards+1):
        hands[board] = get_hands(lines, board)
        scores[board] = get_scores(lines, board)


    with open('/content/drive/MyDrive/RL Bridge/data/Hands_'+ranges+'.json', "w") as fp:
        json.dump(hands , fp, indent=4)

    with open('/content/drive/MyDrive/RL Bridge/data/Scores_'+ranges+'.json', "w") as fp:
        json.dump(scores, fp, indent=4)
