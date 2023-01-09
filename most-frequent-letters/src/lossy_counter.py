import math, collections

def lossy_counting(stream, k, epsilon=0.001, sigma= 0.01):
    """
    Identify the frequent items in a stream using the Lossy Counting algorithm.

    Parameters:
    - stream: a list or iterator of items in the data stream
    - k: the maximum number of frequent items to return
    - epsilon: the error tolerance for the frequent items
    - sigma: frequency treshold (for example sigma=0.01 only keeps result with a count higher than 1% of the total count)

    Returns:
    - a list of the k most frequent items in the stream
    """
    n = 0
    frequencies = {}

    # Divide the data stream into multiple windows
    window_width = math.ceil(1 / epsilon)
    windows = [stream[i:i+window_width] for i in range(0, len(stream), window_width)]


    for window in windows:
        for letter in window:
            n += 1
            if letter.isspace():
                continue
            
            if letter in frequencies:
                frequencies[letter] += 1
            else:
                frequencies[letter] = 1
        
        # after each window, decrement all counters by 1
        for key in frequencies.copy().keys():
            frequencies[key] -= 1

            # If counter equals 0 drop it
            if frequencies[key] == 0:
                del frequencies[key]

    # Only save counters with frequency > (sigma - epsilon) * n to reduce false positives
    frequencies = {k:v for k,v in frequencies.items() if v > (sigma-epsilon)*n}

    # sort and return k most frequent items
    top_k = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    if len(top_k) > k:
        top_k = top_k[:k]
    
    return top_k

def main():
    with open("../data/processed_text.txt", 'r') as f:
        data_stream = f.read()

    for k in [3,5,10]:
        top_k = lossy_counting(data_stream, k)

        with open(f"../results/lossy_counter_k{k}.txt", 'w') as f:
            for letter, count in top_k:
                f.write(f'{letter}: {count}\n')

main()