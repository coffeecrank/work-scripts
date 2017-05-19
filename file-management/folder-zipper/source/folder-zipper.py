import zipfile
import os
import shutil

def main():
    file_names = []
    for root1, dirs1, files1 in os.walk(os.getcwd()):
        for d in dirs1:
            for root2, dirs2, files2 in os.walk(d):
                for f in files2:
                    file_names.append(os.path.join(root1, root2, f))
            zip_files(d, file_names)
            file_names = []
        break

def zip_files(d, file_names):
    archive = zipfile.ZipFile(d + '.zip', 'w')
    
    for f in file_names:
        archive.write(f, os.path.relpath(f, os.getcwd()))
    archive.close()

if __name__ == '__main__':
    main()
