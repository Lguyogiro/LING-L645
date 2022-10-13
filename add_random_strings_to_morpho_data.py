"""
this script adds random words to the dataset, in order to guide the encoder-decoder architecture 
to know that most of the characters from the input are just repeated in the output.

run it like $python add_random_strings_to_morpho_data.py <train_file> <output_file_name> <number_of_words_to_gen>
"""
import random
from sys import argv 

train_file = argv[1]
output_file_name = argv[2]
num_words_to_generate = int(argv[3])

with open(train_file) as f:
    lines = [l.strip("\n") for l in f]

vocab = list({ch for line in lines 
              for ch in line.split("\t")[0] if ch not in " +!"})

new_words = []
for i in range(num_words_to_generate):
    length = random.choice(list(range(3, 10)))
    s = []
    for ch in range(length):
        s.append(random.choice(vocab))
    s = " ".join(s)
    new_words.append(s+"\t"+s)

all_train = lines + new_words
random.shuffle(all_train)
with open(output_file_name, "w") as fout:
    fout.write("\n".join(all_train))
