import os

#This function calculates size of the file
def size_in_kb(file_path)-> int:
    stats = os.stat(file_path)
    size_kb = int(stats.st_size/(1024))
    return size_kb

#This function removes the file if it exists
def remove_file(file_path:str):
    if (os.path.exists(file_path)):
        os.remove(file_path)

#This function helps in getting the extension of the file
def get_extension(file_path:str)-> str:
    temp_list = file_path.split(".")
    return temp_list[-1]


def update_data_helper(current_file,filename,new_path,size_in_kb):
    current_file.original_filename = filename
    current_file.file_size = size_in_kb
    current_file.file_path = new_path
