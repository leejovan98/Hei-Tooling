### Input
from os import listdir, mkdir, path
import re

working_dir = input("Enter directory path containing ipynb files to be marked (0 to exit): ")
if working_dir == '0':
    exit()

### RETRIEVE FILES ###
file_names = []
try:
    file_names = listdir(working_dir)
except FileNotFoundError:
    print("Invalid directory!")
    exit()

file_names = [f for f in file_names if f.endswith('.ipynb')]
print(len(file_names), 'files found')

default_comment = input("\nEnter default Teaching Assistant Comment (can be empty): ")

### CREATE OUTPUT DIR ###
dirname = "/marking_folder"
output_dir = working_dir + dirname
if path.exists(output_dir):
    i = 1
    output_dir = working_dir + dirname + '_' + str(i)
    while path.exists(output_dir):
        i += 1
        output_dir = working_dir + dirname + '_' + str(i)
mkdir(output_dir)
print("\noutput directory created: " + output_dir)


### ITERATE FILES ###
for filename in file_names:

    # read file
    f = open(working_dir + "/" + filename)

    # output data
    output_data = []

    # match score cells
    # todo - use for postmarking script
    # total_score_pattern = r'(\s*\"<b>\s*Student Score:\s*</b>)\s*()s*(\/)\s*(\d+[.]?\d*\s*)(s*mark.*)'
    question_score_pattern = r'(\s*\"<b>\s*Marks Awarded:\s*</b>)\s*()s*(\/)\s*(\d+[.]?\d*\s*)(s*mark.*)'
    teaching_assistant_comment_pattern = r'(\s*\"<b>\s*Teaching\s*Assistant\s*Comment:\s*</b>)\s*()(\\n.*)'

    # flags
    # first teaching_assistant_comment_pattern match is for overall comment
    is_overall_teaching_assistant_comment = True

    # iterate text
    for line in f.readlines():

        if re.match(question_score_pattern, line, re.IGNORECASE):
            output_data.append(re.sub(question_score_pattern, r'\1 \4 \3 \4 \5', line))

        elif re.match(teaching_assistant_comment_pattern, line, re.IGNORECASE):
            if is_overall_teaching_assistant_comment:
                is_overall_teaching_assistant_comment = False
                output_data.append(line)
            else:
                output_data.append(re.sub(teaching_assistant_comment_pattern, r'\1 ' + default_comment + r'\3', line))

        else:
            output_data.append(line)

    # create output file
    f_out = open(output_dir + "/" + filename, "x")
    f_out.writelines(output_data)

print("\nprocessing completed")

