from queue import Empty
import time
import sys
import array

def get_wff(inFile):
    comment = inFile.readline() #Pulls first line of wff for the problem num. and num. of literals per clause
    if comment ==  "": #Returns at end of file
        return []
    layout = comment.split(' ')
    global probNum
    probNum = layout[1]
    global litNum
    litNum = int(layout[2])
    global answer
    answer = layout[3]
    probLine = inFile.readline() #Pulls problem line for number of variables and clauses
    size = probLine.split(' ')
    global varNum
    varNum = int(size[2])
    global numClause
    numClause = int(size[3])
    clauses = []
    for i in range(numClause): #makes list of clauses
        line = inFile.readline()
        literals = line.split(',')
        clauses.append([])
        for j in range(litNum):
            clauses[i].append(literals[j]) #fills list of clauses with literals
    global startTime
    startTime=time.time() #Starts time now that literals are in order
    return clauses

def gen_assign(bruteMask):
    assigned = []
    bitString = str(bin(bruteMask)) #Bitmask generates progressive assignments, with zero being the negation
    bitString = bitString[2:].zfill(varNum) #Fills digits that would be missing in smaller numbers with zero
    for num in range(varNum):
        if bitString[num] == '0':
            assigned.append(str((num+1)*-1)) #negative vairables forthis assignment
        else:
            assigned.append(str(num+1)) # positive variables for this assignment
    return assigned

def ver_assign(clauses,assigned,bruteMask):
    if(bruteMask > 2**(varNum+1)): # If all possible assignments have been tries, return unsatisfiable
        return True, []

    for clause in clauses:
        found = False
        for literal in clause:
            if literal in assigned: #Checks each literal in clause with current assignment
                found = True
        if(not found): #If no literal in a single clause works, the assigment fails and is rejected
            return False, []

    solvars = [] #If it passes 
    for num in range(varNum): #List of variable values for final assigment
        if int(assigned[num]) > 0:
            solvars.append('1') 
        else:
            solvars.append('0')
    return True, solvars
    
def print_out(satisfy,solVars,totCorrect,ansProv,outFile):
    endTime = time.time() 
    totTime = endTime-startTime #Gets time per solve
    if satisfy == answer.strip(): #Compares found answer to answer in file
        correct = 1
        totCorrect += 1
        ansProv +=1
    elif answer.strip() == '?': 
        correct = 0
    else:
        correct = -1
        ansProv += 1
    outFile.write(str(probNum)+','+str(varNum)+','+str(numClause)+','+str(litNum)+','+str(litNum*varNum)+','+str(satisfy)+','+str(correct)+','+str(totTime*(10**6)))
    if(satisfy == 'S'): # Write working assignment if one exists
        for var in solVars:
            outFile.write(','+var)
    outFile.write("\n")
    return totCorrect, ansProv

inFile = open(sys.argv[1],"r")
outFile = open(inFile.name[:-3]+"csv", "w")
satis = 0
unsatis = 0
totCorrect = 0
ansProv = 0
while(True):
    complete = False
    clauses = get_wff(inFile)
    if clauses == []: #If at end of file, break
        break
    bruteMask = 0
    while(not complete): #runs each generation until it suceeds or runs out
        assigned = gen_assign(bruteMask)
        complete, solVars = ver_assign(clauses,assigned,bruteMask)
        bruteMask+=1
    if solVars != []:
        satisfy = 'S'
        satis += 1
    else:
        satisfy = 'U'
        unsatis += 1
    totCorrect, ansProv = print_out(satisfy,solVars,totCorrect,ansProv,outFile)
outFile.write(inFile.name[:-4]+",superComputers,"+str(probNum)+","+str(satis)+","+str(unsatis)+","+str(ansProv)+","+str(totCorrect)+"\n")

outFile.close()
inFile.close()
