import os
import zipfile

def main():
    main_dir_paths = []
    for root, dirs, files in os.walk(os.getcwd()):
        for d in dirs:
            main_dir_paths.append(os.path.join(os.getcwd(), d))
        break

    for d in main_dir_paths:
        file_count = 0
        file_names = []
        zip_count = 1
        for root, dirs, files in os.walk(d):
            for f in files:
                file_count += 1
                file_names.append(os.path.join(root, f))
                if file_count >= 20:
                    zip_files(d, file_names, zip_count)
                    zip_count += 1
                    file_count = 0
                    file_names = []
            zip_files(d, file_names, zip_count)

def zip_files(dir_path, file_names, zip_count):
    archive = zipfile.ZipFile(dir_path + '_' + str(zip_count) + '.zip', 'w', zipfile.ZIP_DEFLATED)

    reversed_dir_name = ''
    for c in dir_path[::-1]:
        if c == '\\':
            break
        else:
            reversed_dir_name += c

    dir_name = ''
    for c in reversed_dir_name[::-1]:
        dir_name += c
    
    for f in file_names:
        archive.write(f, os.path.join(dir_name, os.path.relpath(f, dir_path)))
    archive.close()

if __name__ == '__main__':
   main()
