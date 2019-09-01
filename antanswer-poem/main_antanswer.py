# -*- coding: utf-8 -*-
import statistics

from _anwfunction.analyze_antanswer import dpCompares, compare
from _anwfunction.read_antanswer import readAnw, readOpt, anwDetail

with open("anwOpt.json", 'r', encoding='utf-8-sig') as f:
    anwOpt = readOpt(f)
with open(anwOpt["ads_path"], 'r', encoding='utf-8-sig') as f:
    dMode = anwOpt["detail_mode"]
    DATA = readAnw(f)
    data_list = DATA.data_list
    DLen = len(data_list)
    if dMode == "opt":
        wil = anwOpt["basic_wil"]
        recent = anwOpt["basic_recent"]
        DATA = DATA._replace(anwDetail=anwDetail(wil=wil, recent=recent))
    elif dMode == "opt_rv":
        wil = anwOpt["basic_wil"]
        recent = int(DLen * anwOpt["basic_recentValue"])
        DATA = DATA._replace(anwDetail=anwDetail(wil=wil, recent=recent))
    elif dMode == "file":
        wil = DATA.anwDetail.wil
        recent = DATA.anwDetail.recent
        DATA = DATA._replace(anwDetail=anwDetail(wil=wil, recent=recent))
    else :
        quit()


n = DLen - 1
history = [None for i in range(recent)]

iMode = anwOpt["interface"].upper()
if iMode == "GUI":
    isCLI = False
    from _anwUi.gui_antanswer import *
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = anwUi(DATA)
    sys.exit(app.exec_())

elif iMode == "CLI":
    from random import randint
    from time import time
    from _anwfunction.analyze_antanswer import compare, dpCompares
    isCLI = True
    

else :
    quit()

if not isCLI:
    quit()
while True:
    score = 0
    aHistory = []
    dpHistory = []
    qHistory = []
    
    st = time()

    # core
    for i in range(wil):
        r = i #appended
        #r = randint(0, n)
        #while r in history[-recent:]:
            #r = randint(0, n)

        #history.append(r)
        answer, question = data_list[r][0], data_list[r][1][randint(0, len(data_list[r][1]) - 1)]

        print(question)
        a = input()
        if a in answer:
            score += 1
            print("\n" * 30)
            print("정답! : %d" % score)

        else :
            print("\n" * 30)
            print("틀림! : %d" % score)

        aHistory.append(a)
        dpHistory.append(answer)
        qHistory.append(question)
        a = None

    print("정답률 :" + str(score / wil))
    st = time() - st
    print(str(st) + "초걸림 |")
    print(str(st / wil) + "초/한문항당")
    result = dpCompares(aHistory, dpHistory)
    print("평균 정확도:", statistics.mean(result[0]))

    # display result
    if compare(input("결산을 보시고 싶다면 'result'를 입력"), "result") > 0.9:
        print("\n")
        print("단어 일치율 // 당신이 쓴 답 // 원래 답")
        for i in range(len(result[0])):
            print(round(result[0][i], 3), "//", result[1][i], "//", result[2][i])
    # repeat
    if compare(input("반복 하려면 repeat"), "repeat") > 0.9:
        continue
    else :
        break
