import html
import codecs
import os

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
        new_path = self.path.replace(old_dir, new_dir)
        os.rename(self.path, new_path)

    def convert(self, input_ext, output_ext):
        output_path = self.path.replace(input_ext, output_ext)
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
        time_array = ['0', '0', ':', '0', '0', ':', '0', '0', '.', '0', '0', '0']
        start_idx = time_array.index('.') + 1
        current_idx = start_idx
        for idx, char in enumerate(time[::-1]):
            if idx == len(time) - 1:
                break_idx = -1
                for i, n in enumerate(time):
                    if i > len(time) - 1 - idx and (n == ':' or n == '.'):
                        break_idx = i
                        break
                for digit in time[break_idx - 1::-1]:
                    time_array[current_idx] = digit
                    current_idx -= 1
            elif char == '.':
                for digit in time[len(time) - idx:]:
                    time_array[current_idx] = digit
                    current_idx += 1
                start_idx -= 2
                current_idx = start_idx
            elif char == ':':
                break_idx = -1
                for i, n in enumerate(time):
                    if i > len(time) - 1 - idx and (n == ':' or n == '.'):
                        break_idx = i
                        break
                for digit in time[break_idx - 1:len(time) - 1 - idx:-1]:
                    time_array[current_idx] = digit
                    current_idx -= 1
                start_idx -= 3
                current_idx = start_idx
        formatted_time = ''
        for char in time_array: formatted_time += char
        return formatted_time

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
    input_ext = '.adb.xml'
    output_ext = '.vtt'
    bad_format_dir = 'badly-formatted-xml'
   
    for file in os.listdir(root_path):
        if not file.endswith(input_ext): continue
        input_file = Input(os.path.join(root_path, file))
        input_file.read_and_check()
        if input_file.is_bad():
            if not os.path.exists(bad_format_dir): os.makedirs(bad_format_dir)
            input_file.move(root_path, os.path.join(root_path, bad_format_dir))
        else: input_file.convert(input_ext, output_ext)

if __name__ == '__main__':
    main()
