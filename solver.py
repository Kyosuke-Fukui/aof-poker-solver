from findEquity import *
from generateTotalRange import *


def getUpdatedCallingRange(bb_range, sb_shoving_range, stack, res):
    total_combo = 0
    for jam in range(len(sb_shoving_range)):
        if sb_shoving_range[jam][3]:
            total_combo += sb_shoving_range[jam][2]

    for h in range(len(bb_range)):
        EV = 0
        for jam in range(len(sb_shoving_range)):
            combo = sb_shoving_range[jam][2]
            # SBのプッシュレンジ外のハンドをスキップ
            if not sb_shoving_range[jam][3]:
                continue
            equity = findEquity(bb_range[h], sb_shoving_range[jam], res)
            # EV計算
            EV += (combo / total_combo) * (equity*stack*2 - (stack - 2))

        # EVがプラスならコールすべき
        if bb_range[h][3]:
            # if EV < -1:
            if EV < 0:
                bb_range[h][3] = False
                bb_range[h][4] = 0
            else:
                bb_range[h][3] = True
                bb_range[h][4] = EV

    return bb_range


def getUpdatedJammingRange(sb_range, bb_calling_range, stack, res):
    total_combo = 0
    for call in range(len(bb_calling_range)):
        if bb_calling_range[call][3]:
            total_combo += bb_calling_range[call][2]

    for h in range(len(sb_range)):
        if sb_range[h][3]:
            EV = 0
            for call in range(len(bb_calling_range)):
                combo = bb_calling_range[call][2]
                if not bb_calling_range[call][3]:
                    # BBがフォールドするハンドの場合、必ずブラインドを得られる。
                    EV += 2 * (combo / total_combo)  # ビッグブラインドの額
                    continue
                equity = findEquity(sb_range[h], bb_calling_range[call], res)
                # EV計算
                EV += (combo / total_combo) * \
                    (equity*stack*2 - (stack - 1))

            # EVがプラスならプッシュすべき
            if EV < 0:  # SBの場合
                sb_range[h][3] = False
                sb_range[h][4] = 0
            else:
                sb_range[h][3] = True
                sb_range[h][4] = EV
    return sb_range


if __name__ == "__main__":
    stack = eval(input("Enter effective stack: "))
    iterations = 10  # 実行回数

    # 全169種類のハンドリストを作成（[card1, card2, combo, true/false]）
    bb_total = generateTotalRange()
    sb_total = generateTotalRange()

    # ハンドリストにEV入力欄を追加
    for n in range(len(bb_total)):
        bb_total[n].append(0)
        sb_total[n].append(0)

    # ハンドvsハンドの勝率データを参照
    file_path = 'C:/Users/owner/Downloads/exact.txt'
    with open(file_path) as f:
        lines = f.readlines()
    lines_strip = [line.strip() for line in lines]

    sb_range = sb_total[:]

    for i in range(iterations):
        print("Trial: " + str(i+1))

        # SBレンジ（初期値は全ハンド）とオッズが合うBBレンジを計算⇒そのBBレンジとオッズが合うSBレンジを計算⇒繰り返し
        bb_range = getUpdatedCallingRange(
            bb_total, sb_range, stack, lines_strip)
        sb_range = getUpdatedJammingRange(
            sb_total[:], bb_range, stack, lines_strip)

        # 戦略のEVを計算
        EV = 0
        total_combo = 0
        for h in range(len(bb_range)):
            total_combo += bb_range[h][2]
            EV += bb_range[h][2] * bb_range[h][4]
        EV = EV / total_combo
        print('EV of BB: ' + str('{:.3f}'.format(EV)))

        EV = 0
        total_combo = 0
        for h in range(len(sb_range)):
            total_combo += sb_range[h][2]
            EV += sb_range[h][2] * sb_range[h][4]
        EV = EV / total_combo
        print('EV of SB: ' + str('{:.3f}'.format(EV)))

        print("****************")
        print("Big Blind's calling range: ")

        for r in bb_range:
            if r[3]:
                if r[2] == 6:
                    hand = r[0] + r[1]
                if r[2] == 12:
                    hand = r[0] + r[1] + 'o'
                if r[2] == 4:
                    hand = r[0] + r[1] + 's'
                print(hand)

        print("****************")
        print("Small Blind's jamming range: ")

        for r in sb_range:
            if r[3]:
                if r[2] == 6:
                    hand = r[0] + r[1]
                if r[2] == 12:
                    hand = r[0] + r[1] + 'o'
                if r[2] == 4:
                    hand = r[0] + r[1] + 's'
                print(hand)
