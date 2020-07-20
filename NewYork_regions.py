# Generate data file
import  pandas
import math
import codecs
import  numpy  as  np

TOTAL_VALUE = '../total_value.vocab'
grid0 = 25
grid1  =  24

# Get latitude and longitude, ride time
tripdata = pandas.read_csv('../2016_Green_Taxi_Trip_Data .csv')

time_loc = tripdata[['lpep_pickup_datetime',
                     'Pickup_longitude', 'Pickup_latitude']]
time_loc = time_loc.fillna(
    {'lpep_pickup_datetime': 0, 'Pickup_longitude': 0, 'Pickup_latitude': 0})

time_str = time_loc['lpep_pickup_datetime'].tolist()
longitudes = time_loc['Pickup_longitude'].tolist()
latitudes = time_loc['Pickup_latitude'].tolist()

if  len ( time_str ) ==  len ( longitudes ) and  len ( time_str ) ==  len ( latitudes ):
    # Only save data for January 2016
    time_longi_lati  = []
    for  i  in  range ( len ( time_str )):
        month = int(time_str[i].split('/')[0])
        if time_str[i] == 0 or latitudes[i] == 0 or latitudes[i] == 0:
            continue
        if month > 1:
            break
        time_longi_lati . append (
            [time_str[i], longitudes[i], latitudes[i]])

    # print (time_longi_lati [0])
    # print (time_longi_lati [len (time_str) -1])

# Divide the data every moment into 24*25 areas according to latitude and longitude

# First divide by time, create a 31*(25*24)*48 matrix, each element refers to the number of ride events at a specified location during this period
# The interval is 30 minutes
time_2016_01 = []
for  i  in  range ( len ( time_longi_lati )):
    date  =  int ( time_longi_lati [ i ] [ 0 ]. split ( '/' ) [ 1 ])
    timeofday = time_longi_lati[i][0].split(' ')[1:]
    if  timeofday [ 1 ] ==  'AM' :
        hour = int(timeofday[0].split(':')[0])
    else:
        if int(timeofday[0].split(':')[0]) == 12:
            hour = 12
        else:
            hour = int(timeofday[0].split(':')[0])+12
    minute = int(timeofday[0].split(':')[1])
    time_2016_01.append(
        [ date , hour , minute , time_longi_lati [ i ] [ 1 ], time_longi_lati [ i ] [ 2 ]])

time_2016_01 = np.array(time_2016_01)
maxvalue = np.max(time_2016_01, axis=0)
minvalue = np.min(time_2016_01, axis=0)
max_longitude = maxvalue[3]
max_latitude = maxvalue[4]
min_longitude = minvalue[3]
min_latitude = minvalue[4]

# Process the range of longitude to make the division of precision areas more in line with reality
base_longitude5 = max_longitude-(max_longitude-min_longitude)/3
grid_temp = (max_longitude-base_longitude5)/5

low_longitude = max_longitude-2*grid_temp+2.155
high_longitude = max_longitude-grid_temp-0.682
print(low_longitude,high_longitude)

longitude_grid = (high_longitude-low_longitude)/(grid1-8)
left_sparse_longitude_grid = (low_longitude-min_latitude)/4
right_sparse_longitude_grid = (max_longitude-high_longitude)/4

# Processing the dimension range
base_latitude5=min_latitude+4*(max_latitude-min_latitude)/7-0.5
high_latitude0=max_latitude-2*(max_latitude-min_latitude)/14-0.1
grid_temp1=(high_latitude0-base_latitude5)/5

low_latitude = high_latitude0-grid_temp1*3+0.08
high_latitude = high_latitude0-grid_temp1*1-0.705
print(low_latitude,high_laitude)

latitude_grid = (high_latitude-low_latitude)/(grid0-8)
up_sparse_latitude_grid = (low_latitude-min_latitude)/4
down_sparse_latitude_grid = (max_latitude-high_latitude)/4

counts = [[[0]*48]*(grid0*grid1)]*31
counts = np.array(counts)
nums=[0]*6
for  i  in  range ( len ( time_2016_01 )):
    if  time_2016_01 [ i ] [ 3 ] <=  low_longitude :
        if  time_2016_01 [ i ] [ 3 ] ==  low_longitude :
            locid1 = 3
        else:
            locid1 = (time_2016_01[i][3]-min_longitude)/left_sparse_longitude_grid
            locid1 = math.floor(locid1)
        nums[0]+=1
    elif time_2016_01[i][3] >= high_longitude:
        if  time_2016_01 [ i ] [ 3 ] ==  max_longitude :
            locid1  =  23
        else:
            locid1 = (time_2016_01[i][3]-high_longitude)/right_sparse_longitude_grid
            locid1 = math.floor(locid1)+20
        nums[1]+=1
    else:
        locid1 = (time_2016_01[i][3]-low_longitude)/longitude_grid
        locid1 = math.floor(locid1)+4
        nums[2]+=1

    if time_2016_01[i][4] <= low_latitude:
        if  time_2016_01 [ i ] [ 4 ] ==  low_latitude :
            locid0 = 3
        else:
            locid0=(time_2016_01[i][4]-min_latitude)/up_sparse_latitude_grid
            locid0=math.floor(locid0)
        nums[3]+=1
    elif time_2016_01[i][4] >= high_latitude:
        if time_2016_01[i][4] == max_latitude:
            locid0 = 24
        else:
            locid0=(time_2016_01[i][4] - high_latitude)/down_sparse_latitude_grid
            locid0=math.floor(locid0)+21
        nums[4]+=1
    else:
        locid0 = (time_2016_01[i][4]-low_latitude)/latitude_grid
        locid0 = math.floor(locid0)+4
        nums[5]+=1
    # print(nums)
    locID  = ( locid0 * Grid1 + locid1 )

    counts[int(time_2016_01[i][0] - 1)][locid][
        int(time_2016_01[i][1] * 60 + time_2016_01[i][2]) // 30] += 1

# Save the processed characteristics of the number of rides to the img_value.vocab file
counts_str = []
data = ""
for  i  in  range ( 31 ):
    for  j  in  range ( grid0 * grid1 ):
        for k in range(48):
            if k < 47:
                data = data + str(counts[i][j][k]) + ' '
            else:
                data = data + str(counts[i][j][k])
        counts_str.append(data)
        data = ""

with codecs.open(TOTAL_VALUE, 'w', 'utf-8') as file_output:
    for  i  in  range ( len ( counts_str )):
        file_output.write(counts_str[i] + '\n')