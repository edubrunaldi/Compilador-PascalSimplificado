def grammar_scanner():
	fp = open('grammar.ds', 'r')
	grammar_lines = fp.readlines()
	fp.close()
	for each_line in grammar_lines:
		tmp = ''
		bracket = ''
		terminals = []
		nonterminals = []
		sequence = []
		for i in range(0, len(each_line)):
			if bracket = '': 
				# Terminal fica dentro de  []
				#Nao terminal fica dentro de  <>
				if each_line[i] == '[':
					bracket = '['
				elif each_line[i] = '<':
					bracket = '>'

			else:
				pass