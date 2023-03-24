from urlextract import URLExtract

extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stat(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    # Total Messages

    messages = df.shape[0]

    # Total Words
    words = []
    for i in df["Messages"]:
        words.extend(i.split())

    # Total Media Files

    total_media = df[df["Message_type"] == "File"].shape[0]

    # Total Links

    links = []

    for i in df["Messages"]:
        links.extend(extract.find_urls(i))

    return len(words), messages, total_media, len(links)


def MostBusyUser(df):
    x = df['users'].value_counts().head()

    # All user percent

    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"})

    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    temp = df[df['Messages'] != "notifications"]
    temp = temp[temp["Messages"] != "<Media omitted>\n"]

    def_wc = wc.generate(temp["Messages"].str.cat(sep=" "))
    return def_wc


def MostCommonWords(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    temp = df[df['Messages'] != "notifications"]
    temp = temp[temp["Messages"] != "<Media omitted>\n"]

    file = open("stop_hinglish.txt", "r")
    stop_words = file.read()

    words = []
    for i in temp["Messages"]:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))


def EmojiHelper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    emojis = []
    for i in df["Messages"]:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def MonthlyTimeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    timeline = df.groupby(['Year', 'Months', 'Month']).count()["Messages"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['Month'][i]) + " - " + str(timeline['Year'][i]))

    timeline['time'] = time
    return timeline
