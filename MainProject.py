
import os
import sys
import csv

# global var:
# video_path = "D:/BIU/FinalProject/data/video/interesting videos/mp4/5.mp4"
# folder_path = 'D:/BIU/FinalProject/Anomalies/labels/'
# name_video = "1"
folder_path = sys.argv[1]
name_video = sys.argv[2]
num_frames = 10000
stop_list = []
sorted_folder = []
first_line = []


# convert to float helper
def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


def create_stop_list(exit_list):
    for i in range(len(exit_list)-1):
        if exit_list[i+1] - exit_list[i] > 15:
            stop_list.append(exit_list[i])


def sort_folder(folder):
    exist_files = []
    for i in range(1, num_frames):
        tmp_file = name_video + "_" + str(i) + ".txt"
        if tmp_file in folder:
            exist_files.append(i)
            tmp_file = folder_path + tmp_file
            sorted_folder.append(tmp_file)
    create_stop_list(exist_files)
    return sorted_folder


def write_csv(gerbil, gerbil_count, flag='a'):
    gerbil.insert(0, gerbil_count)
    file = open(f'{name_video}.csv', flag)
    writer = csv.writer(file)
    writer.writerow(gerbil)


def delete_labels_folder():
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            os.remove(folder_path)


# Create csv file. if there is gap between 2 label neighbours - create seperate calculate. if label move from 2
# gerbil to 1 - add to the closer gerbil. If there are 2 - calculate seperate according to the closer
def cal_labeling(matrix, gerbil, prev_matrix):
    for count, line in enumerate(matrix):
        if line[0] == 0:
            gerbil[0] = gerbil[0] + 1
        elif line[0] == 1:
            gerbil[1] = gerbil[1] + 1


# main func
def main():
    gerbil_count = 1
    # go over all files in folder
    file_matrix = []
    # get_first_frame()
    # write_csv(first_line, name_video, flag='w')
    write_csv(["Look", "Harvest"], "Gerbil num", flag='w')
    gerbil = [0, 0]
    # order the file from 1 to end
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_matrix.append(file_name)
    # loop over all the files
    for count, file_name in enumerate(sort_folder(file_matrix)):
        file = open(file_name, 'r')
        prev_matrix = matrix = []
        # insert the lines of spec file to matrix
        for line in file:
            new_line = line.split(" ")
            tmp_line = []
            for char in new_line:
                if is_float(char):
                    tmp_line.append(float(char))
            matrix.append(tmp_line)
        cal_labeling(matrix, gerbil, prev_matrix)
        if count in stop_list or count == len(file_matrix) - 1:
            for i in range(len(gerbil)):
                gerbil[i] = gerbil[i] / 30
            write_csv(gerbil, gerbil_count)
            gerbil = [0, 0]
            gerbil_count = gerbil_count + 1
        file.close()
        #delete_labels_folder()


if __name__ == '__main__':
    main()
