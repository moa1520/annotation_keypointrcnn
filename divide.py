import os
import json


def read_json(dir):
    with open(dir, 'r') as json_file:
        return json_file


def main():
    json_file_dir = '/Volumes/SSD_250G/tk_unlabeled_videos/front_json/f_00001.json'
    read_json(json_file_dir)


if __name__ == '__main__':
    main()
