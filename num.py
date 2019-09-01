# coding: utf-8

global data
data = []
global states
states = []
global symbols
symbols = []
global listValues
listValues = []
global transitions
transitions = []
global finalStates
finalStates = []

def automaton(word, current, response=None):
    if len(word)>0:
        for char in word:
            if not char in symbols:
                return None

        for state in states[current][symbols.index(word[0])]:
            current = state
            if len(word) == 1:
                if current in finalStates:
                    response = True
                else:
                    continue
            else:
                response = automaton(word[1:], current, response)                   
    return response

#Fix please
def reorder():
    state = 0
    while state <= finalStates[0]:
        a = []
        for symbol in symbols:
            b = []
            for transition in transitions:
                if symbol == transition[1] and state == transition[0]:
                    b.append(transition[2])
            a.append(b)
        states.append(a)
        state += 1

def getInitial(v):
    if (v.isdigit()):
        return int(v)
    else:
        return None

def getSymbol(v, index):
    i = 0
    if(v.isdigit()):
        for n in listValues:
            if(i == index):
                return n
            i += 1    
    return None

def setData(values):
    inital_state = values[0:1]
    end_state = values[2: len(values)]
    index = 1
    for v in end_state:
        index += 1
        data_state = []
        if len(v) > 0:
            data_state.append(int(inital_state))
            if(getSymbol(v, index)):
                data_state.append(getSymbol(v, index))
                data_state.append(getInitial(v))
        if(len(data_state) == 3):
            data.append(data_state)

def setValues(line):
    for idy, char in enumerate(line):
        listValues.append(char)
        if idy > 1 and idy % 2 == 0 :
            symbols.append(char)

def getTransitionTable(path):
    try:
        csv = readFile(path)
        for idx, line in enumerate(csv):
            if len(line) > 1:
                if idx == 0 :
                    setValues(line)
                else:
                    setData(line)
        for item in data:
            if item not in transitions:
                transitions.append(item)

        with open(path) as myfile:
            finalStates.append(int(list(myfile)[-1][0]))

        reorder()
        csv.close()
    except Exception as inst:
        raise Exception(inst)
    finally:
        csv.close()

def readFile(name):
    try:
        x = open(name, 'r')
        return x
    except:
        return('Something went wrong when reading to the file')
        x.close()
        
def isNum(n):
    try:
        getTransitionTable('num.csv') 

        return automaton(n, 0)

    except Exception as e:
        print(e)