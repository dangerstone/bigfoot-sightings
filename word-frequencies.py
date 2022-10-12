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
    "woodland",
    "clearing",
    "grove",
    "park",
    "swamp",
    "meadow",
    "field",
    "thicket",
    "plantation",
    "bush",
    "bushes",
    "shrub",
    "wilderness",
    "plains",
    ###
    "pine",
    "oak",
    "birch",
    "maple",
    "elm",
    "redwood",
    "mangrove",
}


def write_counted_words_to_csv_file(words_counted, title):
    with open("data/word-frequencies/" + title, "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Word", "No. of Reports Containing Word", "Reports"]
        )
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


def clean_and_append_word(word_dict, w, reportno):
    word = clean_word(w)
    if word not in word_dict:
        word_dict[word] = (1, [reportno])  # word : count, [reportno, reportno, ...]
        return

    if reportno in word_dict[word][1]:
        return
    info_tuple = word_dict[word]
    info_tuple_as_list = list(info_tuple)
    info_tuple_as_list[0] += 1
    info_tuple_as_list[1].append(reportno)
    word_dict[word] = tuple(info_tuple_as_list)


time_word_dict = {}
weather_word_dict = {}
environment_word_dict = {}
with open("data/bfro_reports_geocoded.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for index, row in enumerate(reader):
        reportno = row[0]
        if (index % 500) == 0:
            print("Counting words in report no " + str(index) + "...")
        csv_words = re.findall(
            r"[^\d\W]+", row[14].lower()
        )  # ignores numbers and uppercases everything
        for w in csv_words:
            if is_of_interest(w, time_words_of_interest):
                clean_and_append_word(time_word_dict, w, reportno)
            if is_of_interest(w, weather_words_of_interest):
                clean_and_append_word(weather_word_dict, w, reportno)
            if is_of_interest(w, environment_words_of_interest):
                clean_and_append_word(environment_word_dict, w, reportno)

print("\n--- TIME-WORDS ---")
write_counted_words_to_csv_file(time_word_dict, "time-word-frequencies.csv")

print("\n--- WEATHER-WORDS ---")
write_counted_words_to_csv_file(weather_word_dict, "weather-word-frequencies.csv")

print("\n--- ENVIRONMENT-WORDS ---")
write_counted_words_to_csv_file(
    environment_word_dict, "environment-word-frequencies.csv"
)

print("\n")
