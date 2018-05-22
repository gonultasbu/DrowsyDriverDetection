import numpy as np
import cv2
import dlib
import os

detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('C:\\Python27\\Lib\\site-packages\\dlib\\shape_predictor_68_face_landmarks.dat')


def crop_eyes(video):
    avi_path=os.path.dirname(video)
    sleepy_directory='sleepyCombination_eyes'
    nonsleepy_directory='nonsleepyCombination_eyes'
    try:
        os.mkdir(os.path.join(avi_path, sleepy_directory))
        os.mkdir(os.path.join(avi_path, nonsleepy_directory))
    except:
        pass


    left_eye_x_center=0
    right_eye_x_center=0
    left_eye_y_center=0
    right_eye_y_center=0
    box_radius=0
    counter=0

    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        resized_left_eye_box=np.zeros((24,24))
        resized_right_eye_box = np.zeros((24, 24))
        # Capture frame-by-frame
        ret, frame = cap.read()

        if frame is not None:
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale
            faces = detector(grayFrame, 0)
            counter = counter + 1


            if len(faces) != 0: # face found
                for k, d in enumerate(faces):
                    detected_landmarks = shape_predictor(grayFrame, d).parts()  # detect landmarks

                landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])  # extract landmark coordinates

                left_eye_y_center = (landmarks[42][0, 1] + landmarks[43][0, 1] + landmarks[44][0, 1] + landmarks[45][0, 1] + landmarks[46][0, 1] + landmarks[47][0, 1]) / 6
                left_eye_x_center = (landmarks[42][0, 0] + landmarks[43][0, 0] + landmarks[44][0, 0] + landmarks[45][0, 0] + landmarks[46][0, 0] + landmarks[47][0, 0]) / 6

                right_eye_y_center = (landmarks[36][0, 1] + landmarks[37][0, 1] + landmarks[38][0, 1] + landmarks[39][0, 1] + landmarks[40][0, 1] + landmarks[41][0, 1]) / 6
                right_eye_x_center = (landmarks[36][0, 0] + landmarks[37][0, 0] + landmarks[38][0, 0] + landmarks[39][0, 0] + landmarks[40][0, 0] + landmarks[41][0, 0]) / 6

                box_radius=landmarks[39][0, 0]-landmarks[36][0, 0]


                left_eye_box = grayFrame[(left_eye_y_center - box_radius):(left_eye_y_center + box_radius),
                          (left_eye_x_center - box_radius):(left_eye_x_center + box_radius)]


                right_eye_box = grayFrame[(right_eye_y_center - box_radius):(right_eye_y_center + box_radius),
                           (right_eye_x_center - box_radius):(right_eye_x_center + box_radius)]
                eyes_undetected_flag=0


            else:
                left_eye_x_center=left_eye_x_center
                right_eye_x_center=right_eye_x_center
                left_eye_y_center=left_eye_y_center
                right_eye_y_center=right_eye_y_center
                box_radius=box_radius



                left_eye_box = grayFrame[(left_eye_y_center - box_radius):(left_eye_y_center + box_radius),
                            (left_eye_x_center - box_radius):(left_eye_x_center + box_radius)]  # Crop the left eye region



                right_eye_box = grayFrame[(right_eye_y_center - box_radius):(right_eye_y_center + box_radius),
                                (right_eye_x_center - box_radius):(right_eye_x_center + box_radius)]  # Crop the left eye region

                eyes_undetected_flag=1

        else:
            print ('unable to read next frame')
            break

        try:
            resized_right_eye_box = cv2.resize(right_eye_box, (24, 24))
            resized_left_eye_box = cv2.resize(left_eye_box, (24, 24))
        except:
            resized_left_eye_box=resized_left_eye_box
            resized_right_eye_box=resized_right_eye_box
            eyes_undetected_flag = 1

        if(video.endswith('nonsleepyCombination (1).avi') == 1):
            if(eyes_undetected_flag==1):
                cv2.imwrite(os.path.join(os.path.join(avi_path, nonsleepy_directory), 'left_'+str(counter)+'x.jpg'), resized_left_eye_box)
                cv2.imwrite(os.path.join(os.path.join(avi_path, nonsleepy_directory), 'right_'+str(counter)+'x.jpg'), resized_right_eye_box)
            else:
                cv2.imwrite(os.path.join(os.path.join(avi_path, nonsleepy_directory), 'left_'+str(counter)+'.jpg'), resized_left_eye_box)
                cv2.imwrite(os.path.join(os.path.join(avi_path, nonsleepy_directory), 'right_'+str(counter)+'.jpg'), resized_right_eye_box)

        else:
            if (eyes_undetected_flag == 1):
                cv2.imwrite(os.path.join(os.path.join(avi_path, sleepy_directory), 'left_'+str(counter)+'x.jpg'), resized_left_eye_box)
                cv2.imwrite(os.path.join(os.path.join(avi_path, sleepy_directory), 'right_'+str(counter)+'x.jpg'), resized_right_eye_box)
            else:
                cv2.imwrite(os.path.join(os.path.join(avi_path, sleepy_directory), 'left_'+str(counter)+'.jpg'), resized_left_eye_box)
                cv2.imwrite(os.path.join(os.path.join(avi_path, sleepy_directory), 'right_'+str(counter)+'.jpg'), resized_right_eye_box)

    cap.release()
    cv2.destroyAllWindows()


def traverse_and_crop(input_dir):
    file_count=0
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith("(1).avi")):
                print(os.path.join(root, name))
                crop_eyes(os.path.join(root,name))
                file_count=file_count+1
    print str(file_count) + " VIDEOS ARE PROCESSED"

traverse_and_crop("C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS\\COMPOUND_DATASET\\Evaluation_Set")