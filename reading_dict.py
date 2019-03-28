import re
import pymongo
import json
#delcom=re.compile("<!--.+-->", re.S) #зачем-то было в скрипте с пары

import ssl


# подключаюсь к MongoDB
def mongo(dictionary):
    client = pymongo.MongoClient('mongodb+srv://fedorenko:wassup23!@db2-2019-exam-tourf.mongodb.net/test?retryWrites=true',
                                 ssl=True,
                                 ssl_cert_reqs=ssl.CERT_NONE)
    db = client['exam']
    print(type(db))
    db.insert_one(dictionary[0])
    print(type(dictionary))

# структура json:
# {lexeme:
#   {head: {id: '123', head_f1: v1, ...},
#   {variants:
#       [
#       {variant: {f1: v1, ...}},
#       {...},
#       ]}
#   {meanings:
#       [
#       {meaning:
#           {head: {head_f1: v1, ...}},
#           {phrases:
#               [
#               {phrase: {f1: v1, ...},
#               ...},
#               ]
#       }
#       {...},
#       ]}
#   }

# 1 делю словарь на лексемы и нумерую их
# 2 считаю, как поля встречаются в шапке, а какие в значениях (в статьях с ms)
def main():
<<<<<<< HEAD
    dictFile = open('blowo12.txt', 'r', encoding='utf8')
    dictionary = [] # весь словарь
=======
    dictFile = open('KS_blowo12.txt', 'r', encoding='utf8') #ПРОВЕРЬ НАЗВАНИЕ ФАЙЛА
>>>>>>> 0a88ecab03061e87841123388c0e282cae134ddb
    lexemes = dictFile.read().split('\n\n') #разделяю на лексемы
    fieldList = {} #для списков полей из шапок и значений
    i = 0
    #нумерую лексемы и беру по одной с номером
    for id, lexeme in enumerate(lexemes[1:]): #удаляю нулевой элемент — строку с названием словаря
        lexeme = re.sub('\n(\w)', ' (\1)', lexeme)
        dictionary.append(readLexeme(lexeme, id)) #отправляю слов. статью на чтение вместе с id
        # делаю список полей из шапок
        if '\n\ms ' in lexeme:
            for field in getFields(lexeme)[0]:
                if field not in fieldList:
                    fieldList[field] = [1, 0]
                else:
                    fieldList[field][0] += 1
            for field in getFields(lexeme)[1]:
                if field not in fieldList:
                    fieldList[field] = [0, 1]
                else:
                    fieldList[field][1] += 1
    dictFile.close()
    mongo(dictionary)

# создаю словарь для шапки, добавляю туда id, глоссы и дату,
# остальные поля складываю в один массив
def readLexeme(lexeme, id):
    inLex = {} #словарь для общелексемных полей
    inLex['id'] = str(id) #добавляю id в словарь шапки
    article = [] #словарь для всех полей статьи
    # читаю статью по строкам
    for line in lexeme.split('\n'):
        divBySpaces = line.split(' ')
        name = divBySpaces[0] #отделяю имя поля
        content = ' '.join(divBySpaces[1:]) # и содержимое
        # дату и глоссы записываю сразу в словарь для шапки
        if name == '\dt' or name.startswith('\g'):
            inLex[name] = content
        # остальное складываю в массив
        else:
            article.append([name, content])
    return divideByMS(inLex, article)

# пилю статью на шапку и значения (по полям \ms, либо по первому \df(e|f|r) )
# ! TODO: посмотреть случаи \df до \ms
def divideByMS(inLex, article):
    meanings = []
    lexFields = []
    msAttested = False # становится верна, если встретилось \ms
    dfAttestedBeforeMs = False # становится верна, если встретилось \df до \ms
    for num, name_content in enumerate(article):
        if msAttested == False and dfAttestedBeforeMs == False:
            # Как только встретилось \df, отрезаю шапку, остальное отправляю в значения
            # но буду проверять (см. след. цикл), не встретилось ли после него \ms (тогда выдам ошибку)
            if name_content[0].startswith('\\df'):
                lexFields = article[0:num]
                meaning = [['\\ms', '0']]
                meaning.extend(article[num:])
                meanings.append(meaning)
                dfAttestedBeforeMs = True
        if name_content[0] == '\\ms':
            # если уже был \df, то это ошибка (просто печатаю статью)
            # if dfAttestedBeforeMs == True:
                #print(article) #! todo: посмотреть ошибки
            # если \df раньше не было, то
            if dfAttestedBeforeMs == False:
                # если это первый \ms, то отрезаю шапку и записываю номер строки с первым \ms
                if msAttested == False:
                    lexFields = article[0:num]
                    lastMS = num
                    msAttested = True
                    continue
                # если \ms уже был, то записываю предыдущий \ms и меняю номер последней строки с \ms
                elif msAttested == True:
                    meanings.append(article[lastMS:num])
                    lastMS = num
                    continue
    # если встречались \ms, то записываю последнее значение
    if msAttested == True:
        meanings.append(article[lastMS:num])
    lexeme = {}
    if lexFields == []:
        lexFields = article
    head_vars = analyseLexFields(inLex, lexFields)
    lexeme['head'] = head_vars[0]
    lexeme['variants'] = head_vars[1]
    if meanings != []:
        lexeme['meanings'] = analyseMeanings(inLex['id'], meanings)
    return lexeme

# беру поля из шапки, отрезаю от них алломорфы и варианты (и всё, что ниже) и отправляю печатать в таблицу с шапками
def analyseLexFields(inLex, lexFields):
    variants = []
    head = {}
    for num, name_content in enumerate(lexFields):
        if name_content[0] in ['\\al', '\\ald']:
            variant = {}
            type = name_content[0]
            variant['id_lex'] = inLex['id']
            variant['type'] = type
            variant['trans'] = name_content[1]
            if lexFields[num+1][0] == type+'or':
                variant['ortho'] = lexFields[num + 1][1]
                del lexFields[num + 1]
                if lexFields[num + 2][0] == '\\ph':
                    variant['\\ph'] = lexFields[num + 2][1]
                    del lexFields[num + 2]
                    if lexFields[num + 3][0] == '\\src':
                        variant['\\src'] = lexFields[num + 3][1]
                        del lexFields[num + 3]
                elif lexFields[num + 2][0] == '\\src':
                    variant['\\src'] = lexFields[num + 2][1]
                    del lexFields[num + 2]
            write(variant, 'var')
            variants.append(variant)
        else:
            inLex[name_content[0]] = name_content[1]
    write(inLex, 'lex')
    return [inLex, variants]

# беру значение, пишу его шапку и отправляю фразы (идиомы, \cbn, примеры) в следующую функцию
def analyseMeanings(id, meanings):
    meanings = []
    for meaning in meanings:
        meaning = {}
        head = {}
        phrases = []
        head['id_lex'] = id
        head['\\ms'] = meaning[0][1]
        for num, name_content in enumerate(meaning):
            if name_content[0] in ['\\idi', '\\cbn', '\\ex']:
                phrase = {}
                type = name_content[0]
                phrase['id_ms'] = id+'_'+head['\\ms']
                phrase['type'] = type
                phrase['trans'] = name_content[1]
                if len(meaning) < num +2:
                    continue
                if meaning[num + 1][0] == type + 'or':
                    phrase['ortho'] = meaning[num + 1][1]
                    del meaning[num + 1]
                    if len(meaning) < num + 3:
                        continue
                    if meaning[num + 2][0] == ('\\src'):
                        phrase['\\src'] = meaning[num + 2][1]
                        del meaning[num + 2]
                        if meaning[num + 3][0].startswith('\\tr'):
                            phrase[meaning[num + 3][0]] = meaning[num + 3][1]
                            del meaning[num + 3]
                            if len(meaning) < num + 5:
                                continue
                            if meaning[num + 4][0].startswith('\\tr'):
                                phrase[meaning[num + 4][0]] = meaning[num + 4][1]
                                del meaning[num + 4]
                                if meaning[num + 5][0].startswith('\\tr'):
                                    phrase[meaning[num + 5][0]] = meaning[num + 5][1]
                                    del meaning[num + 5]
                write(phrase, 'ph')
                phrases.append({'phrase': phrase})
            else:
                head[name_content[0]] = name_content[1]
        write(head, 'ms')
        meaning['head'] = head
        meaning['phrases'] = phrases
        meanings.append({'meaning': meaning})
    return meanings

# беру id значения, фразу
def analysePhrase(id_ms, phraseLines):
    phrase = {}
    phrase['id_ms'] = id_ms
    phrase['type'] = phraseLines[0][0]
    if phraseLines[1][0] == phraseLines[0][0]+'or':
        phraseLines[0][0] = 'trans'
        phraseLines[1][0] = 'ortho'
    for name, content in phraseLines[1:]:
        phrase[name] = content
    write(phrase, 'ph')
    return phrase

# функция для разделения статьи (или ее части) на шапку и блоки (по начальным полям блоков)
def divideBy(lines, dividers):
    nonHeadParts = []
    divAttested = False
    for num, name_content in enumerate(lines):
        if name_content[0] in dividers:
            # если разделитель уже был, то записываю предыдущий разделитель и меняю номер последней строки с разделителем
            if divAttested == True:
                nonHeadParts.append(lines[lastDiv:num])
                lastDiv = num
                continue
            # если это первый разделитель, то отрезаю шапку и записываю номер строки с первым разделитель
            if divAttested == False:
                head = lines[0:num]
                lastDiv = num
                msAttested = True
                continue
    if divAttested == True:
        nonHeadParts.append(article[lastDiv:num])
    else:
        head = lines
    return [head, nonHeadParts]

# беру словарь с полями и записываю его в таблицу
def write(fields, domain):
    tableFile = open('table_'+domain+'.txt', 'a', encoding='utf8')
    toWrite = []
    for i in range(len(fieldList(domain))):
        toWrite.append('')
    for field in fields:
        if field not in fieldList(domain):
            continue
        toWrite[column(field, domain)] = fields[field]
    tableFile.write('\t'.join(toWrite)+'\n')
    tableFile.close()

# беру название поля и таблицы, возвращаю номер столбца для этого поля для этой таблицы
def column(field, domain):
    fNames = fieldList(domain)
    i = 0
    name_num = {}
    for fName in fNames:
        name_num[fName] = i
        i += 1
    return name_num[field]

# беру название домена и возвращаю массив с названиями полей
def fieldList(domain):
    if domain == 'lex':
        return ['id', '\\le', '\\leor', '\\ph', '\\u', '\\voc', '\\voir', '\\key', '\\src', '\\ps', '\\psr', '\\pf', '\\pfr', '\\pff', '\\dt', '\\ge', '\\gf', '\\gr', '\\egr', '\\ege', '\\egf']
    if domain == 'ms':
        return ['id_lex', '\\ms', '\\dfr', '\\smr', '\\dfe', '\\sme', '\\dff', '\\smf', '\\sn', '\\src', '\\syn', '\\synor', '\\ant', '\\antor']
    if domain == 'ph':
        return ['id_ms', 'type', 'trans', 'ortho', '\\trr', '\\smr', '\\tre', '\\sme', '\\trf', '\\smf', '\\src']
    if domain == 'var':
        return ['id_lex', 'type', 'trans', 'ortho', '\\ph', '\\src']

# для подсчета полей в шапках и в значениях
def getFields(lexeme):
    commonFields = []
    msFields = []
    divByMs = lexeme.split('\n\ms ')
    commonLines = divByMs[0]
    msLines = '\n\ms '.join(divByMs[1:len(divByMs)-1])
    for line in commonLines.split('\n'):
        commonFields.append(line.split(' ')[0])
    for line in msLines.split('\n'):
        msFields.append(line.split(' ')[0])
    return [commonFields, msFields]

# создаю файлы для таблиц
def createFiles(domains):
    for domain in domains:
        lexFile = open('table_'+domain+'.txt', 'w', encoding='utf8')
        lexFile.write('\t'.join(fieldList(domain))+'\n')
        lexFile.close()

if __name__ == '__main__':
    createFiles(['lex', 'ms', 'ph', 'var'])
    main()
