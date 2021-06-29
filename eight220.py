import os
import shutil
from glob import glob


def extract(prev_pose, next_pose):
    arr = []
    count = int(next_pose - prev_pose)
    property_num = round((count / 5) + 1e-08)
    if property_num % 2 != 0:
        property_num -= 1
    for n in range(1, 5):
        name = (property_num * n) + prev_pose
        arr.append(name)
    return arr


def main():
    main_dir = '/Volumes/SSD_250G/tk_unlabeled_videos/back_8_frames/'
    all_frames_dir = '/Volumes/SSD_250G/tk_unlabeled_videos/back_all_frames/'

    for folder in sorted(os.listdir(main_dir)):
        folder_dir = os.path.join(main_dir, folder)
        all_folder_dir = os.path.join(all_frames_dir, folder)
        files = sorted(os.listdir(folder_dir))

        print(folder)
        back = int(files[2].split('_')[-1].split('.')[0])
        top = int(files[3].split('_')[-1].split('.')[0])
        down = int(files[4].split('_')[-1].split('.')[0])
        follow_through = int(files[6].split('_')[-1].split('.')[0])
        finish = int(files[7].split('_')[-1].split('.')[0])

        arr1 = extract(back, top)
        arr2 = extract(top, down)
        arr3 = extract(follow_through, finish)
        print(folder_dir)

        for i in range(4):
            f1 = all_folder_dir + '/' + folder + \
                '_' + str(arr1[i]).zfill(4) + '.png'
            f2 = all_folder_dir + '/' + folder + \
                '_' + str(arr2[i]).zfill(4) + '.png'
            f3 = all_folder_dir + '/' + folder + \
                '_' + str(arr3[i]).zfill(4) + '.png'
            shutil.copy(f1, folder_dir)
            shutil.copy(f2, folder_dir)
            shutil.copy(f3, folder_dir)


if __name__ == '__main__':
    main()
