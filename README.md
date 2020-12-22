# PoliticalTweetAnalysis
This project is my final project for Georgia Tech's CS 2803: Social Media Data Analytics. It analyzes the characteristics of popular Tweets as well as the types of individuals originating them.


## Instructions
#### Acquiring Tweets
Two files are used to gather tweets to perform analysis on: *sweep.py* and *PermanentSweep.py*. Utilize *sweep.py* for Crises topics and *PermanentSweep.py* for Permanent topics. Each file will aggregate tweets in the past 7 days pertaining to the inputted topic. For best results, topics should appear as strings separated by spaces and "OR" (e.g "Gun control OR guns OR second amendment"). Additionally, to use either file, the code must be edited to include Twitter API keys as marked. Once each respective file is run and the topic string is inputted, the program will deposit collected Tweets as a text file to data/Permanent or data/Crises, depending on the program used.
#### Assigning Tweets Classifications
In order to proceed with analysis of Crises topics, all crises Tweets must be manually assigned labels designating backing (independent/corporate) and presence(less/greater than 100k follower). Run *analysis.py*, which will prompt you to assign labels to all Crises tweets in the following format: "[backing] [presence]" (e.g "0 1"). Backing is present as 0 for independent and 1 for corporate-backed, while Presence assigns 0 to users with less than 100k followers and 1 to users with more than 100k followers (with exceptions at user discretion). 
#### Analysis
Follow along the Jupyter Notebook at *visualization.ipynb* to Analyze the data and create predictions.
