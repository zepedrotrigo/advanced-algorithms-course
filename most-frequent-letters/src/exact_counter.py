def count_letters(input_file, k=10):
    with open(input_file, 'r') as f:
        input_text = f.read()

    letter_counter = {}

    for l in input_text:
        if l.isspace():
            continue
        elif l in letter_counter:
            letter_counter[l] += 1
        else:
            letter_counter[l] = 1

    sorted_counts = sorted(letter_counter.items(), key=lambda x: x[1], reverse=True)
    top_k = sorted_counts[:k]

    return top_k

def main():
    for k in [3,5,10]:
        top_k = count_letters("../data/processed_text.txt", k)

        with open(f"../results/exact_counter_k{k}.txt", 'w') as f:
            for letter, count in top_k:
                f.write(f'{letter}: {count}\n')

main()