# Inspiration taken from: https://stackoverflow.com/questions/50582432/word-count-on-a-csv-of-tweets-returning-error-out-of-range

import csv
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
    ##
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


time_words = []
weather_words = []
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
            if w in time_words_of_interest:  # not in stop_words:
                time_words.append(w.upper().strip('.,:;()!?"'))
            if w in weather_words_of_interest:  # not in stop_words:
                weather_words.append(w.upper().strip('.,:;()!?"'))

timewordcount = len(time_words)
weatherwordcount = len(weather_words)

time_words_counted = []
for index, w in enumerate(time_words):
    if (index % 1000) == 0:
        print(str(index) + " / " + str(timewordcount))
    n = time_words.count(w)
    time_words_counted.append((w, n))

time_words_counted = list(dict.fromkeys(time_words_counted))
time_words_counted.sort(key=lambda i: (i[1], i[0]), reverse=True)

# write this to csv file
with open(
    "data/word-frequencies/time-word-frequencies.csv", "w", encoding="UTF8", newline=""
) as f:
    writer = csv.writer(f)
    writer.writerows(time_words_counted)

weather_words_counted = []
for index, w in enumerate(weather_words):
    if (index % 1000) == 0:
        print(str(index) + " / " + str(weatherwordcount))
    n = weather_words.count(w)
    weather_words_counted.append((w, n))

weather_words_counted = list(dict.fromkeys(weather_words_counted))
weather_words_counted.sort(key=lambda i: (i[1], i[0]), reverse=True)

# write this to csv file
with open(
    "data/word-frequencies/weather-word-frequencies.csv",
    "w",
    encoding="UTF8",
    newline="",
) as f:
    writer = csv.writer(f)
    writer.writerows(weather_words_counted)

""" words_counted = []
for index, w in enumerate(time_words):
    if (index % 1000) == 0:
        print(str(index) + " / " + str(wordcount))
    n = time_words.count(w)
    words_counted.append((w, n))

words_counted = list(dict.fromkeys(words_counted)) # remove duplicates
words_counted.sort(key=lambda i: (i[1], i[0]), reverse=True)

# write this to csv file
with open("data/word-frequencies/word-frequencies.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(words_counted) """
