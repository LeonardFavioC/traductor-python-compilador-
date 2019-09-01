from num import isNum 
from id import isId 

SPECIALCHAR = [ 'mod', 'pot', '+', '-', '*', '/', '(', ',', ')' ]

def readFile(name):
    try:
        x = open(name, 'r')
        return x
    except:
        return('Something went wrong when reading to the file')
        x.close()
        
def getTockens():
    try:
        txt = readFile('math.txt')
        lines=[]
        for idx, line in enumerate(txt):
            sentence = []
            stack=''
            for char in line.replace(" ", "").split('\n')[0]:
                if char in SPECIALCHAR:
                    if stack:
                        if stack in SPECIALCHAR:
                            sentence += stack[0]
                        elif isNum(stack):
                            sentence.append(dict(type='n', value=int(stack)))
                        elif isId(stack):
                            sentence.append(dict(type='i', value=stack))
                        else:
                            sentence.append(dict(type='u', value=stack))
                        stack=''      
                    sentence.append(char)
                else:
                    stack += char
            if stack:
                if stack in SPECIALCHAR:
                    sentence += stack[0]
                elif isNum(stack):
                    sentence.append(dict(type='n', value=int(stack)))
                elif isId(stack):
                    sentence.append(dict(type='i', value=stack))
                else:
                    sentence.append(dict(type='u', value=stack))
                stack=''
            lines.append(sentence)
        return lines
        txt.close()
    except Exception as e:
        print(e)

