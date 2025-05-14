# This code serves to randomly select 80 files across three different directories for a total of 
# 240 files, and export their text to three json files. 
# These will then be used to populate a training entities dataset
# Code mostly generated with Claude

import os
import json
import random


def load_txt_to_json(directory_path, output_file):
     # Get all text files in the directory, extract 80 at random
    all_files = [f for f in os.listdir(directory_path) if f.endswith('.txt') and 
                os.path.isfile(os.path.join(directory_path, f))]
    
    random_files = random.sample(all_files, 80)

    files_data = []

    for filename in random_files:
        file_path = os.path.join(directory_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                files_data.append({
                    "filename": filename,
                    "content": f.read()
                })
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    with open(output_file, 'w', encoding="utf-8") as json_f:
        json.dump(files_data, json_f, indent=4)

    print(f"Successfully processed {len(files_data)} files into {output_file}")
    return len(files_data)


directory_1563 = "/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_text_images/johnfoxe_transcriptions/TXT/1563"
directory_1570 = "/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_text_images/johnfoxe_transcriptions/TXT/1570"
directory_1576 = "/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_text_images/johnfoxe_transcriptions/TXT/1576"


load_txt_to_json(directory_1563, "training_1563.json")
load_txt_to_json(directory_1570, "training_1570.json")
load_txt_to_json(directory_1576, "training_1576.json")
