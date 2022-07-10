import pydub
import os

root_path = 'D://연구실 문서/외래동물/오디오/'
save_path = 'D://연구실 문서/외래동물/convert/'

for root, dirs, files, in os.walk(root_path):
    for file in files:
        file_ext = file.split('.')[-1]
        if file_ext == 'mp3':
            filepath = root + '/' + file
            print('converting ' + filepath)

            sound = pydub.AudioSegment.from_mp3(filepath)
            filename = file.replace('.%s' % file_ext, '')
            sound.export(save_path + '/' + f'{filename}.wav', format='wav')


save_path = 'D://연구실 문서/외래동물/convert/'

txt_file = open("D://연구실 문서/외래동물/file_names_convert.txt", mode='w')

num = 0

for root, dirs, files, in os.walk(save_path):
    for file in files:
        txt_file.write("%s\n" % file)
        num += 1

print(num)

txt_file.close()
