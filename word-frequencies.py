# Inspiration taken from: https://stackoverflow.com/questions/50582432/word-count-on-a-csv-of-tweets-returning-error-out-of-range

import csv
from os import environ
import re

import nltk
from nltk.corpus import stopwords

# print(stopwords.words("english"))

stop_words = set(stopwords.words("english"))  # {"", "I", "ABOUT"}

time_words_of_interest = {
    "midday": 0,
    "noon": 0,
    "afternoon": 1,
    "evening": 2,
    "sunset": 3,
    "sundown": 3,
    "dusk": 4,
    "night": 5,
    "midnight": 6,
    "nighttime": 7,
    "dawn": 8,
    "sunrise": 9,
    "sunup": 9,
    "morning": 10,
    "day": 11,
    "daytime": 12,
    # "twilight",
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
            f, fieldnames=["word", "id", "no_of_reports_containing_word", "reports"]
        )
        writer.writeheader()
        for word, id_count_and_reports in words_counted.items():
            f.write(
                "{0}, {1}, {2}, {3}\n".format(
                    word,
                    id_count_and_reports[0],
                    id_count_and_reports[1],
                    "; ".join(str(report) for report in id_count_and_reports[2]),
                )
            )


def is_of_interest(w, words_of_interest):
    return w in words_of_interest


def clean_word(w):
    return w.lower().strip('.,:;()!?"')


def clean_and_append_word(word_dict, w, reportno):
    word = clean_word(w)
    if word not in word_dict:
        word_dict[word] = (
            time_words_of_interest[word],
            1,
            [reportno],
        )  # word : id, count, [reportno, reportno, ...]
        return

    if reportno in word_dict[word][2]:
        return
    info_tuple = word_dict[word]
    info_tuple_as_list = list(info_tuple)
    info_tuple_as_list[1] += 1
    info_tuple_as_list[2].append(reportno)
    word_dict[word] = tuple(info_tuple_as_list)


def tidy_dict(word_dict):
    # sort by id: word_dict = sorted(word_dict.items(), key=lambda item: item[1][0])
    word_dict_copy1 = dict(word_dict)
    word_dict_copy2 = dict(word_dict)
    print(type(word_dict_copy1))
    for word1, id_count_reports1 in word_dict_copy1.items():
        id1 = id_count_reports1[0]
        count1 = id_count_reports1[1]
        reports1 = id_count_reports1[2]
        for word2, id_count_reports2 in word_dict_copy2.items():
            id2 = id_count_reports2[0]
            count2 = id_count_reports2[1]
            reports2 = id_count_reports2[2]
            if id1 == id2 and word1 < word2:
                word_dict[(word1 + "/" + word2)] = (
                    id1,
                    count1 + count2,
                    reports1 + list(set(reports2) - set(reports1)),
                )
                del word_dict[word1]
                del word_dict[word2]
    return word_dict


time_word_dict = {}
weather_word_dict = {}
environment_word_dict = {}
with open("data/bfro_reports_geocoded.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for index, row in enumerate(reader):
        reportno = row[0]  # should match "reportno"-column number
        if (index % 500) == 0:
            print("Counting words in report no " + str(index) + "...")
        csv_words = re.findall(
            r"[^\d\W]+",
            (row[13] + " " + row[14] + " " + row[15]).lower(),
        )
        # should match "title" + "observed" + "location-details"-column numbers
        # ignores numbers and uppercases everything
        for w in csv_words:
            if is_of_interest(w, time_words_of_interest.keys()):
                clean_and_append_word(time_word_dict, w, reportno)
            # if is_of_interest(w, weather_words_of_interest):
            # clean_and_append_word(weather_word_dict, w, reportno)
            # if is_of_interest(w, environment_words_of_interest):
            # clean_and_append_word(environment_word_dict, w, reportno)

time_word_dict = tidy_dict(time_word_dict)

print("\n--- TIME-WORDS ---")
write_counted_words_to_csv_file(time_word_dict, "time-word-frequencies.csv")

print("\n--- WEATHER-WORDS ---")
write_counted_words_to_csv_file(weather_word_dict, "weather-word-frequencies.csv")

print("\n--- ENVIRONMENT-WORDS ---")
write_counted_words_to_csv_file(
    environment_word_dict, "environment-word-frequencies.csv"
)

print("\n")
