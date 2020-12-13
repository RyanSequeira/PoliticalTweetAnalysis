from popularity_predictor import load_list
import os


with open("crisis_analysis.txt", "w+") as output:
    '''
    Prompts the user to label the top 10 tweets of each Tweet sample as independent (0) or corporate (1) and rising 
    (0, < 100k followers) or established (1, > 100k followers). Writes to crisis_analysis.txt
    '''
    # Used to hold top ten tweets for each iteration
    top_ten = []

    # counts[0] - total tweets analyzed, counts[1] - # corporate, counts[2] - # established
    counts = []
    names = {}

    # Iterates through all Crises Tweet files
    for i in os.listdir("data/Crises"):
        tweets = load_list("data/Crises/" + i)

        # local # corporate and # established
        fileCount = []

        # skip all files with < 10 tweets
        if len(tweets) < 10:
            continue

        print("----------------------" + str(i) + "----------------------------")

        # Iterate through Tweets
        for j in tweets:

            # If retweet, assign retweet_status to tweet, else assign tweet_status to tweet
            if 'retweeted_status' in j.keys():
                tweet = j['retweeted_status']
            else:
                tweet = j

            # If current tweet is a duplicate, skip
            duplicate = False

            # If the current tweet analyzed is already added to top_ten, skip it (probably a retweet)
            for k in top_ten:
                if k['id'] == tweet['id']:
                    duplicate = True
            if duplicate:
                continue

            # Add tweet to top_ten and sort ascending
            top_ten.append(tweet)
            top_ten = sorted(top_ten, key=lambda tweetMember: tweetMember['favorite_count'])

            # Keep top ten tweets if more than ten tweets reached (drop 11th tweet - smallest no. favorites)
            if len(top_ten) > 10:
                top_ten = top_ten[1:]

        # Skip current iteration on empty top ten list
        if len(top_ten) == 0:
            continue

        # Iterate through top_ten list and query user to assign a support and popularity number
        for top in top_ten:
            if top['user']['screen_name'] in names:
                fileCount.append(names[top['user']['screen_name']])
            elif int(top['user']['followers_count']) < 50000:
                names[top['user']['screen_name']] = (0, 0)
                fileCount.append((0, 0))
            else:
                print("\nname: " + str(top['user']['screen_name']))
                print("Followers: " + str(top['user']['followers_count']))
                print("Description " + str(top['user']['description']))
                print("Favorites " + str(top['favorite_count']))
                print("ID " + str(top['id']))
                response = input("Enter [Backing] [Prescence]: ")
                fileCount.append((int(response[0]), int(response[2])))
                names[top['user']['screen_name']] = (int(response[0]), int(response[2]))

        # Write file name and list of counts
        output.write(i + ", " + str(fileCount) + "\n")
        counts.extend(fileCount)
        top_ten = []
        print("----------------------" + str(counts) + "-----------------------------")

    # Output results of each applicable file (> 10 tweets) and classification breakdown to a text file
    with open("crisis_analysis_total.txt", 'w+') as total:
        total.write(str(counts))


