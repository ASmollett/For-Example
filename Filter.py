import os
import csv
import math
import numpy as np
from tkinter import messagebox as mb

# Описываем функцию, где происходит оконная фильтрация
#  по правилу трёх сигм

def filterf(arrayres, window, count, error, back1, lab1, vid1):
    arrayres1 = np.zeros((count, 3))
    n = 0
    u = (window - 1) / 2
    for i in range(count - window - 1):
        ms1 = 0
        ms2 = 0
        for j in range(i, i + window):
            ms1 += arrayres[j][1]
            ms2 += arrayres[j][2]
        ms1 /= window
        ms2 /= window
        sko1 = 0
        sko2 = 0
        for j in range(i, i + window):
            sko1 += (arrayres[j][1] - ms1) ** 2
            sko2 += (arrayres[j][2] - ms2) ** 2
        sko1 = math.sqrt(sko1 / window) * 3
        sko2 = math.sqrt(sko2 / window) * 3
        lowframe1 = 0
        lowframe2 = 0
        lowframe1 = ms1 - sko1
        lowframe2 = ms2 - sko2
        highframe1 = ms1 + sko1
        highframe2 = ms2 + sko2
        if i == 0:
            for j in range(i, u):
                if ((lowframe1 <= arrayres[j][1]) and (arrayres[j][1] <= highframe1)) and ((lowframe2 <= arrayres[j][2]) and (arrayres[j][2] <= highframe2)):
                    arrayres1[n][0] = arrayres[j][0]
                    arrayres1[n][1] = arrayres[j][1]
                    arrayres1[n][2] = arrayres[j][2]
                    n += 1
                else:
                    back1 -= 1
                    lab1 -= 1
                    vid1 -= 1
        k = i + u
        if ((lowframe1 <= arrayres[k][1]) and (arrayres[k][1] <= highframe1)) and ((lowframe2 <= arrayres[k][2]) and (arrayres[k][2] <= highframe2)):
            arrayres1[n][0] = arrayres[k][0]
            arrayres1[n][1] = arrayres[k][1]
            arrayres1[n][2] = arrayres[k][2]
            n += 1
        elif k < back1:
            back1 -= 1
            lab1 -= 1
            vid1 -= 1
        elif k < lab1:
            lab1 -= 1
            vid1 -= 1
        else:
            vid1 -= 1
        if i == count - window - 1:
            for j in range(i + u + 1, count):
                if ((lowframe1 <= arrayres[j][1]) and (arrayres[j][1] <= highframe1)) and ((lowframe2 <= arrayres[j][2]) and (arrayres[j][2] <= highframe2)):
                    arrayres1[n][0] = arrayres[j][0]
                    arrayres1[n][1] = arrayres[j][1]
                    arrayres1[n][2] = arrayres[j][2]
                    n += 1
                else:
                    vid1 -= 1
    error += count - n
    for i in range(n, count):
        del arrayres1[i][0]
        del arrayres1[i][1]
        del arrayres1[i][2]
    return arrayres1, back1, lab1, vid1, error, n

# Проверяем наличие файла Result.csv и считываем 
#  из него данные в массив arrayres, рассчитываем метки нагрузок

path = "C:/Research/Results/"
path_list = os.listdir(path)
for file in path_list:
    if file == "Result.csv":
        checkres = 1
if checkres != 1: mb.showerror("Ошибка", "Отсутствует файл Result.csv")

results = []
count = 0
with open(path + "Result.csv") as result:
    readerres = csv.reader(result, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    readerres.pop(0)
    for row in readerres:
        results.append(row)
        count += 1

back = round(count / 6)
lab = back * 3
vid = back * 5
back1 = back
lab1 = lab
vid1 = vid

arrayres = np.zeros((count, 3))
j = 0
for row in results:
    arow = row.split(',')
    arrayres[j][0] = arow[0]
    arrayres[j][1] = arow[1]
    arrayres[j][2] = arow[2]
    j += 1

# Запускаем фильтрацию и считаем количество артефактов

error = 0
prevcount = count
for h in range (241, 1, -80):
    arrayres, back1, lab1, vid1, error, count = filterf(arrayres, h, count, error, back1, lab1, vid1)
proc = 100 * error / prevcount

if count <= vid:
    mb.showerror("Ошибка", "Было выявлено слишком много артефактов. Требуется повторная запись")

# Делаем перерасчёт меток нагрузок

back2 = round(count / 6)
lab2 = back * 3
vid2 = back * 5

back = round((back + back2) / 2)
lab = round((lab + lab2) / 2)
vid = round((vid + vid2) / 2)

# Записываем полученные данные в новые файлы ResultFiltered.csv и Markers.csv

with open(path+"ResultFiltered.csv", 'w') as resultf:
    writer = csv.writer(resultf)
    writer.writerow("Time", "LeftChannel", "RightChannel", "", "Arts= ", error, proc + "%")
    for i in range (count):
        writer.writerow(arrayres[i][0], arrayres[i][1], arrayres[i][2])

with open(path+"Markers.csv", 'w') as markers:
    writer = csv.writer(markers)
    writer.writerow("Мarkers by basic logic", 0, back1, lab1, vid1, count)
    writer.writerow("Мarkers by 1st algorithm", 0, back, lab, vid, count)
    writer.writerow("Мarkers by 2nd algorithm", 0, back2, lab2, vid2, count)

mb.showinfo("Программа Фильтр", "Фильтрация закончена и сохранена в папке \Результаты\ под соответствующим названием")
