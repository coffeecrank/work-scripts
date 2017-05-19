import os
import zipfile

def main():
    zip_count = 1
    file_count = 0
    file_names = []
    for root1, dirs1, files1 in os.walk(os.getcwd()):
        for d in dirs1:
            for root2, dirs2, files2 in os.walk(d):
                for f in files2:
                    file_count += 1
                    file_names.append(os.path.join(root1, root2, f))
                    if file_count >= 40:
                        zip_files(file_names, zip_count)
                        zip_count += 1
                        file_count = 0
                        file_names = []
        zip_files(file_names, zip_count)
        break

def zip_files(file_names, zip_count):
    archive = zipfile.ZipFile('videos_' + str(zip_count) + '.zip', 'w', zipfile.ZIP_DEFLATED)
    
    for f in file_names:
        archive.write(f, os.path.relpath(f, os.getcwd()))
    archive.close()

if __name__ == '__main__':
   main()
