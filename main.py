import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import numpy as np
import json
import datetime


def main():
    model_key = models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
    model_key.eval()

    main_dir = 'data/'
    file_name = 'swing041_0072.png'
    data = Image.open(main_dir + file_name)
    transform = transforms.ToTensor()
    data = transform(data)
    data = data.unsqueeze(0)

    prediction = model_key(data)
    boxes = prediction[0]['boxes'].detach().numpy().tolist()
    keypoints = prediction[0]['keypoints'].detach().numpy().tolist()
    width = data.shape[2]
    height = data.shape[3]
    size = [width, height]

    keys = []
    for key in keypoints[0]:
        for k in key:
            keys.append(k)

    out = {
        "info": {
        },
        "licenses": [
        ],
        "images": [
            {
                "coco_url": "http://localhost:8007/images/" + file_name,
                "license": 1,
                "file_name": file_name,
                "height": size[0],
                "width": size[1],
                "date_captured": str(datetime.datetime.now()),
                "flicker_url": "http://localhost:8007/images" + file_name,
                "id": 1
            }
        ],
        "annotations": [
            {
                "id": 1,
                "num_keypoints": 17,
                "category_id": 1,
                "image_id": 1,
                "keypoints": keys,
                "bbox": boxes[0],
            }
        ],
        "categories": [
            {
                "supercategory": "person",
                "id": 1,
                "name": "person",
                "keypoints": [
                    "nose",
                    "left_eye",
                    "right_eye",
                    "left_ear",
                    "right_ear",
                    "left_shoulder",
                    "right_shoulder",
                    "left_elbow",
                    "right_elbow",
                    "left_wrist",
                    "right_wrist",
                    "left_hip",
                    "right_hip",
                    "left_knee",
                    "right_knee",
                    "left_ankle",
                    "right_ankle"
                ],
                "skeleton": [
                    [
                        16,
                        14
                    ],
                    [
                        14,
                        12
                    ],
                    [
                        17,
                        15
                    ],
                    [
                        15,
                        13
                    ],
                    [
                        12,
                        13
                    ],
                    [
                        6,
                        12
                    ],
                    [
                        7,
                        13
                    ],
                    [
                        6,
                        7
                    ],
                    [
                        6,
                        8
                    ],
                    [
                        7,
                        9
                    ],
                    [
                        8,
                        10
                    ],
                    [
                        9,
                        11
                    ],
                    [
                        2,
                        3
                    ],
                    [
                        1,
                        2
                    ],
                    [
                        1,
                        3
                    ],
                    [
                        2,
                        4
                    ],
                    [
                        3,
                        5
                    ],
                    [
                        4,
                        6
                    ],
                    [
                        5,
                        7
                    ]
                ]
            }]
    }

    with open('./test.json', 'w') as outfile:
        json.dump(out, outfile)


if __name__ == '__main__':
    main()
