def main():
    dictFile = open('blowo12.txt', 'r', encoding='utf8')
    lexemes = dictFile.read().split('\n\n'): #разделяю на лексемы
    del lexemes[0]# удаляю нулевой элемент — строку с названием словаря
    for lexeme in lexemes:
        readLexeme(lexeme)
    dictFile.close()

if __name__ == '__main__':
    main()