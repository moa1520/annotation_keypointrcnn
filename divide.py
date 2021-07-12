import os
import json


def bbox_set(image_name, image_id, ball_count, club_count):
    bb_set = {
        "info": {
            "image_name": image_name + ".png",
            "image_id": image_id,
            "person_count": 1,
            "club_count": club_count,
            "ball_count": ball_count
        }
    },
    {
        "bb": {
            "image_id": image_id,
            "person_bb": [
                555,
                199,
                481,
                204
            ],
            "club_bb": [
                433,
                684,
                31,
                53
            ],
            "ball_bb": [
                468,
                680,
                20,
                23
            ]
        }
    }
    return bb_set


def pose(keys, image_id, image_name):
    arr_total = []
    for i in range(0, len(keys), 3):
        arr = [keys[i], keys[i+1], keys[i+2] - 1]
        arr_total.append(arr)
    arr_total = [arr_total]

    json_obj = [
        "info",
        {
            "image_id": int(image_id),
            "person_count": 1,
            "image_name": image_name
        },
        "key",
        {
            "image_id": int(image_id),
            "keypoint_index": arr_total
        }
    ]
    return json_obj


def main():
    root = '/Users/taekyoungkang/Desktop/TK/front_json'
    for file in sorted(os.listdir(root)):
        json_file = os.path.join(root, file)
        with open(json_file) as f:
            obj = json.load(f)

        bbox_obj = dict()
        image_name_obj = dict()

        for i in range(len(obj['annotations'])):
            image_id = obj['annotations'][i]['image_id']
            # body
            if 'num_keypoints' in obj['annotations'][i].keys():
                image_name = obj['images'][i]['coco_url'].split(
                    '/')[-1].split('.')[0]
                body_keypoints = obj['annotations'][i]['keypoints']
                body_bbox = obj['annotations'][i]['bbox']
                pose_json = pose(body_keypoints, image_id=image_id,
                                 image_name=image_name)
                # pose_json = json.dumps(pose_json)

                # pose json파일 저장
                if not os.path.isdir('/Volumes/SSD_250G/ktk/pose/{}'.format(file.split('.')[0])):
                    os.makedirs(
                        '/Volumes/SSD_250G/ktk/pose/{}'.format(file.split('.')[0]))
                with open('/Volumes/SSD_250G/ktk/pose/{}/{}.json'.format(file.split('.')[0], image_name), 'w', encoding='utf-8') as make_file:
                    json.dump(pose_json, make_file, indent='\t')
                #

                bbox_obj[image_id] = {'person_bb': body_bbox}
                image_name_obj[image_id] = image_name

            # ball, club head
            else:
                image_name = image_name_obj[image_id]
                bbox = obj['annotations'][i]['bbox']
                category_id = obj['annotations'][i]['category_id']

                if category_id == '2':  # club_bb
                    bbox_obj[image_id]['club_bb'] = bbox
                else:  # ball_bb
                    bbox_obj[image_id]['ball_bb'] = bbox

        all_bbox = []
        for i in range(len(obj['images'])):
            club_count = 0
            ball_count = 0
            image_id = obj['annotations'][i]['image_id']
            image_name = obj['images'][i]['coco_url'].split(
                '/')[-1].split('.')[0]
            if 'club_bb' in bbox_obj[image_id].keys():
                club_count = len(bbox_obj[image_id]['club_bb']) // 4
            if 'ball_bb' in bbox_obj[image_id].keys():
                ball_count = len(bbox_obj[image_id]['ball_bb']) // 4

            info_set = {
                "info": {
                    "image_name": image_name + ".png",
                    "image_id": image_id,
                    "person_count": 1,
                    "club_count": club_count,
                    "ball_count": ball_count
                }
            }

            if 'club_bb' in bbox_obj[image_id].keys():
                club_bb = bbox_obj[image_id]['club_bb']
            else:
                club_bb = -1
            if 'ball_bb' in bbox_obj[image_id].keys():
                ball_bb = bbox_obj[image_id]['ball_bb']
            else:
                ball_bb = -1

            bb_set = {
                "bb": {
                    "image_id": image_id,
                    "person_bb": bbox_obj[image_id]['person_bb'],
                    "club_bb": club_bb,
                    "ball_bb": ball_bb
                }
            }

            all_bbox.append(info_set)
            all_bbox.append(bb_set)

        all_bbox = {
            "swing{}_detect.json".format(
                str(int(json_file.split('_')[-1].split('.')[0][-4:])).zfill(4)): all_bbox
        }

        # bbox json 파일 저장
        with open('/Volumes/SSD_250G/ktk/bbox/{}.json'.format(file.split('.')[0]), 'w', encoding='utf-8') as make_file:
            json.dump(all_bbox, make_file, indent='\t')
        print(file + "is Done!")


if __name__ == '__main__':
    main()
