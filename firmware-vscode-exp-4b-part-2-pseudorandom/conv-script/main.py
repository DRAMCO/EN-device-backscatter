# Define the path to your text file
file_path = 'pseudorandombinarysequence.txt'

# Open the file in read mode
with open(file_path, 'r') as file:
    # Read the contents of the file
    content = file.read().strip()  # Remove any leading/trailing whitespace

# Split the binary string into 8-bit chunks
binary_chunks = [content[i:i+8] for i in range(0, len(content), 8)]

# Convert each 8-bit chunk to its hexadecimal representation in uppercase
hex_values = [hex(int(chunk, 2))[2:].zfill(2).upper() for chunk in binary_chunks]

# Join the hexadecimal values with commas
hex_string = ', 0x'.join(hex_values)

# # Print the hexadecimal string
# print("Hexadecimal Values:", hex_string)

for i in range(0, len(hex_values), 20):
    print('0x', end='')
    print(', 0x'.join(hex_values[i:i+20]), end='')
    print(',')