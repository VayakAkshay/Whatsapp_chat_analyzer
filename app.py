import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp chat analizer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    user_list = df["users"].unique().tolist()
    user_list.remove('notifications')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis",user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        words,num_of_message,total_media,total_links = helper.fetch_stat(selected_user,df)

        with col1:
            st.header("Total Messages")
            st.subheader(num_of_message)

        with col2:
            st.header("Total Words")
            st.subheader(words)

        with col3:
            st.header("Total Media")
            st.subheader(total_media)

        with col4:
            st.header("Total Links")
            st.subheader(total_links)

        if selected_user == "Overall":
            st.title("Most Busy Users")
            col1,col2 = st.columns(2)
            x,new_df = helper.MostBusyUser(df)
            fig,axe = plt.subplots()
            with col1:
                axe.bar(x.index,x.values)
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words

        st.title("Most common Words")
        mostcommondf = helper.MostCommonWords(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(mostcommondf[0],mostcommondf[1])
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        st.title("Emoji Analysis")
        emoji_df = helper.EmojiHelper(selected_user,df)


        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        timeline = helper.MonthlyTimeline(selected_user,df)

        st.title("Monthly Timeline")

        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['Messages'])
        plt.xticks(rotation = "vertical")

        st.pyplot(fig)