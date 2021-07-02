import datetime


def making_images_dic(id, file_name, size):
    out = {
        "coco_url": "http://localhost:8007/" + file_name,
        "license": 1,
        "file_name": file_name,
        "height": size[0],
        "width": size[1],
        "date_captured": str(datetime.datetime.now()),
        "flicker_url": "http://localhost:8007/" + file_name,
        "id": id
    }
    return out


def making_annotations_dic(annotation_id, id, keys, boxes):
    out = {
        "id": annotation_id,
        "num_keypoints": 21,
        "category_id": 1,
        "image_id": id,
        "keypoints": keys,
        "bbox": boxes,
    }
    return out


def making_json(images, annotations):
    out = {
        "info": {
        },
        "licenses": [
        ],
        "images": images,
        "annotations": annotations,
        "categories": [
            {
                "supercategory": "person_bb",
                "id": 1,
                "name": "person_bb",
                "keypoints": [
                    "Top Head",
                    "Nose",
                    "Neck",
                    "Chest",
                    "right_shoulder",
                    "right_elbow",
                    "right_wrist",
                    "left_shoulder",
                    "left_elbow",
                    "left_wrist",
                    "left_hip",
                    "left_knee",
                    "left_ankle",
                    "right_hip",
                    "right_knee",
                    "right_ankle",
                    "right_big_toe",
                    "right_heel",
                    "left_big_toe",
                    "left_heel",
                    "golf_club_head"
                ],
                "skeleton": [
                    # [
                    #     16,
                    #     14
                    # ],
                    # [
                    #     14,
                    #     12
                    # ],
                    # [
                    #     17,
                    #     15
                    # ],
                    # [
                    #     15,
                    #     13
                    # ],
                    # [
                    #     12,
                    #     13
                    # ],
                    # [
                    #     6,
                    #     12
                    # ],
                    # [
                    #     7,
                    #     13
                    # ],
                    # [
                    #     6,
                    #     7
                    # ],
                    # [
                    #     6,
                    #     8
                    # ],
                    # [
                    #     7,
                    #     9
                    # ],
                    # [
                    #     8,
                    #     10
                    # ],
                    # [
                    #     9,
                    #     11
                    # ],
                    # [
                    #     2,
                    #     3
                    # ],
                    # [
                    #     1,
                    #     2
                    # ],
                    # [
                    #     1,
                    #     3
                    # ],
                    # [
                    #     2,
                    #     4
                    # ],
                    # [
                    #     3,
                    #     5
                    # ],
                    # [
                    #     4,
                    #     6
                    # ],
                    # [
                    #     5,
                    #     7
                    # ]
                ]
            },
            {
                "supercategory": "club_bb",
                "id": 2,
                "name": "club_bb",
            },
            {
                "supercategory": "ball_bb",
                "id": 3,
                "name": "ball_bb"
            }
        ]
    }

    return out
