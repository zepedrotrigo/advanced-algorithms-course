# --- Headers removed by hand
import string

def preprocess_text(input_file, stop_words_file, output_file):
    with open(input_file, 'r') as f:
        input_text = f.read()

    with open(stop_words_file, 'r') as f:
        stop_words = f.read()

    input_words = input_text.split()
    stop_words = stop_words.split()

    # remove punctuation marks from words
    table = str.maketrans('', '', string.punctuation)
    stripped_words = [word.translate(table) for word in input_words]

    # convert to uppercase
    uppercase_words = [word.upper() for word in stripped_words]

    # remove stop words
    stop_words = [word.upper() for word in stop_words]
    filtered_words = [word for word in uppercase_words if word not in stop_words]

    # join the filtered words back into a single string
    output_text = ' '.join(filtered_words)

    with open(output_file, 'w') as f:
        f.write(output_text)

# ---------------------------------------------------------------------------- #

preprocess_text("../data/63334-0.txt", "../data/stopw.txt", "../data/processed_text.txt")