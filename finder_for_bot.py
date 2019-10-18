import pickle


def load_word_lib(first_char=None, length=None):
    file_name = 'word_pickle/'
    if first_char and length:
        file_name += first_char + '_' + str(length) + '.pickle'
    elif first_char:
        file_name += first_char + '.pickle'
    elif length:
        file_name += str(length) + '.pickle'
    else:
        raise ValueError("Invalid arguments")

    # print(file_name)
    with open(file_name, 'rb') as word_file:
        valid_words = pickle.load(word_file)

    return valid_words


def char_frequency(str1):
    freq = {}
    for n in str1:
        keys = freq.keys()
        if n in keys:
            freq[n] += 1
        else:
            freq[n] = 1
    return freq


def chars_2_words(chars, length):
    words = load_word_lib(length=length)
    chars_set = set(list(chars.lower()))
    chars_freq = char_frequency(chars)

    valid_words = []
    for word in words:
        word_set = set(list(word))
        if word_set.issubset(chars_set):
            word_freq = char_frequency(word)
            valid = True
            for char, count in word_freq.items():
                if count > chars_freq[char]:
                    valid = False
                    break
            if valid:
                valid_words.append(word)

    return valid_words
