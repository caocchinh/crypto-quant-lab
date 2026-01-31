import requests
from requests_oauthlib import OAuth1

# Define your consumer key, consumer secret, access token, and access token secret
access_token = "1701493264250281984-uWXdVSGC5Ota5jr4wRjXvlxlLHj4Ib"
access_token_secret = "LvLBG9YUtN8I6IImA6ul9cNWVDskcuxYObSbe2sMsx8PZ"

consumer_key = "iGXcukMaPx8UKjLvMp7nPFluU"
consumer_secret = "HZXI9CjayFyJabip09XkOb7BTWANAPOnI39gRNdqVPJoweYTEX"

# Create an OAuth1 session
auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

# Define the tweet text and the ID of the tweet you are replying to
tweet_text = "Hello! This is a reply to your tweet with an image."
in_reply_to_tweet_id = '1234567890123456789'  # Replace with the ID of the tweet you are replying to

# Upload image as media
image_path = r'C:\Users\lenovo\OneDrive\Bitcoin\Twitter\GIuCYBCXQAAjZKB.jpg'  # Replace with the path to your image file
image_file = open(image_path, 'rb')
media_data = {
    'media': image_file
}
media_response = requests.post('https://upload.twitter.com/1.1/media/upload.json', auth=auth, files=media_data)

if media_response.status_code == 200:
    media_id = media_response.json()['media_id']
    print(media_id)

    # Define the tweet data with the reply text, in_reply_to_tweet_id, and media_id
    tweet_data = {
        'text': tweet_text,
        "reply": {"in_reply_to_tweet_id": in_reply_to_tweet_id},
        "media": {"media_ids": [media_id]}
    }

    # Make a POST request to the Twitter API endpoint for posting a tweet
    response = requests.post('https://api.twitter.com/2/tweets', auth=auth, json=tweet_data)

    # Check the response status
    if response.status_code == 201:
        print("Reply with image posted successfully!")
    else:
        print("Failed to post reply with image. Status code:", response.status_code)
        print("Error message:", response.text)
else:
    print("Failed to upload image as media. Status code:", media_response.status_code)
    print("Error message:", media_response.text)

# Close the image file
image_file.close()
