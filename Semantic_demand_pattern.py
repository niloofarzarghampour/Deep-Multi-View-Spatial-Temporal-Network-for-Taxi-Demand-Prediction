#Build a demand pattern for each location
import  numpy  as  np
import codecs

PICK_DATA = '../img_value.vocab'
DEMAND_VALUE = '../demand_pattern.vocab'

# Take the first four weeks of January, each location corresponds to 4 7-dimensional vectors, and the elements of each vector are the average number of events per day
#Remove the spare in the last three days
with codecs.open(PICK_DATA, 'r', 'utf-8') as dp:
    pickdata  = [ p . strip () for  p  in  dp . readlines ()]

#Find the average number of events per day in each location

#Recover data first
int_pick = []
for  i  in  range ( len ( pickdata )):
    int_pick_temp = [int(w) for w in pickdata[i].split()]
    int_pick.append(int_pick_temp)
    int_pick_temp = []

average0 = []
for  i  in  range ( len ( int_pick )):
    single_average = np.mean(int_pick[i])
    average0.append(single_average)

average = []
for  i  in  range ( 265 ):
    for  j  in  range ( 4 ):
        temp = []
        for k in range(7):
            pointer = i * 31 + j * 7 + k
            temp.append(average0[pointer])
        average.append(temp)

# average is a matrix of 266*4 rows and 7 columns, each 4 rows corresponds to 4 demand_patterns in a location
average = np.array(average)

# Write demand_pattern data into demand_pattern.vocab file
average_str = []
data = ''
for  i  in  range ( 4  *  265 ):
    for  j  in  range ( 7 ):
        data = data + str(average[i][j]) + ' '
    average_str.append(data)
    data = ''

with codecs.open(DEMAND_VALUE, 'w', 'utf-8') as file_output:
    for  data  in  average_str :
        file_output.write(data + '\n')