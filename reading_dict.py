def main():
    dictFile = open('blowo12.txt', 'r', encoding='utf8')
    lexemes = dictFile.read().split('\n\n') #разделяю на лексемы
    del lexemes[0]# удаляю нулевой элемент — строку с названием словаря
    fieldList = {} #списки полей из шапок и значений
    i = 0
    for id, lexeme in enumerate(lexemes, 1):
        readLexeme(lexeme, id)
        ## делаю список полей из шапок
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

def readLexeme(lexeme, id):
    inLex = {}
    inLex['id'] = id
    article = []
    for line in lexeme.split('\n'):
        divBySpaces = line.split(' ')
        name = divBySpaces[0]
        content = ' '.join(divBySpaces[1:len(divBySpaces)])
        if name == '\dt' or name.startswith('\g'):
            inLex[name] = content
        else:
            article.append([name, content])
    divideByMS(inLex, article)

def divideByMS(inLex, article):
    MSs = []
    for lineNum in range(article):
        if article[lineNum][0] = '\ms':
            MSs.append(lineNum)

    #for fieldName in ['id', '\\le', '\\leor', '\\ph', '\\u', '\\voc', '\\voir', '\\key', '\\src', '\\ps', '\\psr', '\\pf', '\\pfr', '\\pff']:

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

if __name__ == '__main__':
    main()