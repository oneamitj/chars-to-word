import json
import pickle
from pdb import set_trace

# words = {}
#
# with open('words_dictionary.json') as word_dict:
#     words = json.load(word_dict)


def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

words_list = load_words()
alpha_words = {}

# '''
# Create word list by alphabets
for word in words_list:
    alphabet = word[0]
    if alphabet not in alpha_words.keys():
        alpha_words[alphabet] = []
    alpha_words[alphabet].append(word)

for alphabet, words in alpha_words.items():
    words = set(words)
    with open('word_pickle/'+alphabet+'.pickle', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)
# '''

alpha_words = {}

# '''
# Create word list word length
for word in words_list:
    word_length = len(word)
    if word_length not in alpha_words.keys():
        alpha_words[word_length] = []
    alpha_words[word_length].append(word)

for word_length, words in alpha_words.items():
    words = set(words)
    with open('word_pickle/'+str(word_length)+'.pickle', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)
# '''

alpha_words = {}

# '''
# Create word list alphabet and word length
for word in words_list:
    word_length = str(len(word))
    alphabet = word[0]
    key = alphabet+'_'+word_length
    if key not in alpha_words.keys():
        alpha_words[key] = []
    alpha_words[key].append(word)

for alpha_len, words in alpha_words.items():
    words = set(words)
    with open('word_pickle/'+str(alpha_len)+'.pickle', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)
# '''

