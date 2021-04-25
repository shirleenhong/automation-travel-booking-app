import shutil
import sys

def copy_file_to_log_folder(source, destination):
    shutil.copy2(source, destination)

if __name__ == '__main__':
	copy_file_to_log_folder(sys.argv[1], sys.argv[2])