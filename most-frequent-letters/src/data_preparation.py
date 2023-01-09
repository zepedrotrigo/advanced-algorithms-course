import string

def preprocess_text(input_file, stop_words_file, output_file):
    # --- Project Gunteberg Headers removed manually

    with open(input_file, 'r') as f:
        input_text = f.read()

    with open(stop_words_file, 'r') as f:
        stop_words = f.read()

    input_words = input_text.split()
    stop_words = stop_words.split()
    stop_words = [word.upper() for word in stop_words]

    # Remove punctuation marks, stop words and convert to uppercase
    processed_text = []
    table = str.maketrans('', '', string.punctuation)

    for word in input_words:
        processed_word = word.translate(table).upper()

        if processed_word not in stop_words:
            processed_text.append(processed_word)

    # join the filtered words back into a single string
    output_text = ' '.join(processed_text)

    with open(output_file, 'w') as f:
        f.write(output_text)

# ---------------------------------------------------------------------------- #

preprocess_text("../data/63334-0.txt", "../data/stopw.txt", "../data/processed_text.txt")
