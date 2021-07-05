import os
import glob

# folders = glob.glob('f_frame')
# print(folders)

root = '/media/tk/SSD_250G/tk_unlabeled_videos/back_20_frames'

for folder in sorted(os.listdir(root)):
    main_root = os.path.join(root, folder)
    print(folder)
    for filename in glob.iglob(root + '/' + folder + '/*.png', recursive=True):
        if filename.split('/')[-1].split('.')[0].split('_')[0] == 'f':
            new_name = 'bad_' + 'front_' + 'swing' + '{0:04d}'.format(int(filename.split('/')[-1].split(
                '.')[0].split('_')[1])) + '_' + filename.split('/')[-1].split('.')[0].split('_')[-1] + '.png'
        else:
            new_name = 'bad_' + 'side_' + 'swing' + '{0:04d}'.format(int(filename.split('/')[-1].split(
                '.')[0].split('_')[1])) + '_' + filename.split('/')[-1].split('.')[0].split('_')[-1] + '.png'

        os.rename(filename, os.path.join(main_root, new_name))
        print(filename, os.path.join(main_root, new_name))

    if folder.split('_')[0] == 'f':
        new_folder_name = 'bad_' + 'front_' + 'swing' + \
            '{0:04d}'.format(int(folder.split('_')[-1]))
    else:
        new_folder_name = 'bad_' + 'side_' + 'swing' + \
            '{0:04d}'.format(int(folder.split('_')[-1]))
    os.rename(root + '/' + folder, root + '/' + new_folder_name)
    print(root + '/' + new_folder_name)
