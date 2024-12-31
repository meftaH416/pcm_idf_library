import os
import shutil
from pathlib import Path
import glob

def copy_to_dir(dir1, dir2, file_type='idf', extension='_pcm23.'):
    """
    Copies files from `dir1` to `dir2` after adding a custom extension.
    
    Parameters:
        dir1 (str): Source directory containing files to copy.
        dir2 (str): Destination directory where files will be copied.
        file_type (str): File type to filter for copying (default is 'idf').
        extension (str): Extension to add to copied files (default is '_pcm23.').
        
    Returns:
        None: The function performs the copying task and does not return any value.
    """
    # Change directory to old idf files to work with
    os.chdir(dir1)
    # Getting names of all idf files only
    files = glob.glob("*"+file_type)

    # Loop to edinting name (_pcm23 extension) and saves file to new directory
    for file in files:
        # print(file)
        # print("*"*20)
        st1 = file.split(".")[0]
        st2 = st1 + extension + file.split(".")[1]
        # print(st2)
        # print("*"*20)
        new_dir = os.path.join(dir2, st2)
        shutil.copyfile(file, new_dir)

