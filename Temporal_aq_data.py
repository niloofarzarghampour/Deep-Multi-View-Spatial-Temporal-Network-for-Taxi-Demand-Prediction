#Extract air quality data
import pandas as pd
import  numpy  as  np
import codecs

AQ_VALUE = '../aq_value.vocab'

aq = pd.read_csv('../daily_aqi_by_county_2016.csv')
loc_id = pd.read_csv('../taxi+_zone_lookup.csv')

aq_colnames = aq.columns.tolist()
aq_temp = aq[[aq_colnames[0], aq_colnames[1], aq_colnames[4], aq_colnames[5]]]

state_str = aq_temp[aq_colnames[0]].tolist()
loc_str = aq_temp[aq_colnames[1]].tolist()
date_str = aq_temp[aq_colnames[4]].tolist()
aq_str = aq_temp[aq_colnames[5]].tolist()

aq_ny_2018_1  = []

for  i  in  range ( len ( state_str )):
    temp_data = date_str[i].split('-')
    if state_str[i] == 'New York' and int(temp_data[1]) == 1:
        aq_ny_2018_1.append(
            [loc_str[i], int(temp_data[2]) - 1,
             int(aq_str[i])])

#Because the taxi data is concentrated in Manhattan, Queens, Bronx and Brooklyn, these are all in the city center, so
#Sampling some areas to reduce data, replacing the whole with part
#I select the data of the Bronx and Queens, and average their air quality indicators into a new list,
#Replace the overall environmental data of New York City with this list

aq_ny_counts = [0.] * 31
aq_ny_counts = np.array(aq_ny_counts)
for  i  in  range ( 31 ):
    aqValue = 0.
    timer = 0
    for  j  in  range ( len ( aq_ny_2018_1 )):
        if  aq_ny_2018_1 [ j ] [ 1 ] ==  i  and ( aq_ny_2018_1 [ j ] [ 0 ] ==  'Bronx'
                                        or aq_ny_2018_1[j][0] == "Queens"):
            timer += 1
            aqValue += float(aq_ny_2018_1[j][2])
    aqmean  =  aqValue  //  timer
    aq_ny_counts[i] = aqmean
aq_max = float(np.max(aq_ny_counts))
aq_ny_counts = aq_ny_counts/aq_max

#Expand the air quality data into a 31*266*48 matrix
counts_aq = [[[0.] * 48] *266] * 31
counts_aq = np.array(counts_aq)
for  i  in  range ( 31 ):
    for  j  in  range ( 266 ):
        temp=[aq_ny_counts[i]]*48
        counts_aq[i][j]=temp

#Save the processed air quality data characteristics to the aq_value.vocab file
counts_aq_str = []
data = ""
for  i  in  range ( 31 ):
    for  j  in  range ( 266 ):
        for k in range(48):
            if k < 47:
                data = data + str(counts_aq[i][j][k]) + ' '
            else:
                data = data + str(counts_aq[i][j][k])
        counts_aq_str.append(data)
        data = ""

with codecs.open(AQ_VALUE, 'w', 'utf-8') as file_output:
    for data in counts_aq_str:
        file_output.write(data + '\n')