import os,glob
import xlwt
import re
from Global import (TF_IDF, tf_idf, bigram, bi_tf_idf)
from tqdm import tqdm
from time import monotonic
from datetime import timedelta
papka_korpus = os.path.dirname(os.path.abspath(__file__))
papka_train = os.path.join(papka_korpus, "testtrain")
papka_outtexts = os.path.join(papka_korpus, "testouttexts")
print("Keywords to excell processing...")
#TF_IDF jaily aqparat
#print(TF_IDF.__doc__)
#-------------------------------------------------------------------------------------------------

def sozgebolu(text):
    tag = re.findall(r'[<]+\w+[>]+', text)
    sozder = re.split(r'[<]+\w+[>]+', text)
    for i in range(len(sozder)):
        sozder[i] = str(sozder[i]).lower()
        new = ""
        for j in sozder[i]:
            if j in "abcdefghigklmnopqrstuvwxyzаәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщьыъіэюя1234567890":
                new += j
        sozder[i] = new
    if sozder[len(sozder)-1] == '':
        del sozder[len(sozder)-1]
    return [sozder, tag]
#----------------------------------------------------------------------------------------------------

#excelge daindyq
wb = xlwt.Workbook()
xlwt.add_palette_colour("kerek", 0x21)
wb.set_colour_RGB(0x21, 204, 255, 255)
style0 = xlwt.easyxf("pattern: pattern solid, fore_color Lime; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman, bold on; align: horiz center;")
style1 = xlwt.easyxf("pattern: pattern solid, fore_color kerek; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman; ")
style2 = xlwt.easyxf("pattern: pattern solid, fore_color yellow; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman;")
style3 = xlwt.easyxf("pattern: pattern solid, fore_color red; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman;")

#stopwordtar
f = open(os.path.join(papka_korpus,"Global/MorfAnaliz/stopw.txt"), 'r', encoding="utf-8")
stxt = list(f.readlines())
for i in range(len(stxt)):
    l = "" 
    for j in range(len(stxt[i])):
        if stxt[i][j] != '\n':
            l += stxt[i][j]
    stxt[i] = l

#textter
files = glob.glob(os.path.join(papka_outtexts, "*.gt"))
length = len(files)
pbar = tqdm(files)
start_time = monotonic()
for fail in pbar:
    filename = fail[fail.rfind("/")+1:]
    pbar.set_description(f"Жасалуда {str(filename)}")
    with open(fail, 'r', encoding="utf-8") as f:
        inddot = filename.rfind(".")
        txt = f.read()

        #failda berilgen matinnen tek sozderdi wygaryp beredi
        soz = sozgebolu(txt)

        #stopwordtard alyp tastau
        n = len(soz[0])
        i = 0
        while i < n:
            for j in stxt:
                if soz[0][i] == j:
                    soz[0].remove(j)
                    del soz[1][i]
                    n -= 1
                    i -= 1
                    break
            i += 1

        #TF_IDF klasssyndagy konstruktordy qoldanyluy
        TfIdf = tf_idf(text = soz, papka_train = papka_train)

        #esepteuler
        tf = TfIdf.tf_esepteu()
        idf = TfIdf.idf_esepteu()
        tfidf = TfIdf.tf_idf_esepteu()

        #bigram klasssyndagy konstruktordy qoldanyluy
        bi = bigram(text = txt, papka_korpus = papka_korpus)
        text = [bi.newlemm, bi.lastlemm]

        #bigram TF_IDF klasssyndagy konstruktordy qoldanyluy
        BiTfIdf = bi_tf_idf(text = text, papka_train = papka_train)

        bi_tf = BiTfIdf.bi_tf_esepteu()
        bi_idf = BiTfIdf.bi_idf_esepteu()
        bi_tfidf = BiTfIdf.bi_tf_idf_esepteu()

        ws = wb.add_sheet(filename[:inddot], cell_overwrite_ok = True)
        ws.write_merge(0, 0, 0, 1, "TF", style0)
        ws.write_merge(0, 0, 2, 3, "IDF", style0)
        ws.write_merge(0, 0, 4, 5, "TF-IDF",style0)

        i = 1
        j = 0
        ws.col(j).width = 5300
        ws.col(j+1).width = 5300
        for x in tf:
            if i < 16:
                ws.write(i, j, str(x), style1)
                ws.write(i, j+1, str(tf[x]), style1)
            else:
                break
            i += 1
        nexti = 1
        for x in bi_tf:
            if nexti < 16:
                ws.write(i, j, str(x), style1)
                ws.write(i, j+1, str(bi_tf[x]), style1)
            else:
                break
            i += 1
            nexti += 1
        i = 1
        j = 2
        ws.col(j).width = 5300
        ws.col(j+1).width = 5300
        for x in idf:
            if i < 16:
                ws.write(i, j, str(x), style1)
                ws.write(i, j+1, str(idf[x]), style1)
            else:
                break
            i += 1
        nexti = 1
        for x in bi_idf:
            if nexti < 16:
                ws.write(i, j, str(x), style1)
                ws.write(i, j+1, str(bi_idf[x]), style1)
            else:
                break
            i += 1
            nexti += 1
        i = 1
        j = 4
        ws.col(j).width = 5300
        ws.col(j+1).width = 5300
        for x in tfidf:
            if i < 16:
                ws.write(i, j, str(x), style1)
                ws.write(i, j+1, str(tfidf[x]), style1)
            else:
                break
            i += 1
        nexti = 1
        for x in bi_tfidf:
            if nexti < 16:
                ws.write(i, j, str(x), style1)
                ws.write(i, j+1, str(bi_tfidf[x]), style1)
            else:
                break
            i += 1
            nexti += 1
wb.save(os.path.join(papka_korpus, "keywords.xls"))
end_time = monotonic()
timedel = end_time - start_time 

print("Аяқталды! Барлығы {0} құжат. Жұмсалған уақыт: {1}".format(length, timedelta(seconds=timedel)))
