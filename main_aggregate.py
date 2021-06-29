import os
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import numpy as np
import json
from glob import glob
from utils import making_annotations_dic, making_images_dic, making_json

THRESHOLD = 0.95


def main():
    model = models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    if torch.cuda.is_available():
        model.cuda()

    main_dir = '/Volumes/SSD_250G/tk_unlabeled_videos/front_8_frames/f_00001/'
    files_dir = glob(main_dir + '*.png')

    images_dic = []
    annotations_dic = []

    annotation_id = 10000

    for i, file_name in enumerate(files_dir):
        data = Image.open(file_name)
        transform = transforms.ToTensor()
        data = transform(data)
        if torch.cuda.is_available():
            data = data.cuda()

        prediction = model([data])[0]

        images_id = set()
        for box, score, keypoints in zip(prediction['boxes'], prediction['scores'], prediction['keypoints']):
            score = score.cpu().detach().numpy()
            if score < THRESHOLD:
                continue

            box = box.cpu().detach().numpy().tolist()
            keypoints = keypoints.cpu().detach().numpy()

            # 목 추가
            neck = np.append(
                (keypoints[6][:2] + (keypoints[5][:2] - keypoints[6][:2])/2), np.array([1]))
            neck[1] = neck.copy()[1] - 1*(neck.copy()[1] - keypoints[0][1])/5
            # 명치 추가 # 18번
            chest = np.append(
                (keypoints[12][:2] + (keypoints[11][:2] - keypoints[12][:2])/2), np.array([1]))  # 11,12
            chest = neck.copy() - (neck.copy() - chest.copy())/2
            # 머리 추가 # 19번
            top = neck.copy()
            top[1] = keypoints[0][1] - (neck[1] - keypoints[0][1]) * 1

            if ((top[0] - keypoints[0].astype(int)[0])**2 + (top[1] - keypoints[0].astype(int)[1])**2)**(1/2) > 70:
                top[1] = top[1] + 4
            # 왼쪽 발끝, 발뒷꿈치
            L_toe = keypoints[16].astype(int).copy()
            L_toe[0] = keypoints[16].astype(int)[0] - 25
            L_toe[1] = keypoints[16].astype(int)[1] + 20
            L_heal = keypoints[16].astype(int).copy()
            L_heal[0] = keypoints[16].astype(int)[0] + 25
            L_heal[1] = keypoints[16].astype(int)[1] + 20

            # 오른쪽 발끝, 발뒷꿈치
            R_toe = keypoints[15].astype(int).copy()
            R_toe[0] = keypoints[15].astype(int)[0] + 25
            R_toe[1] = keypoints[15].astype(int)[1] + 20
            R_heal = keypoints[15].astype(int).copy()
            R_heal[0] = keypoints[15].astype(int)[0] - 25
            R_heal[1] = keypoints[15].astype(int)[1] + 20

            # Golf club head
            Golf_Club = keypoints[15].astype(int).copy() + 70

            keypoints = np.array([top, keypoints[0], neck, chest,
                                  keypoints[6], keypoints[8], keypoints[10],
                                  keypoints[5], keypoints[7], keypoints[9],
                                  keypoints[11], keypoints[13], keypoints[15],
                                  keypoints[12], keypoints[14], keypoints[16],
                                  L_toe, L_heal, R_toe, R_heal, Golf_Club
                                  ]).tolist()

            width = data.shape[1]
            height = data.shape[2]
            size = [width, height]

            keys = []
            for key in keypoints:
                for k in key:
                    keys.append(k)
            if not i in images_id:
                images_dic.append(making_images_dic(
                    i, file_name.split('/')[-1], size))
                images_id.add(i)
            annotations_dic.append(
                making_annotations_dic(annotation_id, i, keys, box))
            annotation_id += 1

    out = making_json(images_dic, annotations_dic)

    with open('./output.json', 'w') as outfile:
        json.dump(out, outfile)


if __name__ == '__main__':
    main()
