def main():
    dictFile = open('blowo12.txt', 'r', encoding='utf8')
    lexemes = dictFile.read().split('\n\n') #разделяю на лексемы
    del lexemes[0]# удаляю нулевой элемент — строку с названием словаря
    common = {}
    i = 0
    for lexeme in lexemes:
        if '\n\ms ' in lexeme:
            i += 1
            for field in commonFields(lexeme):
                if field not in common:
                    common[field] = 1
                else:
                    common[field] += 1
    print(common)
    dictFile.close()

def commonFields(lexeme):
    result = []
    commonLines = lexeme.split('\n\ms ')[0]
    for line in commonLines.split('\n'):
        result.append(line.split(' ')[0])
    return result

if __name__ == '__main__':
    main()