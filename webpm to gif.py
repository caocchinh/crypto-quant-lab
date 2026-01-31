import pprint
import subprocess
import os

input_folder = r"C:\Users\lenovo\Downloads\telegram_webm"
output_folder = r"C:\Users\lenovo\Downloads\telegram_gif"
failed_file = []

for file_name in os.listdir(input_folder):
    try:
        if file_name.lower().endswith(('.webm')) :
            input_file = os.path.join(input_folder, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.mp4'
            output_file = os.path.join(output_folder, output_file_name)
            print(input_file)
            subprocess.run(f'ffmpeg -i {input_file} -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k -vf "format=rgba, transpose=1" {output_file}', shell=True, check=True)
            # subprocess.run(f'ffmpeg -i {input_file} -i palette.png -filter_complex "fps=10,scale=320:-1:flags=lanczos,format=rgba[x];[x][1:v]paletteuse" {output_file}', shell=True, check=True)

    except Exception:
        failed_file.append(file_name)
pprint.pprint(failed_file)