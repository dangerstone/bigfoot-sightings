# Inspiration taken from: https://stackoverflow.com/questions/50582432/word-count-on-a-csv-of-tweets-returning-error-out-of-range

import csv
from os import environ
import re


import nltk
from nltk.corpus import stopwords

# print(stopwords.words("english"))

stop_words = set(stopwords.words("english"))  # {"", "I", "ABOUT"}

time_words_of_interest = {
    "dusk",
    "dawn",
    "morning",
    "evening",
    "night",
    "afternoon",
    "midnight",
    "midday",
    "daytime",
    "nighttime",
    "noon",
    "twilight",
    "sunrise",
    "sunup",
    "sunset",
    "daylight",
    "moonlight",
}  # from https://englishstudyonline.org/times-of-day/

weather_words_of_interest = {
    "sunny",
    "humid",
    "stifling",
    "gloomy",
    "rainy",
    "rain",
    "dry",
    "cloudy",
    "foggy",
    "clear",
    "crisp",
    "cool",
    "windy",
    "breezy",
    "wet",
    "overcast",
}  # from https://www.fluentu.com/blog/english/nature-vocabulary/


environment_words_of_interest = {  # NOTE incomplete
    "river",
    "lake",
    "stream",
    "creek",
    "forest",
    "tree",
    "trees",
    "wood",
    "woods",
    "pine",
    "clearing",
    "grove",
}


def count_words(words):
    wordcount = len(words)
    words_counted = []
    for index, w in enumerate(words):
        if (index % 1000) == 0:
            print(str(index) + " / " + str(wordcount))
        n = words.count(w)
        words_counted.append((w, n))
    words_counted = list(dict.fromkeys(words_counted))
    words_counted.sort(key=lambda i: (i[1], i[0]), reverse=True)
    return words_counted


def write_counted_words_to_csv_file(words_counted, title):
    with open("data/word-frequencies/" + title, "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Word", "Occurrences", "Reports"])
        writer.writeheader()
        # writer.writerows(words_counted)
        # writer.writerows((k,) + v for k, v in words_counted.items())
        for count, reports in words_counted.items():
            f.write("{0}, {1}\n".format(count, ", ".join(str(k) for k in reports)))
        # writer = csv.writer(f)
        # writer.writerows(words_counted)


def is_of_interest(w, words_of_interest):
    return w in words_of_interest


def clean_word(w):
    return w.upper().strip('.,:;()!?"')


def clean_and_append_word(listboi, w, reportno):
    # listboi.append(clean_word(w))
    word = clean_word(w)
    if word not in listboi:
        listboi[word] = (1, [])  # word : count, [reportno, reportno, ...]
        return
    beep = listboi[word]
    lst = list(beep)
    lst[0] += 1
    lst[1].append(reportno)
    listboi[word] = tuple(lst)


time_words = {}
weather_words = {}
environment_words = {}
with open("data/bfro_reports_geocoded.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for index, row in enumerate(reader):
        if (index % 100) == 0:
            print("Report no " + str(index) + "...")
        csv_words = re.findall(
            r"[^\d\W]+", row[0].lower()
        )  # ignores numbers and uppercases everything # row[0].split(" ")
        for w in csv_words:
            if is_of_interest(w, time_words_of_interest):
                clean_and_append_word(time_words, w, index)
            if is_of_interest(w, weather_words_of_interest):
                clean_and_append_word(weather_words, w, index)
            if is_of_interest(w, environment_words_of_interest):
                clean_and_append_word(environment_words, w, index)

print("\n--- COUNTING TIME-WORDS ---")
# time_words_counted = count_words(time_words)
# write_counted_words_to_csv_file(time_words_counted, "time-word-frequencies.csv")
write_counted_words_to_csv_file(time_words, "time-word-frequencies.csv")

print("\n--- COUNTING WEATHER-WORDS ---")
# weather_words_counted = count_words(weather_words)
# write_counted_words_to_csv_file(weather_words_counted, "weather-word-frequencies.csv")
write_counted_words_to_csv_file(weather_words, "weather-word-frequencies.csv")

print("\n--- COUNTING ENVIRONMENT-WORDS ---")
# environment_words_counted = count_words(environment_words)
# write_counted_words_to_csv_file(environment_words_counted, "environment-word-frequencies.csv")
write_counted_words_to_csv_file(environment_words, "environment-word-frequencies.csv")
