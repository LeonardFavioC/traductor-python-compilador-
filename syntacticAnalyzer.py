
import re
import os
import string
import pandas as pd
from lexicalAnalyzer import getTockens
writeLines=[]
ids = []

def parse(line,firstRule,parsingTable, id):
	flag = 0
	stack = []
	stack.append("$")
	stack.append(firstRule)
	index = 0
	originLine=''
	tokenLine=''

	for char in line:
		if type(char) is dict:
			originLine += str(char['value'])
			tokenLine += char['type']
			if char['type'] == 'i':
			  ids.append(char['value'])
		else:
			originLine += char
			tokenLine += char
	tokenLine += '$'

	while len(stack) > 0:
		top = stack[len(stack)-1]
		currentToken = tokenLine[index]

		if top == currentToken:
			stack.pop()
			index = index + 1
			print (top+'		'+currentToken+'		match')
		else:
			key = top , currentToken
			print (top+'		'+currentToken)

			if key not in parsingTable:
				flag = 1
				break
			value = parsingTable[key]
			if value !='@':
				value = value[::-1]
				value = list(value)
				stack.pop()
				for element in value:
					stack.append(element)
			else:
				stack.pop()
	if flag == 0:
		writeLines.append(originLine)
		print ("				Sintax accepted! ")
	else:
		raise ValueError(str(id+1))

def ll1(follow, productions):
	table = {}
	for key in productions:
		for value in productions[key]:
			if value!='@':
				for element in first(value, productions):
					table[key, element] = value
			else:
				for element in follow[key]:
					table[key, element] = value

	new_table = {}
	for pair in table:
		new_table[pair[1]] = {}

	for pair in table:
		new_table[pair[1]][pair[0]] = table[pair]
	print ("\nTable in matrix \n")
	print (pd.DataFrame(new_table).fillna('-'))
	print ("\n")
	return table

def follow(s, productions, ans):
	if len(s)!=1 :
		return {}

	for key in productions:
		for value in productions[key]:
			f = value.find(s)
			if f!=-1:
				if f==(len(value)-1):
					if key!=s:
						if key in ans:
							temp = ans[key]
						else:
							ans = follow(key, productions, ans)
							temp = ans[key]
						ans[s] = ans[s].union(temp)
				else:
					first_of_next = first(value[f+1:], productions)
					if '@' in first_of_next:
						if key!=s:
							if key in ans:
								temp = ans[key]
							else:
								ans = follow(key, productions, ans)
								temp = ans[key]
							ans[s] = ans[s].union(temp)
							ans[s] = ans[s].union(first_of_next) - {'@'}
					else:
						ans[s] = ans[s].union(first_of_next)
	return ans

def first(s, productions):
	c = s[0]
	ans = set()
	if c.isupper():
		for st in productions[c]:
			if st == '@' :
				if len(s)!=1 :
					ans = ans.union( first(s[1:], productions) )
				else :
					ans = ans.union('@')
			else :
				f = first(st, productions)
				ans = ans.union(x for x in f)
	else:
		ans = ans.union(c)
	return ans

def readFile(name, type):
    try:
        x = open(name, type)
        return x
    except:
		return('Something went wrong when reading to the file')
		x.close()

if __name__=="__main__":
	productions=dict()
	grammar = readFile('grammar', 'r')
	first_dict = dict()
	follow_dict = dict()
	flag = 1
	start = ""

	for line in grammar:
		l = re.split("( |->|\n|\||)*", line)
		lhs = l[0]
		rhs = set(l[1:-1])-{''}
		if flag :
			flag = 0
			start = lhs
		productions[lhs] = rhs

	print ('\nFirst\n')
	for lhs in productions:
		first_dict[lhs] = first(lhs, productions)
	for f in first_dict:
		print (str(f) + " : " + str(first_dict[f]))
	print ("")

	print ('\nFollow\n')
	for lhs in productions:
		follow_dict[lhs] = set()
	follow_dict[start] = follow_dict[start].union('$')

	for lhs in productions:
		follow_dict = follow(lhs, productions, follow_dict)

	for lhs in productions:
		follow_dict = follow(lhs, productions, follow_dict)

	for f in follow_dict:
		print (str(f) + " : " + str(follow_dict[f]))
	ll1Table = ll1(follow_dict, productions)

	try:
		for idx, line in enumerate(getTockens()):
			print('Stack		Current input')
			parse(line, start, ll1Table, idx)
			print('\n')

		python = readFile('example.py', 'w+')
		# escribir el main
		python.write('if __name__ == "__main__": \n')
		for j in ids:
			python.write('\t \t ' + j + ' = 0 \n')
			python.write("\t \t print('ingrese un valor para la variable: %s') \n" %j)
			python.write('\t \t ' + j + "=input() \n")
		python.write("\t \t print('Los resultados de las operaciones son:') \n")
		for i in writeLines:
			python.write("\t \t print('%s' + ' = ' + str(%s)) \n" %(i,i))
			# python.write('\t \t print('+i+')\n')

		python.close()
		os.system('python example.py')

	except Exception as e:
		print ("				Sintax not accepted in line: "+ str(e))