import re
import time
start_time = time.time()

# чтение строк из файла, возвращает строки
def F_get_lines(f_name):
    f = open(f_name, 'r')
    my_lines = f.readlines()
    #print(my_lines)
    f.close()
    return my_lines

# чтение данных из файла, возвращает текст
def F_get_text(f_name):
    f = open(f_name, 'r')
    my_text = f.read()
    #print(my_lines)
    f.close()
    return my_text

# запись в файл
def F_write_file_w(data, f_name):
    f = open(f_name, 'w')
    f.write(data)
    #print(data)
    f.close()

# дозапись в файл
def F_write_file_a(data, f_name):
    f = open(f_name, 'a')
    f.write(data)
    #print(data)
    f.close()

# ФУНКЦИЯ ЗАМЕНЫ УДАРЕНИЯ В ОРФОГРАЯИИ
def F_russian_stress(word):
    a1 = ['а\\', 'о\\', 'у\\', 'э\\', 'е\\', 'и\\', 'ы\\', 'я\\', 'ё\\', 'ю\\']
    a2 = ['а́', 'о́', 'у́', 'э́', 'е́', 'и́', 'ы́', 'я́', 'ё', 'ю́']
    for i in range(0, len(a1)):
        if a1[i] in word:
            word = word.replace(a1[i], a2[i])

    return word

# функция должна решать проблемы с ошибками перевода орфографий
def F_old_new_orthography(word_old, word_new):
    res1 = re.search('m[^pbtdkgszylrmn]+ng', word_old)
    if res1:
        print(word_old)
        res12 = re.search('bh[^pbtdkgszylrmn]+nŋ', word_new)
        if res12:
            print('успех')
        else:
            print('нужно менять')
    #elif:
    #    res2 = re.search('m[^pbtdkgszylrmn]+')
    #    if


    w1 = str(word_old)
    w1 = w1.replace('^m', 'bh')
    w1 = w1.replace('^n', 'dh')

    a_new = []

# п 4.2, тоже про запись
def F_db_replaces(word):
    #  ̂ -> ̈,  -> ̂, dh̄n —> n̄
    a1 = ['̂', '', 'dh̄n']
    a2 = ['̈', '̂', 'n̄']
    for i in range(0, len(a1)):
        if a1[i] in word:
            word = word.replace(a1[i], a2[i])

    return word

# основная замена
def M_main(f_name): #18
    my_lines = F_get_lines(f_name)
    my_lines = my_lines[1:]             # РАБОЧАЯ ВЕРСИЯ ДЛЯ ВСЕХ СЛОВ
    #my_lines = my_lines[5:15]             # тестовая выборка
    #print(my_lines_i)
    my_lines_fin = my_lines[0]             # тестовая выборка

    for line in my_lines:
        my_line_m = F_russian_stress(line)
        my_line_f = F_db_replaces(my_line_m)
        my_lines_fin = my_lines_fin + my_line_f

    F_write_file_w(my_lines_fin, ('KS_' + f_name))


M_main('table_lex.txt')
M_main('table_ms.txt')


print("--- %s seconds ---" % (time.time() - start_time))
