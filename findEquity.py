
def findEquity(hand1, hand2, res):
    if hand1[2] == 6:
        txt1 = hand1[0] + hand1[1]
    if hand1[2] == 12:
        txt1 = hand1[0] + hand1[1] + 'o'
    if hand1[2] == 4:
        txt1 = hand1[0] + hand1[1] + 's'
    if hand2[2] == 6:
        txt2 = hand2[0] + hand2[1]
    if hand2[2] == 12:
        txt2 = hand2[0] + hand2[1] + 'o'
    if hand2[2] == 4:
        txt2 = hand2[0] + hand2[1] + 's'

    txt = txt1 + ' vs. ' + txt2 + ':'  # 検索文字列
    hands = [line for line in res if txt in line]
    if hands:
        win_case = res[res.index(hands[0]) + 1].split(' ')
        tie_case = res[res.index(hands[0]) + 3].split(' ')
        # print(win_case)
        # print(tie_case)
        eq = float(win_case[win_case.index('=')+1])
        tie = float(tie_case[tie_case.index('=')+1])
        totalEq = eq + 0.5*tie
        # print(totalEq)
    else:
        txt = txt2 + ' vs. ' + txt1 + ':'

        hands = [line for line in res if txt in line]
        win_case = res[res.index(hands[0]) + 2].split(' ')
        tie_case = res[res.index(hands[0]) + 3].split(' ')
        # print(win_case)
        # print(tie_case)
        eq = float(win_case[win_case.index('=')+1])
        tie = float(tie_case[tie_case.index('=')+1])
        totalEq = eq + 0.5*tie
        # print(totalEq)
    return totalEq
