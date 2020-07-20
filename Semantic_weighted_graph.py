#Get the weight map of each area
import  numpy  as  np
import codecs
import math
import  os

DEMAND_DATA = '../demand_pattern.vocab'
SEMANTIC_INPUT_FILE = '../SEMANTIC_GRAPH_INPUT_FILE/'


#Implement the DTW algorithm
def dtw(s1, s2):
    r , c  =  only ( s1 ), only ( s2 )
    D1 = np.zeros((r, c))

    for  i  in  range ( s ):
        for j in range(c):
            temp = s1[i] - s2[j]
            if temp > 0:
                D1[i][j] = temp
            else:
                D1[i][j] = 0 - temp

    for  i  in  range ( s ):
        for j in range(c):
            if i - 1 >= 0 and j - 1 >= 0:
                D1 [ i ] [ j ] + =  min ( D1 [ i  -  1 ] [ j  -  1 ], D1 [ i ] [ j  -  1 ], D1 [ i  -  1 ] [ j ])
            elif i - 1 >= 0 and j - 1 < 0:
                D1[i][j] += D1[i - 1][j]
            elif i - 1 < 0 and j - 1 >= 0:
                D1[i][j] += D1[i][j - 1]
            else:
                D1[i][j] = D1[i][j]

    return D1[-1][-1]


#If the file path does not exist, create the path
isExists = os.path.exists(SEMANTIC_INPUT_FILE)
if not isExists:
    os.makedirs(SEMANTIC_INPUT_FILE)

#First restore demand_pattern data
with codecs.open(DEMAND_DATA, 'r', 'utf-8') as dd:
    demandValue0 = [w.strip() for w in dd.readlines()]

demandValue = []
for  i  in  range ( len ( demandValue0 )):
    demandValue_temp = [float(w) for w in demandValue0[i].split()]
    demandValue.append(demandValue_temp)
    demandValue_temp = []
demandValue = np.array(demandValue)

#Each location has a corresponding weight map file every week, a total of 266*4 files
#Naming format for each file: area id_weeks
#Each region has 265 weight values ​​per week, discard inappropriate weight combinations and save them in the file
#Per line: predicted area (local area) weight value of other areas (including local area)
for  i  in  range ( 265 ):
    for  j  in  range ( 4 ):
        filename = SEMANTIC_INPUT_FILE + str(i + 1) + '_' + str(j + 1)
        with codecs.open(filename, 'w', 'utf-8') as file_output:
            dtwValue = []
            num  =  0   #Record how many combinations are written
            dtwtemp  = []   #Record the DTW corresponding to the written weight information to find the smallest DTW
            for k in range(265):
                dtwValue = (dtw(demandValue[i * 4 + j],
                                demandValue[k * 4 + j]))
                if dtwValue == 0:
                    dtwtemp.append(100000000)
                else:
                    dtwtemp.append(dtwValue)
                #If the DTW of two regions at the same time is greater than 100, consider the similarity to be too low and discard the data
                #Because it is an undirected graph, so write two lines at a time
                if dtwValue <= 100. and dtwValue > 0:
                    weight = math.exp(-dtwValue)
                    num  + =  1
                    file_output.write(
                        str(i + 1) + ' ' + str(k + 1) + ' ' + str(weight) +
                        '\n')
                    file_output.write(
                        str(k + 1) + ' ' + str(i + 1) + ' ' + str(weight) +
                        '\n')
            #The DTW of some regional combinations in the same time period may all be greater than 100. If this happens, the file is empty
            #At this time, write the minimum weight information of DTW to the file
            if  whether  ==  0 
                dtwtemp = np.array(dtwtemp)
                lock = np.argmin(dtwtemp)
                minvalue  =  dtwtemp . min ()
                minweight = math.exp(-minvalue)
                file_output.write(
                    str(lock + 1) + ' ' + str(i + 1) + ' ' + str(minweight) +
                    '\n')
                file_output.write(
                    str(i + 1) + ' ' + str(lock + 1) + ' ' + str(minweight) +
                    '\n')