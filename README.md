# YOUTUBE HARVESTING AND WAREHOUSING
## DOMAIN:
Social Media
## PROBLEM STATEMENT :
YouTube Data Harvesting and Warehousing is a project that aims to allow users to access and analyze data from multiple YouTube channels. The project utilizes SQL and Streamlit to create a user-friendly application that allows users to retrieve, store, and query YouTube channel and video data
## TOOLS:
-Python Scripting

-API Integration

-Data Collection

-Data Management using SQL

# ABOUT PROJECT
## 1.Set up a Streamlit app:
Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
## 2.Connect to the YouTube API:
You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
## 3.Store and Clean data : 
Once you retrieve the data from the YouTube API, store it in a suitable format for temporary storage before migrating to the data warehouse. You can use pandas DataFrames or other in-memory data structures.
## 4.Migrate data to a SQL data warehouse:
 After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
## 5.Query the SQL data warehouse: 
You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
## 6.Display data in the Streamlit app: 
Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.


