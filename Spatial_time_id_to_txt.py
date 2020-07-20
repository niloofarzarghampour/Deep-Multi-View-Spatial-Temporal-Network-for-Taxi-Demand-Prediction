# Generate the pixel value corresponding to the grayscale image
import  numpy  as  np
import codecs
import  os

TOTAL_VALUE = '../total_value.vocab'
IMG_VALUE = '../img_value.vocab'
PIXEL_PATH = '../CNN_IMG_PIXEL_DATA/'

prednum  =  265

# If the image path does not exist, create a path
isExists = os.path.exists(PIXEL_PATH)
if not isExists:
    os.makedirs(PIXEL_PATH)

# Read the number of rides (ie spatial characteristics)
with codecs.open(TOTAL_VALUE, 'r', 'utf-8') as f_img:
    imgValue = [w.strip() for w in f_img.readlines()]

# Restore counts
counts2 = []
maxs  = []
maxs_index= []
for  i  in  range ( len ( imgValue )):
    counts1 = [int(w) for w in imgValue[i].split()]
    counts2.append(counts1)
    maxs.append(max(counts1))
    maxs_index.append(np.argmax(np.array(counts1)))
    counts1 = []
max_value = max(maxs)
index=np.argmax(np.array(maxs))
maxvalue_index = [index, maxs_index[index]]
counts = []
for  i  in  range ( 31 ):
    counts.append(counts2[i * len(counts2) // 31:(i + 1) * len(counts2) // 31])
counts = np.array(counts)

# Get gray data counts_gray
normalize = [[[1. / max_value] * 48] * len(counts[0])] * 31
normalize = np.array(normalize)
counts_gray = counts * normalize
print(counts_gray.shape)
# counts_gray = np.flatten(counts * normalize)

#  image_value.vocab
imgvalue_str  = []
data = ""
for  i  in  range ( 31 ):
    for  j  in  range ( prednum ):
        for k in range(48):
            if k < 47:
                data = data + str(counts[i][(4+j//16) * 24+j % 16+4][k]) + ' '
            else:
                data = data + str(counts[i][(4+j//16) * 24+j % 16+4][k])
        imgvalue_str.append(data)
        data = ""

with codecs.open(IMG_VALUE, 'w', 'utf-8') as file_output:
    for  i  in  range ( len ( imgvalue_str )):
        file_output.write(imgvalue_str[i] + '\n')

# Create a traffic graph for each time period and time of each location in January 2018, with 265*31*48 pictures, and the naming rules for each picture:
# Area id number (1-265)_number of days (00-30)_time period number (00-47)
# size = len(counts_gray[0])
# imgvalue_file = []
# pics = []
# for day in range(31):
#     for time_interval in range(48):
#         pic = []
#         for loc_id in range(prednum):
#             pic.append(counts_gray[day][(4+loc_id//16)
#                                         * 24+loc_id % 16+4][time_interval])
#         imgvalue_file.append(pic)
#         for loc_id in range(len(pic)):
#             pic_value = np.array([[0.]*9]*9)
# # Fill in the center value of the gray matrix
#             pic_value[4][4] = pic[loc_id]
            
#             for k in range(4):
# # Fill the first four values ​​and the last four values ​​of the fifth row of the gray matrix
#                 pic_value[4][k] = counts_gray[day][(4+loc_id//16) * 24+loc_id % 16 + k][time_interval]
#                 pic_value[4][5+k] = counts_gray[day][(4+loc_id//16) * 24+loc_id % 16 + 5 + k][time_interval]
# # Fill the first 4 rows and the last 4 rows of the gray matrix
#                 for i in range(9):
#                     pic_value[k][i] = counts_gray[day][(k+loc_id//16) * 24+loc_id % 16 + i][time_interval]
#                     pic_value[5+k][i] = counts_gray[day][(5+k+loc_id//16) * 24+loc_id % 16 + i][time_interval]
#             pic_value=np.reshape(pic_value,(81,))

# # Save the pixel matrix value of each location at each time of day, and pull it into a row with 81 elements
#             pics.append(pic_value)
#             pixels = ""
#             for s in range(len(pic_value)):
#                 pixels = pixels + str(pic_value[s])+" "

#             if loc_id+1 < 10:
#                 l = "00" + str(loc_id+1)
#             elif loc_id+1 >= 10 and loc_id+1 < 100:
#                 l = "0" + str(loc_id+1)
#             else:
#                 l = str(loc_id+1)

#             if day < 10:
#                 d = "0" + str(day)
#             else:
#                 d = str(day)

#             if time_interval < 10:
#                 t = "0" + str(time_interval)
#             else:
#                 t = str(time_interval)
#             with codecs.open(PIXEL_PATH + l + '_' + d + '_' + t, 'w',
#                              'utf-8') as p:
#                 p.write(pixels)
#                 print(PIXEL_PATH + l + '_' + d + '_' + t+' is done')

print(counts.shape)
print(max_value)
print(maxvalue_index, index//600+1, index%600)
