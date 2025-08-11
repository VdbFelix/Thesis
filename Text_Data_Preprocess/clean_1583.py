#load libraries
import re
import os
import glob

#iterate through each file in directory with regex, create new output

def clean_punctuation(text):
    text = re.sub(r'(?<=[a-z])\.(?=[a-zA-Z])', '. ', text)
    text = re.sub(r'\b([A-Z])\.(?=\s+[A-Z])', r'\1', text)
    return text

def clean_punctuation_folder(directory_path, output_path):

    for file in os.listdir(directory_path):
        input_file = os.path.join(directory_path, file)
        output_file = os.path.join(output_path, file)

        with open(input_file, "r") as f:
            file_text = f.read()
            
        cleaned_file = clean_punctuation(file_text)

        with open(output_file, "w") as cf:
                cf.write(cleaned_file)
    print(f"Cleaned {len(file)} files.")


input_dir = "your_directory"
output_dir = "your_directory"

clean_punctuation_folder(input_dir, output_dir)  
