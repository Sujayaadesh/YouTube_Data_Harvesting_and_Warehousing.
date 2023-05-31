# -- Youtube libraries
import googleapiclient.discovery
from googleapiclient.errors import HttpError

# -- Streamlit
import streamlit as st

# -- MongoDB
from pymongo import MongoClient

# -- SQL library
import mysql.connector

# -- Pandas
import pandas as pd

from datetime import datetime

#=======================================================================================

#Data Collection Zone 

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyBFdwlrEMOxhIZc3Deb7a2Ms-_xTro0rns"

youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

client = MongoClient("mongodb+srv://Saisujay:Saiappa@cluster0.2knmid1.mongodb.net/?retryWrites=true&w=majority")
db = client["Saiappa"]
collection = db["Youtube_extraction"]


db_connection = mysql.connector.connect(
     host='127.0.0.1',
     user='root',
     password='Saiappa34@',
     database='Saiproject1')
cursor = db_connection.cursor()

# =================================================================================

# Define a function to retrieve Channel Data 
def get_channel_details(channel_id):       #getting channel details 
    finall = []
    request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        id = channel_id
        # snippet -- information or news 
        )
    response = request.execute()
    for item in response["items"]:
        initial_data ={"channelName"                 :item['snippet']['title'],
                           "channel_id"              : item ["id"],
                           "subscriberCount"         :item['statistics']['subscriberCount'],
                           "videoCount"              : item['statistics']['videoCount'],
                           "Channel_views"           : item['statistics']['viewCount'],
                           "Channel_discription"     : item['snippet']['description'],
                           "playlist_id"             : item['contentDetails']['relatedPlaylists']['uploads']}
                        
        finall.append(initial_data)
        
        
    return initial_data 

# Define a function to retrieve playlist data using channel_id
def get_playlists_details(channel_id):
    playlist_data=[]
    response = youtube.playlists().list(part="snippet", channelId=channel_id,maxResults=5).execute()
    for item in response["items"]:
        playlist_data.append({"Channel_id"   : item["snippet"]["channelId"],
                              "playlist_id"  :item["id"], 
                              "Playlist_Name": item ["snippet"]["title"] })
          
    return playlist_data

# Fuction to retrieve only the playlist_id
def get_playlists(channel_id):
    playlist_data=[]
    response = youtube.playlists().list(part="snippet", channelId=channel_id,maxResults=5).execute()
    for item in response["items"]:
        playlist_data.append(item["id"])     
    return playlist_data

# Define a function to retrieve video_ids
def get_playlist_items(playlist_id):
    video_ids = []
    playlist_items_response = youtube.playlistItems().list(part="contentDetails", playlistId=playlist_id,maxResults=5).execute()
    for item in playlist_items_response["items"]:
            data = item["contentDetails"]["videoId"]
            video_ids.append(data)
    return video_ids 
    #-------------------------------------------------------------------------------------
#-Getting all the video_ids behind the maximum limit
    # for item in playlist_items_response["items"]:
    #     video_ids.append(item["contentDetails"]["videoId"])
        
    # next_page_token = response.get("nextPageToken") 
    # more_pages = True 
    # while more_pages:
    #     if next_page_token is None:
    #         more_pages = False
    # else:
    #     request = youtube.playlistItems().list(
    #         part = "contentDetails" ,
    #         playlistId = playlist_id,
    #         maxResults = 50,
    #         pageToken=next_page_token)        
    #     response = request.execute()
    #     for item in response["items"]:
    #         video_ids.append(item["contentDetails"]["videoId"])
    #         next_page_token = response.get("nextPageToken")
    # return video_ids
    #-------------------------------------------------------------------------------------------



# Define a function to retrieve video_data 
def get_video_detalis(video_ids,playlist_id,all_comments):
    vd = []
    #----- for limited videoids
    # request = youtube.videos().list(
    #     part = "contentDetails,snippet,statistics" ,
    #     id = ',' .join(m)
    #     maxResults = 50)  
    # response = request.execute()
    
    for i in range(0,len(video_ids),50):
        request = youtube.videos().list(
            part = "contentDetails,snippet,statistics" ,
            id = ',' .join(video_ids[i:i+50]))  #for first iteration it will 0 untill 50 it will fetch(slicing)

        response = request.execute()
    
        for i in response["items"]:
            vdo_id = i["id"]
            vdo_cmts = []
            for c in all_comments:
                if(c["video_id"] == vdo_id):
                    vdo_cmts.append(c)
            vd.append({"playlist_id"         : playlist_id,
                       "Video_id"            : i["id"],
                       "Video_name"          : i["snippet"]["title"],
                       "Video_descripition"  : i["snippet"]["description"],
                       "Tags"                : i["snippet"].get("tags", []),
                       "publish_date"        : i["snippet"]["publishedAt"],
                       "View_count"          : i["statistics"]["viewCount"],
                       "like_counts"         : i["statistics"]["likeCount"],
                       "favoriteCount"       : i["statistics"]["favoriteCount"],
                       "commentCount"        : i["statistics"]["commentCount"],
                       "video_duration"      : i["contentDetails"]["duration"],
                       "video_Caption_Status": i["contentDetails"].get("caption", 0),
                       "thumbnail"           : i["snippet"]["thumbnails"].get('default', {}).get('url', 'Thumbnail Not Available'),
                       "comment"             : vdo_cmts})
                                                       
            
                       #The statistics.dislikeCount property was made private as of December 13, 2021. This means that the property is included in an API response only if the API request was authenticated by the video owner. See the revision history for more information
                 
    return vd

# Define function to retrieve comment data 
def get_comments(video_id):
            
            comment=[]
            while True:
                try:
                    response = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        order = 'relevance',
                        maxResults=5 #----- Adjust as needed, maximum is 100       
                    ).execute()
                        
                    for i in response['items']:
                        comment.append({"Comment_id"       : i["id"],
                                        "Commente_author"  : i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                        "video_id"         : i["snippet"]["videoId"],
                                        "Comment_text"     : i['snippet']['topLevelComment']['snippet']['textDisplay'],
                                        "Comment_published": i['snippet']['topLevelComment']['snippet']['publishedAt']})
                except HttpError as e:
                    error_response = e.content.decode("utf-8")
                    if 'Disabled' or 'videoNotFound' in error_response:
                       continue
                    else:
                      raise e
                return comment 
#---------------------------------------------------------------------------           
# ------getting all the comments behind the maxmimum limit
# '''     while True:
#         try:
#             comment_response = youtube.commentThreads().list(
#                 videoId=video_id_only,
#                 part='snippet',
#                 pageToken=next_page_token
#             ).execute()

#             for item in comment_response['items']:
#                 comment = {
#                     'comment_id': item['id'],
#                     'video_id': item['snippet']['videoId'],
#                     'comment_text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
#                     'comment_author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
#                     'comment_published': item['snippet']['topLevelComment']['snippet']['publishedAt']
#                 }
#                 comments.append(comment)

#             next_page_token = comment_response.get('nextPageToken')

#             if next_page_token is None:
#                 break
#         except HttpError as e:
#             error_response = e.content.decode("utf-8")
#             if 'Disabled' in error_response:
#                 continue
#             else:
#                 raise e'''
#---------------------------------------------------------------------------  
           
#========================================================================

# Define fuction to push the extracted data to the Mongodb
def push_to_mongo(data):
    collection.insert_one(data)
    st.success("data_extracted to :violet[Mongo]")

#========================================================================
# Function to convert the duration of the videos to Seconds
def convert_duration(duration_str):  #PT15M51S
    duration_str = duration_str[2:]  # Remove 'PT' prefix
    hours = 0
    minutes = 0
    seconds = 0
    if 'H' in duration_str:
        hours, duration_str = duration_str.split('H') #------split upto h 
    if 'M' in duration_str:
        minutes, duration_str = duration_str.split('M') #----------split upto M(15 51S) 
    if 'S' in duration_str:
        seconds = duration_str.replace('S', '')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds


# Define Fuction to Migrate data to MySql tables
def sql(data):
    for key, value in data.items():
        if key == "channel_details":
            query = "INSERT INTO channels1 (channel_id, title, subscribers, video_count, total_views, playlist_id) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (value['channel_id'], value['channelName'], value['subscriberCount'], value['videoCount'], value['Channel_views'], value['playlist_id'])
            try:
                cursor.execute(query, values)
            except mysql.connector.IntegrityError:
                continue
            
        elif key == "playlist_details":  # Remove the extra space here
            for playlist in value:
                query = "INSERT INTO playlist1 (channel_id, playlist_id, Playlist_Name) VALUES (%s, %s, %s)"
                values = (playlist['Channel_id'], playlist['playlist_id'], playlist['Playlist_Name'])
                try:
                    cursor.execute(query, values)
                except mysql.connector.IntegrityError:
                    continue
        elif key == "video_detials":
            for video in value:
                publish_date_str = video['publish_date']
                publish_date = datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')# converts the string publish_date_str to a datetime object using the strptime()
                video['publish_date'] = publish_date.strftime('%Y-%m-%d %H:%M:%S')  #
                video_duration_str = video['video_duration']
                video_duration = convert_duration(video_duration_str)
                video['video_duration'] = video_duration  #
                query = "INSERT INTO video_details (playlist_id, Video_id, Video_name, Video_description, publish_date , View_count, like_counts, favoriteCount,commentCount, video_duration,  thumbnail, video_Caption_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (video['playlist_id'], video['Video_id'], video['Video_name'], video['Video_descripition'], video['publish_date'], video['View_count'], 
					   video['like_counts'], video['favoriteCount'], video['commentCount'], video['video_duration'],  video['thumbnail'],video['video_Caption_Status'])                
                try:
                    cursor.execute(query, values)
                except mysql.connector.IntegrityError:
                    continue
                for comment in video['comment']:
                    publish_date_str_cmt = comment['Comment_published']
                    publish_date_1 = datetime.strptime(publish_date_str_cmt, '%Y-%m-%dT%H:%M:%SZ')# converts the string publish_date_str to a datetime object using the strptime()
                    comment['Comment_published'] = publish_date_1.strftime('%Y-%m-%d %H:%M:%S')
                    query = "INSERT INTO comment_details (Comment_id, video_id, Comment_text,Comment_author, Comment_published) VALUES (%s, %s, %s, %s, %s)"
                    values = (comment['Comment_id'], comment['video_id'], comment['Comment_text'], comment['Commente_author'], comment['Comment_published'])
                    try:
                        cursor.execute(query, values)
                    except mysql.connector.IntegrityError:
                        continue

    db_connection.commit()

def execute_query(query):
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=columns)
    return df
#=================================================================


# MAin Function  
def main():
    st.balloons()
    st.title("Youtube Data :orange[Harvesting] And :green[Warehousing]")
    st.header(":blue[Data Collection]")   
    channel_id = st.text_input("Enter the Channel id") #channe_id as input
    if st.button("**Extract Data and Store in Mongo**"): #button for extracting
            channel_details = get_channel_details(channel_id)
            playlist_details = get_playlists_details(channel_id)
            play_list = get_playlists(channel_id)
            all_comments=[]
            all_video_details = []
            for playlist_id in play_list:
                video_ids = get_playlist_items(playlist_id)
                for video_id in video_ids :
                     comments = get_comments(video_id)
                     all_comments.extend(comments)
                playlist_video_details = get_video_detalis(video_ids,playlist_id,all_comments)
                #if playlist_video_details is not None:
                all_video_details.extend(playlist_video_details)
# ----------- Merging all those details in the singe documents using dictionary                 
            details = {"channel_details"  : channel_details,
                       "playlist_details" : playlist_details,
                       "video_detials" : all_video_details}
            push_to_mongo(details)  
#====================================================================================== 
    #getting all channel extracted channel names in MongoDB
    st.header(":blue[Migration]") 
    doc_name = []
    for doc in collection.find():
        doc_name.append(doc["channel_details"]["channelName"])
    Channel_names = st.selectbox("Select Channel name",options = doc_name, key = doc_name)
    st.write("*****Migrate data to MySQL from MongoDB*****")
    if st.button("Migrate to MySQL"):
        st.success("data_extracted to :green[MySQL]")
    if Channel_names:
        Channel_NAme = {"channel_details.channelName" : Channel_names}
        data = collection.find_one(Channel_NAme)
        sql(data)



# -------------- Queries that read data in the Mysql and display those data in streamlit(table_formate)
    st.header(":blue[Channel Data Analysis]")
    if st.button(":orange[Names of all videos :video_camera: and their corresponding channels]"):
        query1 = "select Video_name , title from video_details s1 join channels1 s2 join playlist1 s3 on s1.playlist_id = s3.playlist_id and s3.channel_id = s2.channel_id"
        df1 = execute_query(query1)
        st.table(df1)

    #SQL Query 2: Channels with the most number of videos and their count
    if st.button(":green[Channels with the most number of videos]"):
        query2 = "SELECT title AS Channel, COUNT(*) AS Video_Count FROM channels1 s2 INNER JOIN video_details join playlist1 s3  ON s3.playlist_id = video_details.playlist_id and s3.channel_id = s2.channel_id GROUP BY title ORDER BY Video_Count DESC"
        df2 = execute_query(query2)
        st.table(df2)

    #  SQL Query 3: Top 10 most viewed videos and their respective channels
    if st.button(":red[Top 10 most viewed videos :sparkler: and their respective channels] :"):
        query3 = "select Video_name, title AS Channel, View_count FROM video_details INNER JOIN channels1 s2 join playlist1 s3 ON video_details.playlist_id = s3.playlist_id and s3.channel_id = s2.channel_id ORDER BY View_count DESC LIMIT 10"    #     
        df3 = execute_query(query3)
        st.table(df3)

    #SQL Query 4: Number of comments on each video and their corresponding video names
    if st.button(":orange[Number of comments :inbox_tray: on each video]"):
        query4 = "select Video_name,count(*) as comment_count from video_details s1 join comment_details s2 on s1.Video_id = s2.video_id group by Video_name"       
        df4 = execute_query(query4)
        st.table(df4)

    #Actuall comments for all videos
    if st.button(":green[Additional : Total Number of comments :inbox_tray: on each video]"):
        query_additional = "select Video_name,commentCount from video_details"       
        df4 = execute_query(query_additional)
        st.table(df4)


     # SQL Query 5: Videos with the highest number of likes and their corresponding channel names
    if st.button(":red[Videos with the highest number of likes :fireworks: :green_heart:]"):
        query5 = "select Video_name,title as channel_name ,like_counts from video_details s1 join channels1 s2 join playlist1 s3 on  s1.playlist_id = s3.playlist_id and s3.channel_id = s2.channel_id order by like_counts desc"
        df5 = execute_query(query5)
        st.table(df5)

    if st.button(":orange[Total number of likes :thumbsup: and their corresponding video names]"):
        query6 = "SELECT Video_name, SUM(like_counts) AS Total_Likes FROM video_details GROUP BY Video_name"
        df6 = execute_query(query6)
        st.table(df6)

    if st.button(":green[Total number of views for each channel :eyes: and  their corresponding channel names]"):
        query7 = "SELECT title AS Channel_Name, SUM(total_views) AS Total_Views FROM channels1 GROUP BY title"
        df7 = execute_query(query7)
        st.table(df7)

    if st.button(":red[Names of all the channels that have published videos in the year 2022 :date:]" ):
        query8 = "select distinct title as channel_name from video_details s1 join channels1 s2 join playlist1 s3 on s1.playlist_id = s3.playlist_id and s3.channel_id = s2.channel_id where publish_date like '2022%'"
        df8 = execute_query(query8)
        st.table(df8)
    
    if st.button(":orange[Average duration :clock9: of all videos in each channel and their corresponding channel names]"):
        query9= "select  title as channel_name , avg(video_duration) as Averade_duration  from video_details s1 join channels1 s2 join playlist1 s3 on s1.playlist_id = s3.playlist_id and s3.channel_id = s2.channel_id group by title"
        df9 = execute_query(query9)
        st.table(df9)
    if st.button(":green[videos having highest number of comments and their corresponding channel names]"):
        query10 = "select title as Channel_name,Video_name,commentCount from video_details s1 join channels1 s2 join playlist1 s3 on s1.playlist_id = s3.playlist_id and s3.channel_id = s2.channel_id ORDER BY commentCount DESC limit 10"
        df10 = execute_query(query10)
        st.table(df10)

    
        
if __name__ == "__main__":
    main()