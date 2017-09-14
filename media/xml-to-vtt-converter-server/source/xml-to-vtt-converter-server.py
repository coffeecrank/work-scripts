import os
import time
import html
import codecs
import traceback

class Input:
    def __init__(self, path):
        self.path = path;
        self.lines = [];
        self.error = False;

    def read_and_check(self):
        reader = codecs.open(self.path, 'r', 'utf-8')
        for line in reader:
            if not 'begin=\"' in line: continue
            elif 'begin=\"' in line and not 'dur=\"' in line and not 'end=\"' in line:
                self.error = True
                break
            opening_tag_count = 0
            closing_tag_count = 0
            for character in line:
                if character == '<': opening_tag_count += 1
                elif character == '>': closing_tag_count += 1
            if opening_tag_count != closing_tag_count:
                self.error = True
                break
            self.lines.append(line)
        reader.close()

    def is_bad(self):
        return self.error

    def move(self, old_dir, new_dir):
        new_path = self.path.replace(old_dir + '\\', new_dir + '\\')
        os.rename(self.path, new_path)

    def convert(self, input_ext, output_ext, input_dir, output_dir):
        output_path = self.path.replace(input_dir + '\\', output_dir + '\\').replace(input_ext, output_ext)
        output_file = Output(output_path)

        begin_times = []
        end_times = []
        strings = []
        for line in self.lines:
            if not 'begin=\"' in line: continue
            begin_time_start_idx = line.index('begin=\"') + len('begin=\"')
            begin_time_end_idx = line.index('\"', begin_time_start_idx)
            begin_time = line[begin_time_start_idx:begin_time_end_idx]
            begin_time = self.format_time(begin_time)
            if 'end=\"' in line:
                end_time_start_idx = line.index('end=\"') + len('end=\"')
                end_time_end_idx = line.index('\"', end_time_start_idx)
                end_time = line[end_time_start_idx:end_time_end_idx]
                end_time = self.format_time(end_time)
            elif 'dur=\"' in line:
                dur_time_start_idx = line.index('dur=\"') + len('dur=\"')
                dur_time_end_idx = line.index('\"', dur_time_start_idx)
                dur_time = line[dur_time_start_idx:dur_time_end_idx]
                dur_time = self.format_time(dur_time)
                end_time = self.get_end_time(begin_time, dur_time)
            string_start_idx = line.index('>') + len('>')
            string_end_idx = line.index('</p>', string_start_idx)
            string = line[string_start_idx:string_end_idx]
            string = html.unescape(string.replace('<br/>', '\n'))
            begin_times.append(begin_time)
            end_times.append(end_time)
            strings.append(string)
        output_file.write(begin_times, end_times, strings)

    def format_time(self, time):
        time_cur_idx = time.find('.')
        template = '00:00:00.000'
        template_cur_idx = template.find('.')
        if time_cur_idx != -1:
            template = template[:template_cur_idx + 1] + self.add_zeroes(time[time_cur_idx + 1:], template[template_cur_idx + 1:], True)
        else:
            time_cur_idx = len(time)
        if ':' in time:
            time_prev_idx = time_cur_idx
            time_cur_idx = len(time) - 1 - time[::-1].find(':')
            template_prev_idx = template_cur_idx
            template_cur_idx = len(template) - 1 - template[::-1].find(':')
            template = template[:template_cur_idx + 1] + self.add_zeroes(time[time_cur_idx + 1:time_prev_idx], template[template_cur_idx + 1:template_prev_idx], False) + template[template_prev_idx:]
            while ':' in time[:time_cur_idx]:
                time_prev_idx = time_cur_idx
                time_cur_idx = len(time) - 1 - time[::-1].find(':', len(time) - 1 - time_cur_idx + 1)
                template_prev_idx = template_cur_idx
                template_cur_idx = len(template) - 1 - template[::-1].find(':', len(template) - 1 - template_cur_idx + 1)
                template = template[:template_cur_idx + 1] + self.add_zeroes(time[time_cur_idx + 1:time_prev_idx], template[template_cur_idx + 1:template_prev_idx], False) + template[template_prev_idx:]
            template_prev_idx = template_cur_idx
            if ':' in template[:template_cur_idx]:
                template_cur_idx = len(template) - 1 - template[::-1].find(':', len(template) - 1 - template_cur_idx + 1)
            else:
                template_cur_idx = -1
            if template_cur_idx == -1:
                template = self.add_zeroes(time[:time_cur_idx], template[:template_prev_idx], False) + template[template_prev_idx:]
            else:
                template = template[:template_cur_idx + 1] + self.add_zeroes(time[:time_cur_idx], template[template_cur_idx + 1:template_prev_idx], False) + template[template_prev_idx:]
        else:
            template_prev_idx = template_cur_idx
            template_cur_idx = len(template) - 1 - template[::-1].find(':')
            template = template[:template_cur_idx + 1] + self.add_zeroes(time[:time_cur_idx], template[template_cur_idx + 1:template_prev_idx], False) + template[template_prev_idx:]
        return template

    def add_zeroes(self, string, template, add_to_end):
        length_difference = len(template) - len(string)
        zeros_to_add = '0' * length_difference
        if add_to_end:
            new_string = string + zeros_to_add
        else:
            new_string = zeros_to_add + string
        return new_string

    def get_end_time(self, begin_time, dur_time):
        end_time_array = ['0', '0', ':', '0', '0', ':', '0', '0', '.', '0', '0', '0']
        reserved = 0
        for i in range(len(end_time_array) - 1, -1, -1):
            if end_time_array[i] == ':' or end_time_array[i] == '.': continue
            sum_of_digits = int(begin_time[i]) + int(dur_time[i]) + reserved
            if sum_of_digits <= 9:
                end_time_array[i] = str(sum_of_digits)
                reserved = 0
            else:
                end_time_array[i] = str(sum_of_digits)[1]
                reserved = int(str(sum_of_digits)[0])
        end_time = ''
        for char in end_time_array: end_time += char        
        return end_time

class Output:
    def __init__(self, path):
        self.path = path;

    def write(self, begin_times, end_times, strings):
        writer = codecs.open(self.path, 'w', 'utf-8')
        output_text = 'WEBVTT\n\n'
        for i in range(len(strings)):
            output_text += begin_times[i]
            output_text += ' --> '
            output_text += end_times[i]
            output_text += '\n'
            output_text += strings[i]
            output_text += '\n\n'     
        writer.write(output_text)
        writer.close()

def main():
    root_path = os.getcwd()
    input_dir = 'xml'
    input_ext = '.adb.xml'
    output_dir = 'vtt'
    output_ext = '.vtt'
    bad_format_dir = os.path.join(input_dir, 'badly-formatted-xml')
    timer = 10

    print('Put the ADB.XML files into the \"xml\" folder and grab the converted files from the \"vtt\" folder. The converter will run once every 10 seconds, so you can keep this window open.\n')
    
    running = True
    while running:
        if not os.path.exists(input_dir): os.makedirs(input_dir)
        if not os.path.exists(output_dir): os.makedirs(output_dir)     
        for file in os.listdir(input_dir):
            if not file.endswith(input_ext): continue
            elif os.path.exists(os.path.join(output_dir, file.replace(input_ext, output_ext))): continue
            input_file = Input(os.path.join(root_path, input_dir, file))
            input_file.read_and_check()
            if input_file.is_bad():
                print('Processing ' + file + '... Errors found!')
                if not os.path.exists(bad_format_dir): os.makedirs(bad_format_dir)
                input_file.move(input_dir, bad_format_dir)
            else:
                print('Processing ' + file + '... Done!')
                input_file.convert(input_ext, output_ext, input_dir, output_dir)
        time.sleep(timer)

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
    input('\nPress ENTER to exit...')
