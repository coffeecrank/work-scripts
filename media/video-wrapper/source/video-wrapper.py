import os
import traceback

def main():
    wowza_path = input('Please copy the Wowza path of the video directory: ')
    txt_file_name = 'videos.txt'
    videos_have_folders = input('\nAre your videos stored in separate folders? Type in Y or N: ')
    if videos_have_folders.lower() == 'y':
        videos_have_folders = True
    else:
        videos_have_folders = False
    
    video_list = []
    txt_file = open(txt_file_name, 'r')
    for line in txt_file.readlines():
        video_list.append(line.replace('\n', ''))
    txt_file.close()

    template_file = open('template.html', 'r')
    template = ''
    for line in template_file.readlines():
        template += line + '\n'
    template_file.close()

    print()
    for video in video_list:
        print('Processing ' + video + '...')
        name = video.replace('.mp4', '')
        short_name = name.replace('_med', '')
        short_name = short_name.replace('_hi', '')
        short_name = short_name.replace('_lo', '')
        if videos_have_folders:
            path = os.path.join(wowza_path, short_name, name).replace('\\', '/')
        else:
            path = os.path.join(wowza_path, short_name).replace('\\', '/')
        mp4_path = path + '.mp4'
        jpg_path = path + '.jpg'
        vtt_path = path + '.vtt'
        txt_path = path + '.txt'
        text = template.replace('VIDEO_FOLDER_NAME', short_name)
        text = text.replace('MP4_PATH', mp4_path)
        text = text.replace('JPG_PATH', jpg_path)
        text = text.replace('VTT_PATH', vtt_path)
        text = text.replace('TXT_PATH', txt_path)
        if not os.path.exists(short_name) and videos_have_folders:
            os.makedirs(short_name)
        if videos_have_folders:
            wrapper_file = open(os.path.join(short_name, short_name + '.html'), 'w')
        else:
            wrapper_file = open(short_name + '.html', 'w')
        wrapper_file.write(text)
        wrapper_file.close()

    input('\nPress ENTER to exit...')

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        input('\nPress ENTER to exit...')
