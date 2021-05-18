import os
import cv2


dir = 'C:/VC_golfdb/Golf Swing Videos/'

dir_list = os.listdir(dir)

for main_dir in dir_list:
    main_dir = dir + main_dir + '/'

# main_dir = 'C:/VC_golfdb/Golf Swing Videos/0c18ac27-004a-4825-9457-867351168f9f/'
    file_list = os.listdir(main_dir)

    for file_name in file_list:
        saved_dir = main_dir + file_name.split('.')[0] + '/'
        if not os.path.isdir(saved_dir):
            os.makedirs(saved_dir)

        vidcap = cv2.VideoCapture(main_dir + file_name)

        count = 0

        while vidcap.isOpened():
            ret, image = vidcap.read()
            if not ret:
                break
            if int(vidcap.get(1)) % 1 == 0:
                print('Saved from number: ' + str(int(vidcap.get(1))))
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                cv2.imwrite(saved_dir + 'frame%d.png' % count, image)
                count += 1

        vidcap.release()
