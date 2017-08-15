import os

def main():
    base_root = os.getcwd()
    bad_file_names = []
    for root, dirs, files in os.walk(base_root):
        for f in files:
            if f.lower() != f:
                bad_file_names.append(os.path.join(root, f).replace(base_root + '\\', ''))

    print('There are ' + str(len(bad_file_names)) + ' file names containing capital letters.')
    for name in bad_file_names:
        print(name)

    input('\nPress ENTER to exit...')

if __name__ == '__main__':
    main()
