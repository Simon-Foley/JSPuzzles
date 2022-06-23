import string
from time import time
import timeit
import pandas as pd



word_file = open('words.txt', 'r')
words = word_file.readlines()
words = [x.strip().lower() for x in words]

# How you filter a list of words if any chars of word are in set
# letters = {'t', 'e', 's', 't'}
# filteredTest = [word for word in words if all([char not in letters for char in word])]
# print(filteredTest)

used = set()
available = set(string.ascii_lowercase)
print(words)

letterCounts = dict((el, [0,0,0,0,0]) for el in string.ascii_lowercase)
letterCountsTest = dict((el, [0,0,0,0,0]) for el in string.ascii_lowercase)
start = time()
for word in words:
    for idx, char in enumerate(word):
        letterCounts[char][idx] += 1



word_scores = []
for word in words:
    score = 0
    for idx, char in enumerate(word):
        score += letterCounts[char][idx]
    word_scores.append((word, score))

letter_ranks = []
for letter, counts in letterCounts.items():
    letter_ranks.append((letter, sum(counts)))


word_scores.sort(key = lambda x:x[1], reverse=True)
print(word_scores)
letter_ranks.sort(key = lambda x:x[1], reverse=True)
print(letter_ranks)

