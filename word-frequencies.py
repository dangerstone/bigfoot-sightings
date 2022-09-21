# Inspiration taken from: https://stackoverflow.com/questions/50582432/word-count-on-a-csv-of-tweets-returning-error-out-of-range

import csv
import re


import nltk
from nltk.corpus import stopwords

# print(stopwords.words("english"))

stop_words = set(stopwords.words("english"))  # {"", "I", "ABOUT"}

words = []
with open("data/bfro_reports_geocoded.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for index, row in enumerate(reader):
        if (index % 100) == 0:
            print(index)
        csv_words = re.findall(
            r"[^\d\W]+", row[0].lower()
        )  # ignores numbers and uppercases everything # row[0].split(" ")
        for w in csv_words:
            if w not in stop_words:
                words.append(w.upper().strip('.,:;()!?"'))

wordcount = len(words)

words_counted = []
for index, w in enumerate(words):
    if (index % 1000) == 0:
        print(str(index) + " / " + str(wordcount))
    n = words.count(w)
    words_counted.append((w, n))

words_counted = list(dict.fromkeys(words_counted))
words_counted.sort(key=lambda i: (i[1], i[0]), reverse=True)

# write this to csv file
with open("word-frequencies.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(words_counted)
