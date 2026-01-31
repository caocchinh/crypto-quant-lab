import pprint
import subprocess
import os

input_folder = r"C:\Users\lenovo\OneDrive\dogonsol.online\thumbnail"
output_folder = r"C:\Users\lenovo\OneDrive\dogonsol.online\thumbnail-jpg"
failed_file = []

for file_name in os.listdir(input_folder):
    try:
        if file_name.lower().endswith(('avif')) :
            input_file = os.path.join(input_folder, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.jpg'
            output_file = os.path.join(output_folder, output_file_name)
            ffmpeg_command = f"ffmpeg -i {input_file} -c:v mjpeg -q:v 100 {output_file}"
            subprocess.run(ffmpeg_command, shell=True, check=True)
    except Exception:
        failed_file.append(file_name)
pprint.pprint(failed_file)