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

#word = '' # ПОДСТАВЬ НУЖНОЕ
#word = F_russian_stress(word)
#print(word)

def F_old_new_orthography(word_old, word_new):
    res1 = re.search('m.+ng', word_old)
    if res1:
        print(word_old)
        res12 = re.search('bh.+nŋ', word_new)
        if res12:
            print('успех')
        else:
            print('нужно менять')

    w1 = str(word_old)
    w1 = w1.replace('^m', 'bh')
    w1 = w1.replace('^n', 'dh')

    a_new = []

F_old_new_orthography('mëng', 'bhʌ̄ŋ')

#\le bhīn
#\leor mi

print("--- %s seconds ---" % (time.time() - start_time))
