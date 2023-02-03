import os
from glob import glob


def delete_trash_files(temp_folder):
    trash_list = glob(temp_folder + '/*.jpg') \
        + glob(temp_folder + '/*.txt') \
        + glob(temp_folder + '/*.xz')

    delete_files(trash_list)


def delete_folder_files(folder):
    file_list = glob(folder + '/*')

    delete_files(file_list)


def delete_files(file_list):
    for filePath in file_list:
        try:
            os.remove(filePath)
        except:
            print("error deleting file : ", filePath)
