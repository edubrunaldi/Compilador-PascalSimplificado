
GRAMMAR = {}
NONTERMINAL = []
TERMINAL = []
FIRST = {}
FOLLOW = {}
PARSING_TABLE = {}

TOKEN_SEQUENCE = []
STACK_MAX_DEPTH = 2000
SYNTAX_RESULT = []

def grammar_scanner():
	fp = open('gramatica_pascal2.ds', 'r')
	grammar_lines = fp.readlines()
	fp.close()
	for each_line in grammar_lines:
		tmp = ''
		bracket = ''
		terminals = []
		nonterminals = []
		sequence = []
		for i in xrange(0, len(each_line)):
			'''
			Para cada linha na gramatica_pascal.ds
			leia e aloca corretamente nas listas de
			terminais e de nao terminais
			 	Terminal fica dentro de  []
				Nao terminal fica dentro de  <>
			'''
			if bracket == '': 
			
				if each_line[i] == '[':
					bracket = ']'
				elif each_line[i] == '<':
					bracket = '>'

			else:
				if each_line[i] == bracket:
					if each_line[i] == ']':
						terminals.append(tmp)
						sequence.append(tmp)
						tmp = ''
						bracket = ''

					else:
						nonterminals.append(tmp)
						sequence.append(tmp)
						tmp = ''
						bracket = ''
				else:
					tmp = tmp + each_line[i]

		if not sequence[0] in GRAMMAR:
			GRAMMAR[sequence[0]] = []
		GRAMMAR[sequence[0]].append(sequence[1:len(sequence)])

		for each in nonterminals:
			if not each in NONTERMINAL:
				NONTERMINAL.append(each)
		for each in terminals:
			if not each in TERMINAL:
				TERMINAL.append(each)

		TERMINAL.append('$')

def getFirst():
	global GRAMMAR, NONTERMINAL, TERMINAL, FIRST

	for each in TERMINAL:
		FIRST[each] = [each]

	for each_nonterminal in NONTERMINAL:
		FIRST[each_nonterminal] = []
		for each_sequence in GRAMMAR[each_nonterminal]:
			if each_sequence == ['null']:
				FIRST[each_nonterminal] = ['null']
	
	stop = False

	while( not stop):
		stop = True
		for each_nonterminal in NONTERMINAL:
			for each_sequence in GRAMMAR.get(each_nonterminal, []):
				counter = 0
				for each_mark in each_sequence:
					for each_marks_first in FIRST[each_mark]:
						if ((each_marks_first != 'null') and (not each_marks_first in FIRST[each_nonterminal])):
							FIRST[each_nonterminal].append(each_marks_first)
							stop = False
					if not 'null' in FIRST[each_mark]:
						break
					else:
						counter += 1

				if (counter == len(each_sequence) and (not 'null' in FIRST[each_nonterminal])):
					FIRST[each_nonterminal].append('null')
					stop = False


def getFollow():
	global GRAMMAR, NONTERMINAL, TERMINAL, FOLLOW

	for each in TERMINAL:
		FOLLOW[each] = []

	for each_nonterminal in NONTERMINAL:
		FOLLOW[each_nonterminal] = []

	FOLLOW['programa'] = ['$']

	for each_nonterminal in NONTERMINAL:
		for each_sequence in GRAMMAR[each_nonterminal]:
			for i in xrange(0, len(each_sequence)-1):
				for each_next_marks_first in FIRST[each_sequence[i+1]]:
					if (not each_next_marks_first in FOLLOW[each_sequence[i]]) and (not each_next_marks_first == 'null'):
						FOLLOW[each_sequence[i]].append(each_next_marks_first)


	stop = False
	while(not stop):
		stop = True

		for each_nonterminal in NONTERMINAL:
			for each_sequence in GRAMMAR[each_nonterminal]:
				for i in xrange(len(each_sequence)-1,-1,-1):
					for each_follow in FOLLOW[each_nonterminal]:
						if not each_follow in FOLLOW[each_sequence[i]]:
							FOLLOW[each_sequence[i]].append(each_follow)
							stop = False
					if not 'null' in FIRST[each_sequence[i]]:
						break;

def get_parsing_table():
	global FIRST, FOLLOW, PARSING_TABLE

	for each_nonterminal in NONTERMINAL:
		PARSING_TABLE[each_nonterminal] = {}
		for each_terminal in TERMINAL:
			PARSING_TABLE[each_nonterminal][each_terminal] = -100

	for each_nonterminal in NONTERMINAL:
		for i in xrange(0, len(GRAMMAR[each_nonterminal])):
			counter = 0
			for each_mark in GRAMMAR[each_nonterminal][i]:
				for each_marks_first in FIRST[each_mark]:
					if PARSING_TABLE[each_nonterminal][each_marks_first] > 0:
						print('nao eh ll1, problema em:')
						print((each_nonterminal+'->'),GRAMMAR[each_nonterminal][i])
						print('e:')
						print((each_nonterminal+'->'),GRAMMAR[each_nonterminal][PARSING_TABLE[each_nonterminal][each_marks_first]])
						print('each_marks_first:',each_marks_first)
						exit(0)
					else:
						PARSING_TABLE[each_nonterminal][each_marks_first] = i
				if not 'null' in FIRST[each_mark]:
					break
				else:
					counter += 1
			if counter == len(GRAMMAR[each_nonterminal][i]):
				for each_follow in FOLLOW[each_nonterminal]:
					if each_follow in TERMINAL:
						if PARSING_TABLE[each_nonterminal][each_follow] > 0:
							print('nao eh ll1, erro em:')
							print(each_nonterminal,'->',GRAMMAR[each_nonterminal][i])
							print('each follow:',each_follow)
							exit(0)
						else:
							PARSING_TABLE[each_nonterminal][each_follow] = i

		for each_nonterminal in NONTERMINAL:
			for each_follow in FOLLOW[each_nonterminal]:
				if PARSING_TABLE[each_nonterminal][each_follow] < 0:
					PARSING_TABLE[each_nonterminal][each_follow] = -1

def syntax_parse():
	global SYNTAX_RESULT

	SYNTAX_RESULT = []
	stack = range(2100)
	stack[0] = 'programa'
	stack_top = 0
	token_curse = 0
	while(stack_top >= 0):
		print('stack_top: ' +str(stack_top))
		if(token_curse >= len(TOKEN_SEQUENCE)):
			print('1')
			SYNTAX_RESULT.append('error: estrutura do programa nao esta completa, nao compilar\n')
			break;
		if stack_top > STACK_MAX_DEPTH:
			print('Aviso: analise preditiva tentou empilhar mais de 2000 saidas')
			exit(0)
		if (stack[stack_top] in TERMINAL):
			#Se for terminal
			print('2')
			if stack[stack_top] == TOKEN_SEQUENCE[token_curse]:
				print('2.1')
				SYNTAX_RESULT.append('folha:[' + TOKEN_SEQUENCE[token_curse]+']\n')

			else:
				print('3')
				SYNTAX_RESULT.append('error: terminal inaceitavel: [' + TOKEN_SEQUENCE[token_curse]+']\n')
			stack_top = stack_top -1
			token_curse = token_curse + 1

		# se for Nao-terminal
		else:
			print('4')
			if PARSING_TABLE[stack[stack_top]][TOKEN_SEQUENCE[token_curse]] < 0:
				print('5')
				if ['Lambda'] in GRAMMAR[stack[stack_top]]:
					print('6')
					tmp_str = 'sucesso: [' + stack[stack_top]+']\t::=\t[Lambda]\n'
					SYNTAX_RESULT.append(tmp_str)
					stack_top = stack_top -1
				else:
					print('7')
					if PARSING_TABLE[stack[stack_top]][TOKEN_SEQUENCE[token_curse]] == -1:
						print('8')
						#se o pop sair errado
						SYNTAX_RESULT.append('error: [ ' + TOKEN_SEQUENCE[token_curse]+']: '+stack[stack_top] + '\n')
						stack_top = stack_top -1
					else:
						print('9')
						SYNTAX_RESULT.append('error: [ '+TOKEN_SEQUENCE[token_curse]+ 'para recuperar o simbolo de erro ignorado, o elemento de topo eh: '+stack[stack_top] + '\n')
						token_curse = token_curse +1

			else:
				#estado aceitavel, trocando o topo da pilha
				print('10')
				tmp_sequence = GRAMMAR[stack[stack_top]][PARSING_TABLE[stack[stack_top]][TOKEN_SEQUENCE[token_curse]]]
				tmp_str = 'sucesso: [ ' + stack[stack_top]+ ']\t::=\t'
				stack_top = stack_top -1
				for x in xrange(0, len(tmp_sequence)):
					tmp_str = tmp_str + '['+tmp_sequence[x]+']'
					stack_top = stack_top +1
					stack[stack_top] = tmp_sequence[len(tmp_sequence)-1-x]
				tmp_str += '\n'
				SYNTAX_RESULT.append(tmp_str)
	if token_curse<(len(TOKEN_SEQUENCE)-1):
		SYNTAX_RESULT.append('error: estrutura do programa nao esta completa, nao compilar! \n')


def reestruture_code(code):
	tokens = []
	for i in code:
		tokens.append(i[1])
	return tokens


def do_syntax(code):
	global GRAMMAR, NONTERMINAL, TERMINAL, TOKEN_SEQUENCE, SYNTAX_RESULT
	grammar_scanner()
	getFirst()
	getFollow()
	get_parsing_table()
	TOKEN_SEQUENCE = reestruture_code(code)
	print(TOKEN_SEQUENCE)
	syntax_parse()
	return SYNTAX_RESULT