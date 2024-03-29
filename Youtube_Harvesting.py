import pandas as pd
from googleapiclient.discovery import build
import streamlit as st
import datetime

Api_Key = "Your API KEY"
Api_Name = "youtube"
Api_Version = "v3"

def Api_connect():
    youtube = build(Api_Name, Api_Version, developerKey=Api_Key)
    return youtube

# Function to get the channel details
def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()

    data = []
    for i in response["items"]:
        data.append({
            "Channel_Name": i["snippet"]["title"],
            "Channel_Id": i["id"],
            "Subscribers": i["statistics"]["subscriberCount"],
            "Views": i["statistics"]["viewCount"],
            "Total_videos": i["statistics"]["videoCount"],
            "Channel_description": i["snippet"]["description"],
            "Playlist_Id": i["contentDetails"]["relatedPlaylists"]["uploads"]
        })
    return data


#Function to get the video ids
def get_video_ids(youtube, channel_id):
    video_ids = []
    response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_ids

#Function to get the Video Details
import datetime
def get_Video_Details(youtube, video_ids):
    Video_data = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        for item in response["items"]:
            publish_date_str = item['snippet']['publishedAt']
            publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
            formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')


            data = {
                'Channel_Name': item['snippet']['channelTitle'],
                'channel_Id': item['snippet']['channelId'],
                'Video_Id': item['id'],
                'Title': item['snippet']['title'],
                'Tags': item['snippet'].get('tags'),
                'Thumbnail': item['snippet']['thumbnails']['default']['url'],
                'Description': item['snippet'].get('description'),
                'Publishdate': formatted_publish_date,
                'Duration': item['contentDetails']['duration'],
                'Views': item['statistics'].get('viewCount'),
                'Likes': item['statistics'].get('likeCount'),
                'Comments': item['statistics'].get('commentCount'),
                'Favorite_count': item['statistics'].get('favoriteCount'),
                'Definition': item['contentDetails']['definition'],
                'Caption_Status': item['contentDetails']['caption']
            }
            Video_data.append(data)
    return Video_data

def get_comment_Details(youtube, video_ids):
    Comment_data = []
    try:
        for video_id in video_ids:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response = request.execute()

            for item in response['items']:
                publish_date_str = item['snippet']['topLevelComment']['snippet']['publishedAt']
                publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
                formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'Comment_id': item['snippet']['topLevelComment']['id'],
                    'Video_id': item['snippet']['topLevelComment']['snippet']['videoId'],
                    'Comment_text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'Comment_Author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'Comment_Published':  formatted_publish_date
                }
                Comment_data.append(data)
    except Exception as e:
        print("Error retrieving comments:", e)
    return Comment_data

def get_playlist_details(youtube, channel_id):
    next_page_token = None
    All_data = []
    while True:
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            data = {
                'Playlist_Id': item['id'],
                'Title': item['snippet']['title'],
                'Channel_Id': item['snippet']['channelId'],
                'Channel_Name': item['snippet']['channelTitle'],
                'PublishedAt': item['snippet']['publishedAt'],
                'Video_count': item['contentDetails']['itemCount']
            }
            All_data.append(data)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return All_data

def main():
    st.title(":red[YOUTUBE HARVESTING AND WAREHOUSING]")
    st.header("DATA COLLECTION")
    st.write("This Data collection zone can collect data by using channel id  and gives all the channel details,playlist details,comment details and video details")

                       
    youtube = Api_connect()

    channel_id_input_placeholder = 'channel_id_input'
    channel_id = st.text_input('Enter the Channel ID', key=channel_id_input_placeholder)

    if st.button("GET DETAILS"):
                            playlist = get_playlist_details(youtube,channel_id)
                            Video_data = get_video_ids(youtube,channel_id)
                            comment = get_comment_Details(youtube,Video_data)
                            video1 = get_Video_Details(youtube,Video_data)
                            channel_data = get_channel_info(youtube, channel_id)

                            st.subheader("Channel Details")
                            st.write(pd.DataFrame(channel_data))

                            st.subheader("Video Details")
                            st.write(pd.DataFrame(video1))

                            st.subheader("Comment Details")
                            st.write(pd.DataFrame(comment))

                            st.subheader("Playlist Details")
                            st.write(pd.DataFrame(playlist))

if __name__ == "__main__":
    main()

import mysql.connector


# MySQL connection configuration
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "Your PASSWORD"
mysql_database = "YOUR DATABASE"
mysql_port = "YOUR PORT"

# Function to connect to MySQL database
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            port=mysql_port
        )
        print("Connected to MySQL database successfully")
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

# Function to create tables in MySQL
def create_tables(conn):
    cursor = conn.cursor()

    # Table creation queries
    channel_table_query = """
    CREATE TABLE IF NOT EXISTS channel_data (
        Channel_Name VARCHAR(255),
        Channel_Id VARCHAR(255),
        Subscribers INT,
        Views INT,
        Total_videos INT,
        Channel_description TEXT,
        Playlist_Id VARCHAR(255)
    )
    """
    video_table_query = """
    CREATE TABLE IF NOT EXISTS video_data (
        Channel_Name VARCHAR(255),
        Channel_Id VARCHAR(255),
        Video_Id VARCHAR(255),
        Title VARCHAR(255),
        Tags TEXT,
        Thumbnail TEXT,
        Description TEXT,
        Publishdate DATETIME,
        Duration VARCHAR(255),
        Views INT,
        Likes INT,
        Comments INT,
        Favorite_count INT,
        Definition VARCHAR(255),
        Caption_Status VARCHAR(255)
    )
    """
    comment_table_query = """
    CREATE TABLE IF NOT EXISTS comment_data (
        Comment_id VARCHAR(255),
        Video_id VARCHAR(255),
        Comment_text TEXT,
        Comment_Author VARCHAR(255),
        Comment_Published DATETIME
    )
    """
    playlist_table_query = """
    CREATE TABLE IF NOT EXISTS playlist_data (
        Playlist_Id VARCHAR(255),
        Title VARCHAR(255),
        Channel_Id VARCHAR(255),
        Channel_Name VARCHAR(255),
        PublishedAt DATETIME,
        Video_count INT
    )
    """

    try:
        # Execute table creation queries
        cursor.execute(channel_table_query)
        cursor.execute(video_table_query)
        cursor.execute(comment_table_query)
        cursor.execute(playlist_table_query)

        conn.commit()
        print("Tables created successfully in MySQL")
    except mysql.connector.Error as e:
        print("Error creating tables in MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

# Test the functions
conn = connect_to_mysql()
if conn is not None:
    create_tables(conn)
    conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR PASSWORD",
    database="YOUR DATABASE",
    port="YOUR PORT"
)



# Function to insert channel details into MySQL database
def insert_channel_info_to_mysql(conn, channel_info):
    cursor = conn.cursor()
    try:
        for info in channel_info:
            
            insert_query = """
            INSERT INTO channel_data (Channel_Name, Channel_Id, Subscribers, Views, Total_videos, Channel_description, Playlist_Id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the channel_info list
            cursor.execute(insert_query, (info["Channel_Name"], info["Channel_Id"], info["Subscribers"], info["Views"], info["Total_videos"], info["Channel_description"], info["Playlist_Id"]))
        
        conn.commit()
        print("Channel info inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting channel info into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

import mysql.connector

# Function to insert video data into MySQL database
def insert_video_data_to_mysql(conn, video_data):
    cursor = conn.cursor()
    try:
        for data in video_data:
            tags = data.get('Tags', [])
            if not isinstance(tags, list):
                tags = [tags]  
            tags = [tag for tag in tags if tag is not None]
            insert_query = """
            INSERT INTO Video_data (Channel_Name, Channel_Id, Video_Id, Title, Tags, Thumbnail, Description, Publishdate, Duration, Views, Likes, Comments, Favorite_count, Definition, Caption_Status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the video_data list
            cursor.execute(insert_query, (
                data['Channel_Name'],
                data['channel_Id'],
                data['Video_Id'],
                data['Title'],
                ",".join(tags),  
                data['Thumbnail'],
                data.get('Description', ''),
                data['Publishdate'],
                data['Duration'],
                data['Views'],
                data.get('Likes', 0),  
                data.get('Comments', 0),  
                data.get('Favorite_count', 0),  
                data['Definition'],
                data['Caption_Status']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Video data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting video data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()



import mysql.connector

# Function to insert comment data into MySQL database
def insert_comment_data_to_mysql(conn, comment_data):
    cursor = conn.cursor()
    try:
        for data in comment_data:
            insert_query = """
            INSERT INTO comment_data (Comment_id, Video_id, Comment_text, Comment_Author, Comment_Published) 
            VALUES (%s, %s, %s, %s, %s)
            """
            # Execute the query with data from the comment_data list
            cursor.execute(insert_query, (
                data['Comment_id'],
                data['Video_id'],
                data['Comment_text'],
                data['Comment_Author'],
                data['Comment_Published']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Comment data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting comment data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()



import mysql.connector
import datetime  

# Function to insert playlist data into MySQL database
def insert_playlist_data_to_mysql(conn, playlist_data):
    cursor = conn.cursor()
    try:
        for data in playlist_data:
            insert_query = """
            INSERT INTO playlist_data (Playlist_Id, Title, Channel_Id, Channel_Name, PublishedAt, Video_count) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the playlist_data list
            cursor.execute(insert_query, (
                data['Playlist_Id'],
                data['Title'],
                data['Channel_Id'],
                data['Channel_Name'],
                data['PublishedAt'],
                data['Video_count']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Playlist data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting playlist data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()


def main():
    st.title(":red[MIGRATION TO MYSQL]")

    # Connect to YouTube API
    youtube = Api_connect()

    channel_id = st.text_input('Enter the Channel ID')

    # Button to trigger data retrieval and migration to MySQL
    if st.button("Migrate Data"):
        # Retrieving data from YouTube API
        playlist_data = get_playlist_details(youtube, channel_id)
        Video_data = get_video_ids(youtube,channel_id)
        comment_data = get_comment_Details(youtube, Video_data)
        video2 = get_Video_Details(youtube,Video_data)
        channel_data = get_channel_info(youtube, channel_id)
        
        

        # Establishing connection to MySQL database
        conn = connect_to_mysql()

        # Creating tables if they don't exist
        if conn is not None:
            create_tables(conn)

            # Inserting data into MySQL tables
            insert_channel_info_to_mysql(conn, channel_data)
            insert_video_data_to_mysql(conn, video2)
            insert_comment_data_to_mysql(conn, comment_data)
            insert_playlist_data_to_mysql(conn, playlist_data)

            # Closing the MySQL connection
            conn.close()

            # Displaying success message
            st.success("Data migrated to MySQL successfully!")

# Run the main function
if __name__ == "__main__":
    main()

with st.sidebar:
    st.header("*Domain*")
    st.markdown("- Social Media\n")
    st.header("*Skills From This Project*")
    st.markdown("- Python scripting\n- Data Collection\n- Streamlit\n- API Intergration\n- Sql ")
    st.header("*About Project*") 
    st.markdown("- Building a simple UI with streamlit, retrieving data from youtube API,migrating to a Sql data warehouse, querying the data warehouse with Sql, and displaying the data in streamlit app")

# Queris and result
import plotly.express as px

def execute_query(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Luxpapa@09",
        database="pro",
        port="3306"
    )
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    mydb.close()
    return data

st.title(":red[QUERIES AND RESULTS]")
question = st.selectbox("Select Your Question To Display The Query",
                        ("1.What are the names of all the videos and their corresponding channels?",
                        "2.Which channels have the most number of videos, and how many videos do they have?",
                        "3.What are the top 10 most viewed videos and their respective channels?",
                        "4.How many comments were made on each video, and what are their corresponding video names?",
                        "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                        "6.What is the total number of likes for each video, and what are their corresponding video names?",
                        "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                        "8.What are the names of all the channels that have published videos in the year 2022?",
                        "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                        "10.Which videos have the highest number of comments, and what are their corresponding channel names?"),
                        )

if question == "1.What are the names of all the videos and their corresponding channels?":
     query = """
        SELECT c.Channel_Name, v.Title 
        FROM channel_data AS c 
        JOIN video_data AS v 
        ON c.Channel_Id = v.Channel_Id;
    """
     result = execute_query(query)
     df = pd.DataFrame(result, columns=["Channel_Name","Title"])
     st.write(df)

elif question == "2.Which channels have the most number of videos, and how many videos do they have?":
        query = """
            SELECT Channel_Name, Total_videos 
            FROM channel_data
            ORDER BY Total_videos DESC;
        """
        result = execute_query(query)
        df1 = pd.DataFrame(result, columns=["Channel_Name", "Total_videos"])
        st.write(df1)

        fig = px.bar(df1, x='Channel_Name', y='Total_videos', title='Channels with Most Videos',
                 labels={'Total_videos': 'Number of Videos', 'Channel_Name': 'Channel'})

    # Update layout
        fig.update_layout(xaxis_title='Channel', yaxis_title='Number of Videos')

        # Display the chart using Streamlit
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "3.What are the top 10 most viewed videos and their respective channels?":
        query = """
                select Channel_Name,Title,Views from video_data
                order by Views desc limit 10;
                """
        result = execute_query(query)
        df2 = pd.DataFrame(result, columns=["Channel_Name", "Title","Views"])
        st.write(df2)

        fig = px.bar(df2, x='Channel_Name', y='Views', text='Title', title='Top 10 Most Viewed Videos by Channel')
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Views')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "4.How many comments were made on each video, and what are their corresponding video names?" :
        query = """
                Select c.Channel_Name, v.comments,v.Title from channel_data as c join video_data as v on c.Channel_ID=v.Channel_ID;
                """
        result = execute_query(query)
        df3 = pd.DataFrame(result, columns=["Channel_Name", "Comments","Title"])
        st.write(df3)

        fig = px.bar(df3, x='Title', y='Comments', color='Channel_Name', title='Number of Comments on Each Video')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Number of Comments', legend_title='Channel Name')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "5.Which videos have the highest number of likes, and what are their corresponding channel names?" :
        query = """
                select c.Channel_Name,v.Title,v.Likes from channel_data as c join video_data as v on c.Channel_ID=v.Channel_ID
                order by v.Likes desc;
                """
        result = execute_query(query)
        df4 = pd.DataFrame(result, columns=["Channel_Name", "Title","Likes"])
        st.write(df4)

        fig = px.bar(df4, x='Title', y='Likes', color='Channel_Name', title='Number of Likes on Each Video')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Number of Likes', legend_title='Channel Name')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "6.What is the total number of likes for each video, and what are their corresponding video names?" :
        query = """
                SELECT Title, SUM(Likes) AS Total_Likes
                FROM video_data
                GROUP BY Title
                ORDER BY Total_Likes DESC;
                """
        result = execute_query(query)
        df5 = pd.DataFrame(result, columns=[ "Title","Likes"])
        st.write(df5)

        fig = px.bar(df5, x='Title', y='Likes', title='Total Number of Likes for Each Video')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Total Number of Likes')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "7.What is the total number of views for each channel, and what are their corresponding channel names?" :
        query = """
                select Channel_Name,views from channel_data order by views desc;
                """
        result = execute_query(query)
        df6 = pd.DataFrame(result, columns=[ "Channel_Name","views"])
        st.write(df6)

        fig = px.bar(df6, x='Channel_Name', y='views', title='Total Number of Views for Each Channel')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Total Number of Views')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "8.What are the names of all the channels that have published videos in the year 2022?" :
        query = """
                select Channel_Name from video_data
                where EXTRACT(YEAR FROM Publishdate) = 2022;
                """
        result = execute_query(query)
        df7 = pd.DataFrame(result, columns=[ "Channel_Name"])
        st.write(df7)

        fig = px.histogram(df7, x='Channel_Name', title='Channels that Published Videos in 2022')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Frequency')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?" :
        query = """
                SELECT c.Channel_Name, AVG(v.Duration) AS Avg_Duration
                FROM channel_data c
                JOIN video_data v ON c.Channel_Id = v.Channel_Id
                GROUP BY c.Channel_Name;
                """
        result = execute_query(query)
        df8 = pd.DataFrame(result, columns=[ "Channel_Name","Avg_Duration"])
        st.write(df8)

        fig = px.bar(df8, x='Channel_Name', y='Avg_Duration', title='Average Duration of Videos in Each Channel')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Average Duration')
        st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "10.Which videos have the highest number of comments, and what are their corresponding channel names?" :
        query = """
                SELECT c.Channel_Name, v.Title, COUNT(co.Comment_Id) AS Num_Comments
                FROM channel_data c
                JOIN video_data v ON c.Channel_Id = v.Channel_Id
                LEFT JOIN comment_data co ON v.Video_Id = co.Video_Id
                GROUP BY c.Channel_Name, v.Title
                ORDER BY Num_Comments DESC
                LIMIT 10;
                """
        result = execute_query(query)
        df9 = pd.DataFrame(result, columns=[ "Channel_Name","Title","Num_Comments"])
        st.write(df9)

        fig = px.bar(df9, x='Title', y='Num_Comments', color='Channel_Name', title='Videos with the Highest Number of Comments')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Number of Comments', legend_title='Channel Name')
        st.write("Visualization:")
        st.plotly_chart(fig)