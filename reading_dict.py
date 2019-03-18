import re

# * делю словарь на лексемы и нумерую их
# * считаю, как поля встречаются в шапке, а какие в значениях (в статьях с ms)
def main():
    dictFile = open('blowo12.txt', 'r', encoding='utf8')
    lexemes = dictFile.read().split('\n\n') #разделяю на лексемы
    del lexemes[0] #удаляю нулевой элемент — строку с названием словаря
    fieldList = {} #для списков полей из шапок и значений
    i = 0
    #нумерую лексемы и беру по одной с номером
    for id, lexeme in enumerate(lexemes, 1):
        lexeme.replace('\n(\w)', ' (\1)')
        readLexeme(lexeme, id) #отправляю слов. статью на чтение вместе с id
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
    divideByMS(inLex, article)

# пилю статью на шапку и значения (по полям \ms, либо по первому \df(e|f|r) )
# ! посмотреть случаи \df до \ms
def divideByMS(inLex, article):
    meanings = []
    lexFields = []
    msAttested = False # становится верна, если встретилось \ms
    dfAttestedBeforeMs = False # становится верна, если встретилось \df до \ms
    for num, name_content in enumerate(article):
        if msAttested == False:
            # Как только встретилось \df, отрезаю шапку, остальное отправляю в значения
            # но буду проверять (см. след. цикл), не встретилось ли после него \ms (тогда выдам ошибку)
            if name_content[0].startswith('\df'):
                lexFields = article[0:num]
                meanings.append(article[num:])
                dfAttestedBeforeMs = True
        if name_content[0] == '\ms':
            # если уже был \df, то это ошибка (просто печатаю статью)
            if dfAttestedBeforeMs == True:
                print()#(article) #! todo: посмотреть ошибки
            # если \df раньше не было, то
            else:
                # если это первый \ms, то отрезаю шапку и записываю номер строки с первым \ms
                if msAttested == False:
                    lexFields = article[0:num]
                    lastMS = num
                    msAttested = True
                # если \ms уже был, то записываю предыдущий \ms и меняю номер последней строки с \ms
                if msAttested == True:
                    meanings.append(article[lastMS:num])
                    lastMS = num
    # если встречались \ms, то записываю последнее значение
    if msAttested == True:
        meanings.append(article[lastMS:num])
    if lexFields == []:
        lexFields = article
    analyseLexFields(inLex, lexFields)
    #analyseMeanings(inLex['id'], meanings)

def analyseLexFields(inLex, lexFields):
    divideBy(lexFields, ['\al', '\ald', '\var'])
    write(inLex, 'lex')

def divideBy(lines, dividers):
    nonHeadParts = []
    divAttested = False
    for num, name_content in enumerate(lines):
        if name_content[0] in dividers:
            # если это первый разделитель, то отрезаю шапку и записываю номер строки с первым разделитель
            if divAttested == False:
                head = lines[0:num]
                lastDiv = num
                msAttested = True
            # если разделитель уже был, то записываю предыдущий разделитель и меняю номер последней строки с разделителем
            if msAttested == True:
                nonHeadParts.append(lines[lastDiv:num])
                lastDiv = num
    if divAttested == True:
        nonHeadParts.append(article[lastDiv:num])
    else:
        head = lines
    return [head, nonHeadParts]

#беру словарь с полями и записываю его в таблицу
def write(fields, table):
    tableFile = open(table+'.txt', 'a', encoding='utf8')
    toWrite = []
    for field in fields:
        toWrite.insert(column(field, table), fields[field])
    tableFile.write('\t'.join(toWrite)+'\n')
    tableFile.close()

def column(field, table):
    if table == 'lex':
        fNames = listOfLexFields()
    i = 0
    name_num = {}
    for fName in fNames:
        name_num[fName] = i
        i += 1
    return name_num[field]

def listOfLexFields():
    return ['id', '\\le', '\\leor', '\\ph', '\\u', '\\voc', '\\voir', '\\key', '\\src', '\\ps', '\\psr', '\\pf', '\\pfr', '\\pff', '\\dt', '\\ge', '\\gf', '\\gr']

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

def createFiles():
    lexFile = open('lex.txt', 'w', encoding='utf8')
    lexFile.write('\t'.join(listOfLexFields())+'\n')
    lexFile.close()

if __name__ == '__main__':
    createFiles()
    main()