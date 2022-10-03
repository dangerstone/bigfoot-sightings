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


def write_counted_words_to_csv_file(words_counted, title):
    with open("data/word-frequencies/" + title, "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Word", "Occurrences", "Reports"])
        writer.writeheader()
        for word, count_and_reports in sorted(words_counted.items()):
            f.write(
                "{0}, {1}, {2}\n".format(
                    word,
                    count_and_reports[0],
                    "; ".join(str(report) for report in count_and_reports[1]),
                )
            )


def is_of_interest(w, words_of_interest):
    return w in words_of_interest


def clean_word(w):
    return w.upper().strip('.,:;()!?"')


def clean_and_append_word(listboi, w, reportno):
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
        if (index % 500) == 0:
            print("Counting words in report no " + str(index) + "...")
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

print("\n--- TIME-WORDS ---")
write_counted_words_to_csv_file(time_words, "time-word-frequencies.csv")

print("\n--- WEATHER-WORDS ---")
write_counted_words_to_csv_file(weather_words, "weather-word-frequencies.csv")

print("\n--- ENVIRONMENT-WORDS ---")
write_counted_words_to_csv_file(environment_words, "environment-word-frequencies.csv")
