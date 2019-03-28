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

# транскрипция
def F_transpon(word):
    cons = ['bh', 'dh', 'p', 'b', 't', 'k', 'g', 's', 'z', 'y', 'l', 'r', 'm', 'n', 'd']
    voc = ['i', 'e', 'ɛ', 'a', 'ɔ', 'o', 'u', 'ᴧ', 'ë', 'ɤ', 'ö', 'ɯ', 'ü']
    #print(word)
    for i in range(0, len(cons)):
        word = word.replace(cons[i], 'C')
    #print(word)

    for j in range(len(voc)):
        word = word.replace(voc[j], 'V')

    word = word.replace('=', '')
    word = word.replace("'", "")
    word = word.replace('-', '')
    word = word.replace('-', '')

    return word

# Основная функция
def M_phon(f_name):

    my_lines_1 = F_get_lines(f_name)
    my_lines = my_lines_1[1:]        # все слова: без первой строчки с названиями
    #my_lines = my_lines_1[16:25]  # РАБОЧАЯ ВЕРСИЯ ДЛЯ ВСЕХ СЛОВ
    my_lines_fin = my_lines_1[0]
    trans_12 = 'None'
    new_table = 'lex' + '\t' + 'Str' + '\t' + 'vowels'

    for line in my_lines:
        #print(line)
        new_line = str(line)
        line_split = new_line.split('\t')
        trans_1 = line_split[2]  # для данного слова есть его словарное вхождение
        trans_1 = trans_1.strip()
        #print(trans_1)

        for elem in trans_1:
            trans_12 = trans_1.replace("'", '')
            trans_12 = trans_12.replace("=", '')
            trans_12 = trans_12.replace("-", '')
            trans_12 = trans_12.replace("p", '')
            trans_12 = trans_12.replace("b", '')
            trans_12 = trans_12.replace("t", '')
            trans_12 = trans_12.replace("d", '')
            trans_12 = trans_12.replace("k", '')
            trans_12 = trans_12.replace("g", '')
            trans_12 = trans_12.replace("s", '')
            trans_12 = trans_12.replace("z", '')
            trans_12 = trans_12.replace("y", '')
            trans_12 = trans_12.replace("l", '')
            trans_12 = trans_12.replace("r", '')
            trans_12 = trans_12.replace("m", '')
            trans_12 = trans_12.replace("n", '')
            trans_12 = trans_12.replace("h", '')

        transpon = F_transpon(trans_1)
        #print('tr: ', transpon)

        new_table = new_table + '\n' + line_split[1] + '\t' + transpon + '\t' + trans_12

        #print(new_table)
        F_write_file_w(new_table, 'table_phon_v2.txt')


M_phon('table_lex.txt')

print("--- %s seconds ---" % (time.time() - start_time))
