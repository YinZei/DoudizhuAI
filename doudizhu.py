import random
from itertools import combinations
import numpy as np

experiment_control = False
process_sum = 0

def initial_state():
    if experiment_control:
        user_type = [2, 1, 1]
    else:
        user_type = [0, 0, 0]
        for i in range(3):
            while True:
                str1 = input('please select user' + str(i) + ' type: (0)human, (1)baseline AI, (2)tree-based AI:')
                if str1 != '0' and str1 != '1' and str1 != '2':
                    print('invalid input, try again')
                    continue
                else:
                    user_type[i] = int(str1)
                    break
                
    dizhu = random.randint(0, 2)
    
    #J->11, Q->12, K->13, A->14, 2->15, black joker->16, red joker->17
    cards = list(range(3, 16)) * 4
    cards.append(16)
    cards.append(17)
    
    orders = list(range(54))
    random.shuffle(orders)
    
    dizhu_cards = [cards[i] for i in orders[0:20]]
    dizhu_cards.sort()
    cards1 = [cards[i] for i in orders[20:37]]
    cards1.sort()
    cards2 = [cards[i] for i in orders[37:54]]
    cards2.sort()
    
    players_cards = [[], [], []]
    players = [0, 1, 2]
    
    players_cards[dizhu] = dizhu_cards
    players.remove(dizhu)
    players_cards[players[0]] = cards1
    players_cards[players[1]] = cards2
    
    #0state->player0 cards, 1player1 cards, 2player2 cards, 3player0 type, 4player1 type, 5player2 type, 6dizhu player, 7player's turn, 8cards on the desk, 9the last player
    return (tuple(players_cards[0]), tuple(players_cards[1]), tuple(players_cards[2]), user_type[0], user_type[1], user_type[2], dizhu, dizhu, (), dizhu)
    
def matchX(cards):
    return [(i,) for i in set(cards)]
    
def matchXX(cards):
    result = []
    
    if len(cards) < 2:
        return result
        
    for i in range(len(cards) - 1):
        if cards[i] == cards[i + 1]:
            result.append((cards[i], cards[i]))
            
    return sorted(list(set(result)))
    
def matchXXX(cards):
    result = []
    
    if len(cards) < 3:
        return result
        
    for i in range(len(cards) - 2):
        if cards[i] == cards[i + 1] and cards[i + 2] == cards[i + 1]:
            result.append((cards[i], cards[i], cards[i]))
            
    return sorted(list(set(result)))
    
def matchXXXX(cards):
    result = []
    
    if len(cards) < 4:
        return result
        
    for i in range(len(cards) - 3):
        if cards[i] == cards[i + 1] and cards[i + 2] == cards[i + 1] and cards[i + 2] == cards[i + 3]:
            result.append((cards[i], cards[i], cards[i], cards[i]))
            
    return result
    
def matchRedBlack(cards):
    result = []
        
    if len(cards) >= 2 and cards[-1] == 17 and cards[-2] == 16:
        result.append((16, 17))
        
    return result
    
def matchXs(single_list):
    if len(single_list) < 5:
        return []
        
    tmp = []
    i = 1
    count = 1
    while i < len(single_list):
        if single_list[i][0] > 14:
            break
        if single_list[i - 1][0] + 1 == single_list[i][0]:
            count += 1
        else:
            if count >= 5:
                tmp.append(tuple(numt[0] for numt in single_list[i - count : i]))
            count = 1
            
        i += 1
        
    if count >= 5:
        tmp.append(tuple(numt[0] for numt in single_list[i - count : i]))
    
    result = []
    for cards in tmp:
         for i in range(0, len(cards) - 4):
             for j in range(i + 5, len(cards) + 1):
                 result.append(cards[i:j])
    return result
    
def matchXXXs(triple_list):
    if len(triple_list) < 2:
        return []
        
    tmp = []
    i = 1
    count = 1
    while i < len(triple_list):
        if triple_list[i][0] > 14:
            break
        if triple_list[i - 1][0] + 1 == triple_list[i][0]:
            count += 1
        else:
            if count >= 2:
                tmp.append(tuple(numt[0] for numt in triple_list[i - count : i]))
            count = 1
            
        i += 1
        
    if count >= 2:
        tmp.append(tuple(numt[0] for numt in triple_list[i - count : i]))
    
    result = []
    for cards in tmp:
         for i in range(0, len(cards) - 1):
             for j in range(i + 2, len(cards) + 1):
                 result.append(tuple(x for x in cards[i:j] for y in range(3)))
    return result
    
def matchXXs(double_list):
    if len(double_list) < 3:
        return []
        
    tmp = []
    i = 1
    count = 1
    while i < len(double_list):
        if double_list[i][0] > 14:
            break
        if double_list[i - 1][0] + 1 == double_list[i][0]:
            count += 1
        else:
            if count >= 3:
                tmp.append(tuple(numt[0] for numt in double_list[i - count : i]))
            count = 1
            
        i += 1
        
    if count >= 3:
        tmp.append(tuple(numt[0] for numt in double_list[i - count : i]))
    
    result = []
    for cards in tmp:
         for i in range(0, len(cards) - 2):
             for j in range(i + 3, len(cards) + 1):
                 result.append(tuple(x for x in cards[i:j] for y in range(2)))
    return result
    
def matchXXXY(triple_list, cards):
    return [(t[0], t[1], t[2], s) for t in triple_list for s in set(cards) if t[0] != s]
    
def matchXXXsYs(triples_list, cards):
    return [tuple(list(t) + list(s)) for t in triples_list for s in combinations(cards, len(t) // 3) if len(t) > 3 and (set(t) & set(s)) == set()]

def matchXXXXYZ(quad_list, cards):
    return [tuple(list(q) + list(s)) for q in quad_list for s in combinations(cards, 2) if q[0] not in s]


def valid_actions(state):
    cards = state[state[7]]
    desk = state[8]
    if state[7] == state[9]:
        single = matchX(cards)
        dul = matchXX(cards)
        triple = matchXXX(cards)
        quad = matchXXXX(cards)
        
        return single + dul + triple + quad + matchRedBlack(cards) + matchXs(single) + matchXXXs(triple) + matchXXs(dul) + matchXXXY(triple, cards) +  matchXXXsYs(triple, cards) + matchXXXXYZ(quad, cards)
    else:
        if len(desk) == 1:
            return [i for i in matchX(cards) if i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif len(desk) == 2 and desk[0] == desk[1]:
            return [i for i in matchXX(cards) if i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif len(desk) == 3 and desk[0] == desk[1] and desk[1] == desk[2]:
            return [i for i in matchXXX(cards) if i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif len(desk) == 4 and desk[0] == desk[1] and desk[1] == desk[2] and desk[2] == desk[3]:
            return [i for i in matchXXXX(cards) if i[0] > desk[0]] + matchRedBlack(cards) + [()]
        elif len(desk) == 2 and desk[0] == 16 and desk[1] == 17:
            return [()]
        elif desk[1] == desk[0] + 1:
            return [i for i in matchXs(matchX(cards)) if len(desk) == len(i) and i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif len(desk) == 4 and desk[0] == desk[1] and desk[1] == desk[2] and desk[2] != desk[3]:
            return [i for i in matchXXXY(matchXXX(cards), cards) if i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif desk[0] == desk[1] and desk[2] == desk[1] + 1:
            return [i for i in matchXXs(matchXX(cards)) if len(desk) == len(i) and i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif desk[0] == desk[1] and desk[1] == desk[2] and desk[2] + 1 == desk[3] and desk[-1] == desk[-2] and desk[-2] == desk[-3] and desk[-4] + 1 == desk[-3]:
            return [i for i in matchXXXs(matchXXX(cards)) if len(desk) == len(i) and i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        elif len(desk) == 6 and desk[0] == desk[1] and desk[1] == desk[2] and desk[2] == desk[3]:
            return [i for i in matchXXXXYZ(matchXXXX(cards), cards) if i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]
        else:
            return [i for i in matchXXXsYs(matchXXX(cards), cards) if len(desk) == len(i) and i[0] > desk[0]] + matchXXXX(cards) + matchRedBlack(cards) + [()]

def perform_action(state, action):
    state = list(state)
    cards = list(state[state[7]])
    for i in action:
        cards.remove(i)
    state[state[7]] = tuple(cards)
    
    if action != ():
        state[8] = action
        state[9] = state[7]
    
    state[7] = (state[7] + 1) % 3
    
    return tuple(state)
    
def game_over(state):
    return len(state[0]) == 0 or len(state[1]) == 0 or len(state[2]) == 0 
    
def evaluate(state):
    if len(state[state[6]]) <= (len(state[(state[6] + 1) % 3]) + len(state[(state[6] + 1) % 3])) // 2:
        return 2
    else:
        return 1
    
def score_in(state):
    if len(state[state[6]]) == 0:
        return 3
    else:
        return 0
    


def minimax(state, max_depth):
    global process_sum
    process_sum = process_sum + 1
    if game_over(state): return None, score_in(state)
    if max_depth == 0: return None, evaluate(state)

    children = [perform_action(state, action) for action in valid_actions(state)]
    results = [minimax(child, max_depth-1) for child in children]

    
    _, utilities = zip(*results)
    if state[6] == state[7]: action = np.argmax(utilities)
    if state[6] != state[7]: action = np.argmin(utilities)
    return children[action], utilities[action]

def play():
    max_depth = 9
    state = initial_state()
    while not game_over(state):
        print('player0 cards:', end = ' ')
        for i in state[0]:
            print(i, end = ' ')
        print('')
        
        print('player1 cards:', end = ' ')
        for i in state[1]:
            print(i, end = ' ')
        print('')
        
        print('player2 cards:', end = ' ')
        for i in state[2]:
            print(i, end = ' ')
        print('')
        
        print("player" + str(state[6]) + " is Dizhu")
        print("it is player" + str(state[7]) + "'s turn")
        print("cards on the desk:", end = ' ')
        for i in state[8]:
            print(i, end = ' ')
        print(", player" + str(state[9]))
        
        
        type = state[state[7] + 3]
        if type == 0:
            actions = valid_actions(state)
            print("valid actions:", actions)
            control = True
            while control:
                inputs = input("please input cards(seperated by spaces): ")
                res = inputs.split()
                action1 = sorted([int(s) for s in res])
                for action in actions:
                    if action1 == sorted(action):
                        state = perform_action(state, action)
                        control = False
                        break
                        
                if control:
                     print("invalid inputs")
                    

        elif type == 1:
            actions = valid_actions(state)
            action = random.choice(actions)
            state = perform_action(state, action)
            print("AI action:", end = ' ')
            for i in action:
                print(i, end = ' ')
            print('')
            if not experiment_control:
                input()
        else:
            state, _ = minimax(state, max_depth)
            print("AI action:", end = ' ')
            if state[7] == (state[9]) + 1 % 3:
                for i in state[8]:
                    print(i, end = ' ')
                print('')
            else:
                print("pass")
            if not experiment_control:
                input()
            
    players = [0, 1, 2]
    scores = [0, 0, 0]
    if state[9] == state[6]:
        scores[state[6]] = 1
    else:
        players.remove(state[6])
        for i in players:
            scores[i] = 1
            
    print("scores are:", scores)
    return scores
    
if __name__ == "__main__":
      play()
