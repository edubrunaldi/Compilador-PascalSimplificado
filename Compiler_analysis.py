import sys
from libLexical import *
from libSyntax import do_syntax

def printTable(cadeia_token):
    print('|--------------------------------------|--------------------------------------|')
    print('|               CADEIA                 |                 TOKEN                |')
    print('|--------------------------------------|--------------------------------------|')
    for i in cadeia_token:
        espace1 = ' ' * int((38 - len(i[0]))/2)
        espace2 = ' ' * int((38 - len(i[1]))/2)
        res1 = len(i[0]) % 2
        res2 = len(i[1]) % 2

        if res1==1 and res2==1:
            print('|' + espace1 + i[0] + espace1 + ' |' + espace2 + i[1] + espace2 + ' |')
        elif res1==1 and res2==0:
            print('|' + espace1 + i[0] + espace1 + ' |' + espace2 + i[1] + espace2 + '|')
        elif res1==0 and res2==1:
            print('|' + espace1 + i[0] + espace1 + '|' + espace2 + i[1] + espace2 + ' |')
        else:
            print('|' + espace1 + i[0] + espace1 + '|' + espace2 + i[1] + espace2 + '|')
    print('|--------------------------------------|--------------------------------------|')



if __name__ == '__main__':
    code = sys.stdin.read()
    parser_code = doParser(code)
    #print(code)
    cadeia_token, error = findTokens(parser_code)
    #printTable(cadeia_token)
    if error:
        print('erro na analise lexica, concertar essa parte primeiro!')
        exit(0)
    syntax_result = do_syntax(cadeia_token)
    print('14- syntax result retornada: ')
    for i in syntax_result:
        print(i)
    
