import os
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import numpy as np
import json
from utils import making_annotations_dic, making_images_dic, making_json

THRESHOLD = 0.95


def main():
    model_key = models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
    model_key.eval()

    main_dir = 'data/images/'
    file_list = os.listdir(main_dir)

    images_dic = []
    annotations_dic = []

    annotation_id = 10000
    
    for i, file_name in enumerate(file_list):
        data = Image.open(main_dir + file_name)
        transform = transforms.ToTensor()
        data = transform(data)

        prediction = model_key([data])[0]

        for box, score, keypoints in zip(prediction['boxes'], prediction['scores'], prediction['keypoints']):
            score = score.detach().numpy()
            if score < THRESHOLD:
                continue

            box = box.detach().numpy().tolist()
            keypoints = keypoints.detach().numpy()

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

            keypoints = np.array([top, keypoints[0], neck, chest,
                                  keypoints[6], keypoints[8], keypoints[10],
                                  keypoints[5], keypoints[7], keypoints[9],
                                  keypoints[11], keypoints[13], keypoints[15],
                                  keypoints[12], keypoints[14], keypoints[16],
                                  keypoints[1], keypoints[2], keypoints[3], keypoints[4], keypoints[0]
                                  ]).tolist()

            width = data.shape[1]
            height = data.shape[2]
            size = [width, height]

            keys = []
            for key in keypoints:
                for k in key:
                    keys.append(k)
            images_dic.append(making_images_dic(i, file_name, size))
            annotations_dic.append(
                making_annotations_dic(annotation_id, i, keys, box))
            annotation_id += 1

    out = making_json(images_dic, annotations_dic)

    with open('./output.json', 'w') as outfile:
        json.dump(out, outfile)


if __name__ == '__main__':
    main()
