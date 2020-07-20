# Encode the obtained weight map into a 32-dimensional vector and store it in text format
import  numpy  as  np
import codecs
import  os

WEIGHTED_GRAPH = '../SEMANTIC_GRAPH_INPUT_FILE/'
EMBEDDING_VECTOR = '../Embed/'
# Create a path if the file path does not exist
isExists = os.path.exists(EMBEDDING_VECTOR)
if not isExists:
    os.makedirs(EMBEDDING_VECTOR)

# Set a flag, after finding the place where the program ran last time, no longer judge whether the file exists
checkFlag = 0

# Convert weight graph to vector
for  i  in  range ( 265 ):
    for  j  in  range ( 4 ):
        if i + 1 < 10:
            locid = "00" + str(i + 1)
            if i+2 < 10:
                locidnext = "00"+str(i+2)
            else:
                locidnext = "0"+str(i+2)
        elif i + 1 >= 10 and i + 1 < 100:
            locid = "0" + str(i + 1)
            if i+2 < 100:
                locidnext = "0"+str(i+2)
            else:
                locidnext = str(i+2)
        else:
            locid  =  str ( i  +  1 )
            locidnext = str(i+2)
        filename = WEIGHTED_GRAPH + str(i + 1) + '_' + str(j + 1)
        embedding_file = EMBEDDING_VECTOR + locid + '_' + str(j + 1)

        if  checkFlag  ==  0 :
            # Check whether the output file exists, if it exists, delete the file, keep the previous file, and regenerate a new file from the file
            isFileExists = os.path.exists(embedding_file)
            if  j  <  3  and  i  <=  264 :
                isFileExists_next = os.path.exists(
                    EMBEDDING_VECTOR + locid + '_' + str(j + 2))
            elif  j  ==  3  and  i  <  264 :
                isFileExists_next = os.path.exists(EMBEDDING_VECTOR +
                                                   locidnext + '_' + str(1))
            else:
                isFileExists_next = 1
            # If the current file exists, check whether the next file exists, if it exists, enter the next cycle, otherwise, delete the current file and regenerate
            if isFileExists:
                print("##" + embedding_file + "##" + ' is exist.')
                if not isFileExists_next:
                    print("##" + embedding_file + "##" +
                          '\'s next file is not exist!')
                    print("Regenerate " + embedding_file)
                    os.remove(embedding_file)
                    cmd = "./line -train " + filename + " -output " + embedding_file + \
                        " -binary 0 -size 32 -order 2 -negative 5 -samples 100 -rho 0.025 -threads 20"

                    print('\n' + filename)
                    os.system(cmd)
                    print(embedding_file + " has been generated")
                    print(
                        "#######################################################"
                    )
                    checkFlag = 1
                    print(
                        "The program will not judge the file is exist or not!\n"
                    )
                else:
                    print("##" + embedding_file + "##" +
                          '\'s next file is exist!')
                    print("Judgement will continue" + '\n')
            else:
                print("##" + embedding_file + "##" + ' is not exist.' + '\n')
                cmd = "./line -train " + filename + " -output " + embedding_file + \
                    " -binary 0 -size 32 -order 2 -negative 5 -samples 100 -rho 0.025 -threads 20"
                print('\n' + filename)
                os.system(cmd)
                print(embedding_file + " has been generated")
                print(
                    "#######################################################")
                checkFlag = 1
                print("The program will not judge the file is exist or not!\n")

        else:
            cmd = "./line -train " + filename + " -output " + embedding_file + \
                " -binary 0 -size 32 -order 2 -negative 5 -samples 100 -rho 0.025 -threads 20"
            print('\n' + filename)
            os.system(cmd)
            print(embedding_file + " has been generated")
            print("#######################################################")

# Delete the first line of the file, only keep the vector data
for  i  in  range ( 265 ):
    for  j  in  range ( 4 ):
        if i + 1 < 10:
            locid = "00" + str(i + 1)
        elif i + 1 >= 10 and i + 1 < 100:
            locid = "0" + str(i + 1)
        else:
            locid  =  str ( i  +  1 )
        embedding_file = EMBEDDING_VECTOR + locid + '_' + str(j + 1)
        with codecs.open(embedding_file, 'r') as read:
            txt = [w.strip() for w in read.readlines()]
            txt = txt[1:]
        with codecs.open(embedding_file, 'w') as out:
            for data in txt:
                out.write(data + '\n')

# #test
# embedding_file = EMBEDDING_VECTOR + '1_1.1'
# with codecs.open(embedding_file, 'r') as read:
#     txt = [w.strip() for w in read.readlines()]
#     txt = np.array(txt)
#     txt = txt[1:]

# # txt=[]
# # for i in range(len(txt_num)):
# #     txt_temp=[w for w in txt_num[i].split()]
# #     txt.append(txt_temp)

# #     print(txt_num[1])
# #     print(np.shape(txt_num))
# #     print(len(txt_num))
# #     print(txt_num[1][3]+'ppp')
#     # txt = [""] * 266
#     # for i in range(len(txt_num)):
#     #     txt_tmp=""
#     #     for j in range(len(txt_num[0])):
#     #         if j < len(txt_num[0]) - 1:
#     #             txt_tmp+=str(txt_num[i][j]) + ' '
#     #             print(j)
#     #         else:
#     #             txt_tmp += str(txt_num[i][j]) + '\n'
#     #             print(j)
#     #     txt[i]=txt_tmp
#     #     txt_tmp=""
#     # txt = np.array(txt)

# with codecs.open(embedding_file, 'w', 'utf-8') as out:
#     for data in txt:
#         out.write(data+'\n')