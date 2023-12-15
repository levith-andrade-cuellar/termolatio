import random

def select_lines(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    n = len(lines)
    chunk_size = n // 5
    selected_lines = []

    for i in range(0, n, chunk_size):
        chunk = lines[i:i + chunk_size]
        selected_lines.extend(random.sample(chunk, min(20, len(chunk))))

    with open(output_file, 'w') as outfile:
        outfile.writelines(selected_lines)

if __name__ == "__main__":
    input_file_path = "input.txt"  
    output_file_path = "tester.txt" 

    select_lines(input_file_path, output_file_path)
