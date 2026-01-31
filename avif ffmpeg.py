# import pprint
# import subprocess
# import os
#
# input_folder = r"C:\Users\lenovo\OneDrive\dogonsol.online\thumbnail"
# output_folder = r"C:\Users\lenovo\OneDrive\dogonsol.online\real thumbnail"
# failed_file = []
# files = [   {"file":"no_dog.jpg", "transparent":False},
#             {"file":"solana_goated.jpg", "transparent":False},
#             {"file":"i_told_you.jpg", "transparent":False},
#             {"file":"internal_screaming.jpg", "transparent":False},
#             {"file":"princess.jpg", "transparent":False},
#             {"file":"uno.jpg", "transparent":False},
#             {"file":"dreg0_0.jpg", "transparent":False},
#             {"file":"quino.jpg", "transparent":False},
#             {"file":"dog_transparent.png", "transparent":True},
#          ]
# available = os.listdir(input_folder)
# for i in files:
#     file_name = i["file"]
#     isTransparent = i["transparent"]
#     try:
#         if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and file_name in available:
#             input_file = os.path.join(input_folder, file_name)
#             output_file_name = os.path.splitext(file_name)[0] + '.avif'
#             output_file = os.path.join(output_folder, output_file_name)
#             if isTransparent:
#                 ffmpeg_command = f"ffmpeg -i {input_file} -map 0 -map 0 -filter:v:1 alphaextract -frames:v 1 -c:v libaom-av1 -still-picture 1 -crf 24 {output_file}"
#             else:
#                 ffmpeg_command = f"ffmpeg -i {input_file} -c:v libaom-av1 -still-picture 1 {output_file}"
#             subprocess.run(ffmpeg_command, shell=True, check=True)
#     except Exception:
#         failed_file.append(file_name)
# pprint.pprint(failed_file)

import pprint
import subprocess
import os

input_folder = r"C:\Users\lenovo\Downloads\img"
output_folder = r"C:\Users\lenovo\Downloads\avif"
isTransparent = False
failed_file = []

for file_name in os.listdir(input_folder):
    try:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) :
            input_file = os.path.join(input_folder, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.avif'
            output_file = os.path.join(output_folder, output_file_name)
            if isTransparent:
                ffmpeg_command = f"ffmpeg -i {input_file} -map 0 -map 0 -filter:v:1 alphaextract -frames:v 1 -c:v libaom-av1 -still-picture 1 -crf 24 {output_file}"
            else:
                ffmpeg_command = f"ffmpeg -i {input_file} -c:v libaom-av1 -still-picture 1 {output_file}"
            subprocess.run(ffmpeg_command, shell=True, check=True)
    except Exception:
        failed_file.append(file_name)
pprint.pprint(failed_file)