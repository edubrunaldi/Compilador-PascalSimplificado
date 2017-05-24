import sys
import re
#simbulos da linguagem
simbulos = (':', '(', ')', ',', '.', ';', '{', '}', '<', '>', '<=', '>=', '<>', '=', '+', '-', '*', '/', ':=')

#palavras reservadas da linguagem
reservedWords = ('begin', 'const', 'do', 'else', 'end', 'for', 'if', 'integer', 'procedure', 'program',
                 'read', 'real', 'then', 'var', 'while', 'write')

def doParser(code):
    '''
    separa palavra por palavra, simbulo por simbulo. Faz o parser e o retorna
    :param code: codigo recebido do usuario
    :return: o codigo em parser numa lista (separado devidamente e colocado em uma lista)
    '''
    list_parser = []
    len_code = 0
    word = ''
    while len_code < len(code):
        letter = code[len_code]
        word = ''
        while letter != ' ' and letter != '\n':
            word = word + letter
            len_code += 1
            if len_code >= len(code):
                break
            letter = code[len_code]
        list_parser.append(word)
        len_code += 1
    parser_aux = []
    word = ''
    for i in list_parser:
        if not i.isalnum():
            for letter in i:
                if letter.isalnum() or letter == '_' or (letter == '.' and i[len(i)-1] != letter) or \
                                        (letter == '-' and i[0] == letter) or not (letter in simbulos):
                    word = word + letter
                else:
                    if word != '':
                        parser_aux.append(word)
                        word = ''
                    parser_aux.append(letter)
            if word != '':
                parser_aux.append(word)
                word = ''
        else:
            parser_aux.append(i)
    return parser_aux


def closeTags(cadeia, parser_code, pivo):
    '''
    Procura se as tags se fecham
    :param cadeia:
    :param parser_code:
    :param pivo:
    :return: True - se a tag oposta ta fechada ex: tem { e tem }, False se nao achou o fecho
    '''
    if cadeia == '{':
        tag = '}'
    elif cadeia == '(':
        tag = ')'
    else:
        # pode ser '"' ou "'" que o fecho eh igual
        tag = cadeia

    p = pivo + 1
    while p < len(parser_code):
        if parser_code[p] == tag:
            return True
        p += 1
    return False

def findTokens(parser_code):
    '''
    passa por todas as cadeia e acha seus tokens
    :param parser_code:
    :return: lista de tuplas de 2, contendo (cadeia, token)
    '''
    error = False # retorna se ouve algum erro ou nao
    list_parser_token =[]
    pivo_list = 0
    while pivo_list < len(parser_code):
        cadeia = parser_code[pivo_list]

        regexNum = re.compile("^-?[0-9][a-zA-Z0-9]*(\.[a-zA-Z0-9]+)?$")
        regexAlnum = re.compile("^[a-zA-Z][a-zA-Z0-9_]*$")
        if re.match(regexNum, cadeia):
            regexInt = re.compile("^-?[0-9]+$")
            regexReal = re.compile("^-?[0-9]+\.[0-9]+$")
            regexIntErr = re.compile("^-?[0-9]+[a-zA-Z0-9]+$")
            regexRealErr = re.compile("^-?[0-9]+[a-zA-Z0-9]*\.[a-zA-Z0-9]+$")

   
            if re.match(regexInt, cadeia):
                list_parser_token.append((cadeia, "numero_int"))
            elif re.match(regexReal, cadeia):
                list_parser_token.append((cadeia, "numero_real"))
            elif re.match(regexIntErr, cadeia):
                list_parser_token.append((cadeia, "numero_int incorreto"))
            elif re.match(regexRealErr, cadeia):
                list_parser_token.append((cadeia, "numero_real incorreto"))

        elif re.match(regexAlnum, cadeia):
            if cadeia in reservedWords:
                list_parser_token.append((cadeia, cadeia))
            else:
                if len(cadeia) > 25:
                    list_parser_token.append((cadeia, "ident muito Longo"))
                    error = True
                else:
                    list_parser_token.append((cadeia, "ident"))

        elif cadeia in simbulos:
            regexTags = re.compile("\{|\(")
            if re.match(regexTags, cadeia) is not None and closeTags(cadeia, parser_code, pivo_list):
                if cadeia == '{':
                    while cadeia != '}':
                        pivo_list += 1
                        cadeia = parser_code[pivo_list]
                else:
                    list_parser_token.append((cadeia, cadeia))
            else:
                if re.match(regexTags, cadeia) is not None:
                    list_parser_token.append((cadeia, "Nao fechada"))
                    error = True
                else:
                    list_parser_token.append((cadeia, cadeia))
        else:
            list_parser_token.append((cadeia, "Simbulo nao pertence a linguagem"))
            error = True
        pivo_list += 1

    return list_parser_token, error
