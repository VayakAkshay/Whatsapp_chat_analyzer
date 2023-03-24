import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({"user_messages":messages,"message_date":dates})
    df["message_date"] = pd.to_datetime(df["message_date"],format='%m/%d/%y, %H:%M - ')
    df.rename(columns = {"message_date":"Date","user_messages":"Messages"},inplace=True)

    users = []
    messages = []
    for i in df["Messages"]:
        data = re.split('([\w\W]+?):\s',i)
        if data[1:]:
            users.append(data[1])
            messages.append(data[2])
        else:
            users.append("notifications")
            messages.append(data[0])
    df["users"] = users
    df["Messages"] = messages

    df["Days"] = df["Date"].dt.day
    df["Months"] = df["Date"].dt.month_name()
    df["Year"] = df["Date"].dt.year
    df["Hous"] = df["Date"].dt.hour
    df["Minutes"] = df["Date"].dt.minute
    df["Day_Name"] = df["Date"].dt.day_name()
    df["Month"] = df["Date"].dt.month

    Message_type = []
    for i in df["Messages"]:
        pattern1 = '^https://'
        pattern2 = '^<Media omitted>'
        if re.findall(pattern1,i):
            Message_type.append("Link")
        elif re.findall(pattern2,i):
            Message_type.append("File")
        else:
            Message_type.append("Message")

    df["Message_type"] = Message_type

    return df