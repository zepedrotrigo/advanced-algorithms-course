import random

def count_letters(input_file, k=10, fixed_prob=1/16):
    '''Fixed probability counter 1/16'''
    with open(input_file, 'r') as f:
        input_text = f.read()

    letter_counter = {}

    for l in input_text:
        if l.isspace():
            continue

        if random.random() < fixed_prob:
            if l in letter_counter:
                letter_counter[l] += 1
            else:
                letter_counter[l] = 1

    sorted_counts = sorted(letter_counter.items(), key=lambda x: x[1], reverse=True)
    top_k = sorted_counts[:k]

    return top_k

def main():
    for k in [3,5,10]:
        top_k = count_letters("../data/processed_text.txt", k)

        with open(f"../results/approximate_counter_k{k}_try5.txt", 'w') as f:
            for letter, count in top_k:
                f.write(f'{letter}: {count}\n')

main()