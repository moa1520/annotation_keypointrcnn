import os
import cv2
import glob


dir = '/Users/taekyoungkang/Desktop/TK/dataset/'

video_files = glob.glob(dir + "*.mp4")

if not os.path.isdir('./data'):
    os.makedirs('./data')

for video in video_files:
    file_name = video.split('/')[-1]
    save_dir = './data/' + file_name.split('.')[0]
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    vidcap = cv2.VideoCapture(video)

    count = 0
    while vidcap.isOpened():
        ret, image = vidcap.read()
        if not ret:
            break
        if int(vidcap.get(1)) % 25 == 0:
            print('Saved from number: ' + str(int(vidcap.get(1))))
            cv2.imwrite(save_dir + '/frame_{}.png'.format(count), image)
            count += 1
    vidcap.release()
