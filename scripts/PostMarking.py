from os import listdir, mkdir, path
import re

### INPUT ###
working_dir = input("Enter directory path containing marked ipynb files (0 to exit): ")
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

default_comment = input("\nEnter default overall comment (required): ")
while len(default_comment.strip()) == 0:
    print("\nDefault comment cannot be empty")
    default_comment = input("\nEnter default overall comment (required): ")

### CREATE OUTPUT DIR ###
dirname = "/processed"
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

    # match cells
    total_score_pattern = r'(\s*\"<b>\s*Student Score:\s*</b>)\s*()s*(\/)\s*(\d+[.]?\d*\s*s*mark.*)'
    question_score_pattern = r'(\s*\"<b>\s*Marks Awarded:\s*</b>)\s*(\d+[.]?\d*\s*)s*(\/)\s*(\d+[.]?\d*\s*)(s*mark.*)'
    teaching_assistant_comment_pattern = r'(\s*\"<b>\s*Teaching\s*Assistant\s*Comment:\s*</b>)\s*()(\\n.*)'

    # variables
    total_score = 0.0
    total_score_line_index = None
    overall_comment_line_index = None
    is_overall_comment = True
    i = 0

    # iterate text
    for line in f.readlines():

        # find overall comment cell
        if re.match(teaching_assistant_comment_pattern, line, re.IGNORECASE) and is_overall_comment:
            is_overall_comment = False
            overall_comment_line_index = i
            output_data.append(line)

        # find total score cell
        elif re.match(total_score_pattern, line, re.IGNORECASE):
            total_score_line_index = i
            output_data.append(line)

        elif re.match(question_score_pattern, line, re.IGNORECASE):
            score = re.match(question_score_pattern, line, re.IGNORECASE).group(2)
            total_score += float(score)

        else:
            output_data.append(line)

        i += 1

    # populate overall comment
    output_data[overall_comment_line_index] = re.sub(teaching_assistant_comment_pattern,
                                                     r'\1 ' + default_comment + r' \3',
                                                     output_data[overall_comment_line_index])

    # update total score
    output_data[total_score_line_index] = re.sub(total_score_pattern,
                                                 r'\1 ' + '%.2f' % total_score + r' \3 \4',
                                                 output_data[total_score_line_index])


    # create output file
    f_out = open(output_dir + "/" + filename, "x")
    f_out.writelines(output_data)

print("\nprocessing completed")

