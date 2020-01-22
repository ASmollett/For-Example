import os
import csv
from tkinter import messagebox as mb

# Параметр gencheck определяет при сборке,
#  в каких столбцах находятся необходимые данные

gencheck = 0
answer = mb.askyesno(title="Вопрос", message="С левой стороны записывали 1ый канал?")
if answer == True:
    gencheck+=1
answer = mb.askyesno(title="Вопрос", message="С правой стороны записывали 1ый канал?")
if answer == True:
    gencheck += 2
    
# Происходит проверка наличия файлов в рабочей папке
    
check = 0
check1 = 0
checklc = 0
checkrc = 0
path = "C:/Research/Raw/"
destpath = "C:/Research/Results/"
path_list = os.listdir(path)
for file in path_list:
    if file == "TimeLC.txt":
        check = 1
    if file == "TimeRC.txt":
        check1 = 1
    if file == "LC.csv":
        checklc = 1
    if file == "RC.csv":
        checkrc = 1
if check != 1:
    mb.showerror("Ошибка", "Отсутствует файл TimeLC.txt")
if check1 != 1:
    mb.showerror("Ошибка", "Отсутствует файл TimeRC.txt")
if checklc != 1:
    mb.showerror("Ошибка", "Отсутствует файл LC.csv")
if checkrc != 1:
    mb.showerror("Ошибка", "Отсутствует файл RC.csv")

# Из файлов TimeLC(-RC).txt получаем информацию
#  о времени запусков записи левого и правого канала
#  для выявления разницы и последующей синронизации при сборке

ptimelc = path + "TimeLC.txt"
ptimerc = path + "TimeRC.txt"

timelc = open(ptimelc)
timerc = open(ptimerc)

linelc = timelc.read()
linerc = timerc.read()

if linelc > linerc:
    dif = round((ord(linelc) - ord(linerc))*0.004)
    check1 = 1
else:
    dif = round((ord(linerc) - ord(linelc))*0.004)
    check1 = 2

timelc.close()
timerc.close()

os.rename(ptimelc, destpath+"TimeLC.txt")
os.rename(ptimerc, destpath+"TimeRC.txt")

# Открываем файлы с данными и запускаем синхронизированную перезапись
#  в новый файл Resul.csv

plc = path + "LC.csv"
prc = path + "RC.csv"

with open(plc) as lc, open(prc) as rc, open(path+"Result.csv", 'w') as result:
    writer = csv.writer(result)
    writer.writerow("Time", "LeftChannel", "RightChannel")
    readerlc = csv.reader(lc, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    readerrc = csv.reader(rc, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    if gencheck == 0:
        if check1 == 1:
            for row in readerlc:
                row1 = readerrc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow[8], arow1[8])
        if check1 == 2:
            for row in readerrc:
                row1 = readerlc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow1[8], arow[8])
    elif gencheck == 1:
        if check1 == 1:
            for row in readerlc:
                row1 = readerrc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow[4], arow1[8])
        if check1 == 2:
            for row in readerrc:
                row1 = readerlc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow1[4], arow[8])
    elif gencheck == 2:
        if check1 == 1:
            for row in readerlc:
                row1 = readerrc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow[8], arow1[4])
        if check1 == 2:
            for row in readerrc:
                row1 = readerlc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow1[8], arow[5])
    else:
        if check1 == 1:
            for row in readerlc:
                row1 = readerrc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow[4], arow1[4])
        if check1 == 2:
            for row in readerrc:
                row1 = readerlc[row+dif]
                arow = row.split(',')
                arow1 = row1.split(',')
                if arow1[0] == None:
                    break
                writer.writerow(arow[0], arow1[4], arow[4])
    

os.rename(plc, destpath+"LC.csv")
os.rename(prc, destpath+"RC.csv")
os.rename("/Result.csv", destpath+"Result.csv")

mb.showinfo("Программа Сборка", "Сборка успешно завершена")