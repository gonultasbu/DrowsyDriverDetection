from keras.models import load_model
import numpy as np
import cv2
import os

model = load_model('DDD_model.h5')


def read_and_predict(image_file):
    im = cv2.imread(image_file)
    im = np.dot(np.array(im, dtype='float32'), [[0.2989], [0.5870], [0.1140]]) / 255
    im = np.expand_dims(im, axis=0)
    im = im.reshape((im.shape[0], im.shape[3]) + im.shape[1:3])
    return model.predict(im, batch_size=32, verbose=0, steps=None)


def traverse_and_call(input_dir):

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
                    if (y1 > 0.5 or y2 > 0.5):
                        prediction_storage[frameno]=0
                        closed_frame_counter=0
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
                    if (y1 > 0.5 or y2 > 0.5):
                        prediction_storage[frameno]=0
                        closed_frame_counter=0

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
            print (int(np.sum(prediction_storage))/int(np.size(prediction_storage)))
        else:
            pass

        if (ns_flag):
            output_file = open(os.path.join(os.path.dirname(root), "nonsleepyCombination.eval"),"w")
            output_file.write(str(int(np.sum(prediction_storage))/int(np.size(prediction_storage))))
            output_file.close()
        elif (s_flag):
            output_file = open(os.path.join(os.path.dirname(root),"sleepyCombination.result"),"w")
            for character in prediction_storage:
                output_file.write(str(int(character)))
            output_file.close()
        else:
            pass



traverse_and_call('C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS\\COMPOUND_DATASET\\Person_001\\glasses')