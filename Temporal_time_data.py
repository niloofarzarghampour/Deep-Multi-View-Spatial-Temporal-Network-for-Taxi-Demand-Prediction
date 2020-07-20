#Get holiday information and day of the week data
import  numpy  as  np
import codecs

TIME_DATA = '../time.vocab'

#Mark the day of the week in January 2018
week = [
    1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4,
    5, 6, 7, 1, 2, 3
]

#Annotate U.S. holidays in January 2018 (excluding weekends)
holidays = [
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0
]

#Generate time information
time_info = []
for  i  in  range ( 31 ):
    temp = str(week[i]) + '-' + str(holidays[i])
    time_info.append(temp)

#Expand the time information to a matrix of 31*266*48
counts_time = [[["0-0"] * 48] * 266] * 31
counts_time = np.array(counts_time)
for  i  in  range ( 31 ):
    for  j  in  range ( 266 ):
        temp = [time_info[i]] * 48
        temp = np.array(temp)
        counts_time[i][j] = temp

#Save the processed time information data characteristics to the time.vocab file
counts_time_str = []
data = ""
for  i  in  range ( 31 ):
    for  j  in  range ( 266 ):
        for k in range(48):
            if k < 47:
                data = data + counts_time[i][j][k] + ' '
            else:
                data = data + counts_time[i][j][k]
        counts_time_str.append(data)
        data = ""

with codecs.open(TIME_DATA, 'w', 'utf-8') as file_output:
    for data in counts_time_str:
        file_output.write(data + '\n')
© 2020 GitHub, Inc.