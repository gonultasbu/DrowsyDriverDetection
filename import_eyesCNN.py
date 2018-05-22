from keras.models import load_model
import numpy as np
import cv2
import os




model = load_model('DDD_model.h5')

def eval_func(dataset_file,processed_file):


    #if cannot read the file, print error
    try:
        datasetFile = open(dataset_file,'r')
        processedFile = open(processed_file,'r')
        main_path= os.path.dirname(dataset_file)
    except IOError:
        print ('CANNOT OPEN ONE OR MANY FILES')
        quit()

    datasetData = datasetFile.read()
    processedData = processedFile.read()

    TruePositiveCounter = 0
    TrueNegativeCounter = 0
    FalsePositiveCounter = 0
    FalseNegativeCounter = 0

    #if len(datasetData) != len(processedData):
    #    print ('FILE LENGTHS DO NOT MATCH, QUITTING!')
    #    quit()


    for i in range(0, len(datasetData)):
        try:
            if datasetData[i] == '1' and processedData[i] == '1':
                TruePositiveCounter += 1
            elif datasetData[i] == '0' and processedData[i] == '0':
                TrueNegativeCounter += 1
            elif datasetData[i] == '0' and processedData[i] == '1':
                FalsePositiveCounter += 1
            elif datasetData[i] == '1' and processedData[i] == '0':
                FalseNegativeCounter += 1
            elif datasetData[i] == '\n' or processedData[i] == '\n':
                print ('EOF')
            else:
                print ('INVALID DATA EXISTS IN THE FILE(S), PLEASE CHECK')
        except:
            pass


    datasetFile.close()
    processedFile.close()
    output_file = open(os.path.join(main_path,"sleepyCombination.eval"), "w")
    output_file.write("TRUE POSITIVE = " + str(TruePositiveCounter) )
    output_file.write("\nTRUE NEGATIVE = " + str(TrueNegativeCounter) )
    output_file.write("\nFALSE POSITIVE = " + str(FalsePositiveCounter) )
    output_file.write("\nFALSE NEGATIVE = " + str(FalseNegativeCounter) )
    output_file.write("\nSUCCESS RATE = " + str(float(TruePositiveCounter+TrueNegativeCounter)/
                                                float(FalseNegativeCounter+TruePositiveCounter+
                                                      TrueNegativeCounter+FalsePositiveCounter)))
    print("SUCCESS RATE = " + str(float(TruePositiveCounter+TrueNegativeCounter)/
                                                float(FalseNegativeCounter+TruePositiveCounter+
                                                      TrueNegativeCounter+FalsePositiveCounter)))
    output_file.close()


    return (str(float(TruePositiveCounter+TrueNegativeCounter)/
                                            float(FalseNegativeCounter+TruePositiveCounter+
                                                    TrueNegativeCounter+FalsePositiveCounter)))






def read_and_predict(image_file):
    im = cv2.imread(image_file)
    im = np.dot(np.array(im, dtype='float32'), [[0.2989], [0.5870], [0.1140]]) / 255
    im = np.expand_dims(im, axis=0)
    im = im.reshape((im.shape[0], im.shape[3]) + im.shape[1:3])
    return model.predict(im, batch_size=32, verbose=0, steps=None)


def traverse_and_call(input_dir):

    open_eyes_frame_bias=12
    CNN_threshold=0.50

    sleepy_success_counter = 0.0
    sleepy_success_accumulator = 0.0

    nonsleepy_success_counter = 0.0
    nonsleepy_success_accumulator = 0.0

    for root, dirs, files in os.walk(input_dir, topdown=False):
        ns_flag=0
        s_flag=0
        total_file_count=len(files)
        closed_frame_counter=0
        if (root.endswith("nonsleepyCombination_eyes")):
            ns_flag=1
            print("Working in directory " + root)
        elif (root.endswith("sleepyCombination_eyes")):
            s_flag=1
            print("Working in directory " + root)
        else:
            continue #skip an unnecessary directory

        try:
            prediction_storage = np.zeros((int(total_file_count / 2)))
        except:
            pass
        for name in files:
            if (name.endswith(".jpg") and name.startswith("left")): #find left_eye.jpg
                if(root.endswith('nonsleepyCombination_eyes')):

                    name_list = name.split('_')
                    pre_frameno_list = name_list[1].split('.')
                    frameno_list = pre_frameno_list[0].split('x')
                    frameno=int(frameno_list[0])-1

                    y1=read_and_predict(os.path.join(root, name))
                    y2=read_and_predict(os.path.join(root, "right_"+str(name_list[1])))
                    y1=float(y1[0])
                    y2=float(y2[0])

                    #do not forget to use x marked frames
                    if (y1 > CNN_threshold or y2 > CNN_threshold):
                        prediction_storage[frameno]=0
                        closed_frame_counter=closed_frame_counter-open_eyes_frame_bias
                        #print(prediction_storage[frameno])
                    else:
                        if (closed_frame_counter<12):
                            prediction_storage[frameno]=0
                            closed_frame_counter=closed_frame_counter+1
                            #print(prediction_storage[frameno])
                        else:
                            prediction_storage[frameno]=1
                            closed_frame_counter=closed_frame_counter+1
                            #print(prediction_storage[frameno])

                elif (root.endswith('sleepyCombination_eyes')):

                    name_list = name.split('_')
                    pre_frameno_list = name_list[1].split('.')
                    frameno_list = pre_frameno_list[0].split('x')
                    frameno=int(frameno_list[0])-1


                    y1=read_and_predict(os.path.join(root, name))
                    y2=read_and_predict(os.path.join(root, "right_"+str(name_list[1])))
                    y1=float(y1[0])
                    y2=float(y2[0])

                    #do not forget to use x marked frames
                    if (y1 > CNN_threshold or y2 > CNN_threshold):
                        prediction_storage[frameno]=0
                        closed_frame_counter=closed_frame_counter-open_eyes_frame_bias

                    else:
                        if (closed_frame_counter<12):
                            prediction_storage[frameno]=0
                            closed_frame_counter=closed_frame_counter+1

                        else:
                            prediction_storage[frameno]=1
                            closed_frame_counter=closed_frame_counter+1

                else:
                    pass
        if (int(np.sum(prediction_storage)) != 0):
            pass
            #print (int(np.sum(prediction_storage))/int(np.size(prediction_storage)))
        else:
            pass

        if (ns_flag):
            nonsleepy_success_counter=nonsleepy_success_counter+1
            output_file = open(os.path.join(os.path.dirname(root), "nonsleepyCombination.eval"),"w")
            output_file.write("SUCCESS RATE = " + str(1 - (int(np.sum(prediction_storage))/
                                                        int(np.size(prediction_storage)))))
            output_file.close()
            print ("SUCCESS RATE = " + str(1 - (int(np.sum(prediction_storage))/
                                                        int(np.size(prediction_storage)))))

            nonsleepy_success_accumulator = nonsleepy_success_accumulator + float(1 - (int(np.sum(prediction_storage))/
                                                        int(np.size(prediction_storage))))
        elif (s_flag):
            sleepy_success_counter=sleepy_success_counter+1
            output_file = open(os.path.join(os.path.dirname(root),"sleepyCombination.result"),"w")
            for character in prediction_storage:
                output_file.write(str(int(character)))
            output_file.close()

            sleepy_success_accumulator = sleepy_success_accumulator + float(eval_func(os.path.join(os.path.dirname(root),"sleepyCombinationLabel.txt"),
                      os.path.join(os.path.dirname(root),"sleepyCombination.result")))
        else:
            pass

    print ( "NONSLEEPY SUCCESS TOTAL = "+ str(nonsleepy_success_accumulator/nonsleepy_success_counter))
    print ( "SLEEPY SUCCESS TOTAL = " + str(sleepy_success_accumulator/sleepy_success_counter))

traverse_and_call('C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS\\COMPOUND_DATASET')