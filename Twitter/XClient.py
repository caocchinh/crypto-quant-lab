import random
import time

import requests
from requests_oauthlib import OAuth1
import pandas as pd

accounts = []

file = pd.read_excel(r"C:\Users\lenovo\OneDrive\Bitcoin\Twitter\Twitter account.xlsx")
for i in file.values[1:]:
    temp = {}
    count = -1
    for x in i:
        count += 1
        if count == 4:
            temp['consumer_key'] = x
        if count == 5:
            temp['consumer_secret'] = x
        if count == 6:
            temp['access_token'] = x
        if count == 7:
            temp['access_token_secret'] = x
    accounts.append(temp)


tweet_ideas = [
    "🚀 To the moon with DOG! 🌕 #crypto #memecoin",
    "Just bought more DOG! Who's with me? 🐶💰 #cryptocurrency",
    "When in doubt, HODL your DOG! 🐕💎 #memecoin",
    "DOGE who? It's all about DOG now! 🚀🌝 #crypto",
    "The DOG community is the best! Let's keep pushing forward! 🐾💪 #cryptotwitter",
    "Retweet if you're a proud DOG holder! 🙌🐶 #memecoin",
    "Watching DOG's price go up like... 📈🚀 #cryptocurrency",
    "In DOG we trust! 🐕💎 #crypto",
    "Just got my DOG memes ready for the next pump! 😂🚀 #memecoin",
    "Who let the DOG out? 🐶🚀 #cryptotwitter",
    "DOG is not just a memecoin, it's a movement! 💪🌕 #crypto",
    "Barking all the way to the bank with DOG! 🐕💰 #memecoin",
    "The DOG community is on fire today! 🔥🚀 #cryptocurrency",
    "New day, new opportunities with DOG! 🌅💎 #crypto",
    "Keep calm and buy more DOG! 🐶💸 #memecoin",
    "DOG holders right now: 💎🙌 #cryptotwitter",
    "The DOG fam is the best fam! Let's keep supporting each other! 🐾💪 #crypto",
    "Just a friendly reminder to HODL your DOG tight! 🐕💎 #memecoin",
    "When life gives you DOG, make gains! 🚀💰 #cryptocurrency",
    "DOG memes never fail to make me laugh! 😂🐶 #crypto",
    "Rise and shine with DOG by your side! 🌞🐕 #memecoin",
    "Who's ready for the next DOG pump? Buckle up! 🚀💎 #cryptotwitter",
    "In DOG we bark! 🐾🚀 #crypto",
    "My DOG bag is packed and ready for liftoff! 🚀🌕 #memecoin",
    "Today's goal: spread the word about DOG to everyone! 🗣💰 #cryptocurrency",
    "DOGE who? It's all about DOG now! 🐶🌝 #crypto",
    "HODLing DOG like my life depends on it! 💎🐕 #memecoin",
    "The DOG community is full of diamond paws! 🐾💎 #cryptotwitter",
    "Just bought the dip on DOG! Time to ride the wave up! 🌊🚀 #crypto",
    "No regrets, only gains with DOG! 💰🐕 #memecoin",
    "DOG is more than a coin, it's a lifestyle! 🚀🌟 #cryptocurrency",
    "Who's up for a DOG meme contest? Let's get creative! 😂🎨 #crypto",
    "Another day, another opportunity to grow our DOG community! 🐶🌱 #memecoin",
    "When in doubt, just remember: DOG has your back! 🐕💎 #cryptotwitter",
    "Let's show the world what the power of DOG can do! 🌎💪 #crypto",
    "My DOG bag is getting heavier by the day, and I love it! 💼🚀 #memecoin",
    "HODL strong, fellow DOG holders! Diamond paws only! 💎🐾 #cryptocurrency",
    "The journey with DOG may have ups and downs, but we're in it together! 📈📉 #crypto",
    "DOGE might have started it all, but DOG is here to stay! 🐶🚀 #memecoin",
    "Every dip is just another opportunity to buy more DOG at a discount! 💰🐕 #cryptotwitter",
    "Who else is obsessed with checking their DOG balance every hour? Guilty as charged! ⏰💸 #crypto",
    "The future is bright for DOG and its amazing community! Let's keep pushing forward! 🔆🐾 #memecoin",
    "When someone asks me about my favorite pet, I tell them it's my DOG wallet! 🐶💼 #cryptocurrency",
    "Just a friendly reminder: never invest more than you're willing to lose, even with a gem like DOG! 💎🚫 #crypto",
    "DOGE, SHIB, what's next? It's all about DOG now! Join the pack! 🐶🌟 #memecoin",
    "Every time I see a DOG meme, I can't help but smile and buy more coins! 😄💰 #cryptotwitter",
    "The DOG community is not just about profits, it's about having fun and supporting each other too! 🎉🤝 #crypto",
    "Who else dreams of waking up to a world where DOG is the top memecoin? Let's make it happen together! 🌍🚀 #memecoin",
    "No matter how high or low the price goes, I'm here for the long run with my beloved DOG coins! 💪💎 #cryptocurrency",
    "Let's spread the word about DOG far and wide so more people can join our awesome community! 🌐🐾 #crypto",
"   Rise and shine with DOG by your side! 🌞🐕💎 #memecoin",
    "It's a DOG-eat-DOGE world out there! 🐶🚀 #cryptotwitter",
    "Who's ready for the DOG party? Let's celebrate those gains! 🎉💰 #crypto",
    "DOGE might have started the trend, but DOG is here to stay! 🐾🌕 #memecoin",
    "Every DOG has its day, and today is DOG's day! 🐕💎 #cryptocurrency",
    "Don't stop believin' in DOG! 🎶🚀 #crypto",
    "Haters gonna hate, but DOG holders gonna HODL! 🐶💪 #memecoin",
    "Just a friendly reminder to spread positivity in the DOG community! 🌟🐾 #cryptotwitter",
    "The only way is up for DOG! Let's keep climbing together! 🧗‍♂️🚀 #crypto",
    "In a world full of uncertainties, I can always count on my DOG investments! 🐕💰 #memecoin",
    "Just joined the DOG fam and already feeling the love! 🐶❤️ #cryptocurrency",
    "Who's excited for the next DOG meme contest? Get your creative juices flowing! 🎨😂 #crypto",
    "When life gets ruff, just remember you have DOG by your side! 🐾🌈 #memecoin",
    "DOGE may have started the journey, but DOG is leading the way to the moon! 🚀🌕 #cryptotwitter",
    "If you're not talking about DOG, then what are you even talking about? 🤷‍♂️🐶 #crypto",
    "The DOG community is not just about gains, it's about supporting each other through thick and thin! 🤝💪 #memecoin",
    "Just checked my DOG wallet and feeling blessed! Thank you, DOG fam! 🙏💎 #cryptocurrency",
    "Let's keep the DOG memes coming! Laughter is the best medicine in this crypto journey! 😆🐕 #crypto",
    "When the going gets tough, the tough buy more DOG! 💪🚀 #memecoin",
    "Who else is proud to be part of the DOG revolution? Let's change the game together! 🌍🐾 #cryptotwitter",
    "🌟 Woof woof! Let's bark our way to financial freedom with DOG! 🚀🐾 #cryptocurrency",
    "🚀🌕 Embrace the volatility, ride the waves, and hold onto your DOG for dear life! 💎🐕 #memecoin",
    "🐶💰 Join the pack, feel the thrill, and watch DOG soar to new heights! 🚀🌈 #crypto",
    "🔥📈 The fire in our hearts burns brighter with every DOG milestone achieved! Let's keep the flame alive! 🔥💪 #cryptotwitter",
    "🚀🐾 Strap in, hold tight, and get ready for the DOG rocket ship to take off! Destination: MOON! 🌕🚀 #crypto",
    "💡💸 Invest in innovation, believe in the power of community, and witness the magic of DOG unfold before your eyes! ✨🐶 #memecoin",
    "🌟🚀 Shine bright like a DOG diamond as we navigate the crypto universe together! 🌌💎 #cryptocurrency",
    "🎉🥳 Celebrate each DOG milestone with joy, unity, and a whole lot of memes! Let's make history together! 🎊😂 #crypto",
    "🌈💰 Ride the rainbow of possibilities with DOG by your side. Let's paint the world with success, one paw print at a time! 🐾🌈 #memecoin",
    "🚀🔥 Ignite your passion for crypto, fuel your dreams with DOG, and let's create a brighter future together! 💫🐶 #cryptotwitter",
    "🔒💎 Lock in your faith, secure your investments, and watch DOG pave the way to financial prosperity! 🚀💰 #crypto",
    "🎨😂 Unleash your creativity, spread laughter through memes, and let DOG be the canvas of our shared imagination! 🐕🖌️ #memecoin",
    "🌕🚀 As the moon beckons, let's howl in unison as DOG leads us to new horizons of success and abundance! 🌝🐾 #cryptocurrency",
    "🌟💫 Let's make DOG not just a token, but a symbol of unity, resilience, and endless possibilities in the crypto world! 🐶🚀 #cryptocurrency",
    "🚀🔥 Fuel your ambition, stoke the flames of success, and let DOG be your guiding light in the vast sea of cryptocurrencies! 💡💰 #memecoin",
    "🐾🌕 Follow the paw prints of DOG to the moon and beyond, where dreams become reality and gains are unlimited! 🚀💎 #crypto",
    "🎉🚀 Join the DOG party and dance to the rhythm of innovation, community spirit, and financial freedom! 🎶🐕 #cryptotwitter",
    "💪🌈 Stand strong with DOG, weather the storms of volatility, and emerge victorious with diamond hands and unwavering belief! 💎🐾 #crypto",
    "🚀🔮 Peer into the future with DOG by your side, where every dip is a chance to buy more and every peak is a reason to celebrate! 💸🐶 #memecoin",
    "🌟🚀 Illuminate the path to success with DOG as your beacon, guiding you through the darkness of uncertainty towards the light of prosperity! 💫🌟 #cryptocurrency",
    "🔒🌕 Secure your future with DOG, where each investment is a step towards financial security and each milestone is a testament to our collective strength! 💰🐕 #crypto",
    "🎨😂 Paint a picture of joy and laughter with DOG memes, where creativity knows no bounds and humor is our universal language of fun and friendship! 🖌️🐶 #cryptotwitter",
    "🚀💎 Strap in for the ride of a lifetime with DOG as your co-pilot, soaring through the crypto skies towards new horizons of wealth and success! 🚀🌈 #memecoin",
"🌟🚀 Embrace the journey with DOG as your companion, where every twist and turn leads to new opportunities and exciting adventures in the crypto world! 🌌🐶 #cryptocurrency",
    "🔥💡 Ignite your passion for DOG and let the flames of enthusiasm, innovation, and community spirit propel us to greater heights of success and prosperity! 🔥🚀 #memecoin",
    "🌈🐾 Follow the rainbow of possibilities with DOG by your side, where each color represents a different aspect of our shared vision for a brighter future in crypto! 🌈💰 #crypto",
    "🎉🐶 Join the celebration of DOG's rise to fame, where every milestone is a reason to rejoice, every achievement a cause for jubilation, and every meme a source of laughter! 🎊😂 #cryptotwitter",
    "💪💎 Stand firm in your belief in DOG, where each dip is a chance to prove your resilience, each peak a testament to your diamond hands, and each moment an opportunity for growth! 🚀💎 #crypto",
    "🚀🌕 Soar to new heights with DOG leading the way, where the moon is just the beginning and the stars are our destination in the vast galaxy of cryptocurrencies! 🚀🌟 #memecoin",
    "🔒🚀 Lock in your gains with DOG's solid performance, where each investment is a step towards financial security, each decision a move towards prosperity, and each day a chance to succeed! 💰🐕 #cryptocurrency",
    "🎨🚀 Paint the town red with DOG memes, where creativity knows no bounds, humor reigns supreme, and laughter is the universal language that unites us all in joy and friendship! 🖌️🐶 #crypto",
    "🌟💫 Shine bright like a DOG diamond, where each facet represents a different aspect of our community spirit, innovation, and unwavering belief in the power of crypto to transform lives! 💎🌈 #cryptotwitter",
    "💡🐾 Illuminate the path to success with DOG as your guiding light, where every step is a move towards financial freedom, every decision a choice for prosperity, and every moment an opportunity for growth! 💡💸 #memecoin",
    "🚀 DOG: The journey to the moon begins now! 🌕🐾 #crypto",
    "🔥 Hold tight, DOG is on fire today! 💎🔥 #memecoin",
    "🐶 Join the pack, buy DOG, and let's howl for gains! 🌙💰 #cryptocurrency",
    "💪 HODL strong, DOG army! We're in this together! 🚀🐾 #crypto",
    "🎉 Celebrate every DOG milestone with memes and joy! 🎊😂 #cryptotwitter",
    "🌈 Ride the rainbow of DOG opportunities to success! 🐕🌈 #memecoin",
    "🚀 To infinity and beyond with DOG! 🚀🌌 #crypto",
    "💎 Diamond hands only with DOG in your wallet! 💎🐶 #cryptocurrency",
    "🎨 Get creative with DOG memes and spread the laughter! 🖌️🐾 #crypto",
    "🌟 Shine bright like a DOG diamond in the crypto sky! 💫💰 #memecoin",
    "🐶 When life gives you DOG coins, make it rain treats! 🌧️🦴 #cryptocurrency",
    "🚀 Strap on your spacesuit, we're going interstellar with DOG! 🚀🌠 #memecoin",
    "🔥 Hot tip: DOG coins are the new currency in town. Woof woof, baby! 💸🐾 #crypto",
    "💎 Who needs diamonds when you can have DOG coins? Sparkle with profits! ✨🐶 #cryptotwitter",
    "🎉 Party like it's 2024 with DOG gains and memes! Let's dance to the Blockchain beat! 🎶🚀 #crypto",
    "🌈 Follow the rainbow road to DOG riches. It's a paw-some journey! 🐾🌈 #memecoin",
    "🌟 When the stars align, DOG coins shine the brightest! Reach for the moon and beyond! 🌟💰 #cryptocurrency",
    "💡 Need a bright idea? Invest in DOG coins and watch your portfolio light up! 💡🐶 #crypto",
    "🎨 Picasso who? We've got DOG meme artists in the house! Creativity level: intergalactic! 🎨😂 #cryptotwitter",
    "🚀 Blast off to financial freedom with DOG coins as your rocket fuel! Destination: prosperity planet! 🚀🌍 #memecoin",
    "🐶 Ready to fetch some profits with DOG coins? Let's play ball in the crypto park! 🎾💰 #cryptocurrency",
    "🚀 DOG coins: the only rocket ship you'll ever need for a trip to the moon and back! 🌕🚀 #memecoin",
    "🔥 Feeling the heat of DOG coin gains? Don't worry, it's just the beginning of the bonfire! 🔥🐾 #crypto",
    "💎 Forget about rocks, diamonds, and gems. All you need are DOG coins for that bling-bling! 💎🐶 #cryptotwitter",
    "🎉 DOG coin party: where every dip is a dance move and every pump is a celebration! Let's groove! 🎶🚀 #crypto",
    "🌈 Ride the DOG rainbow to the pot of gains at the end. Spoiler alert: it's full of DOG coins! 🌈💰 #memecoin",
    "🌟 Stars in your eyes from all the DOG coin success stories? Keep dreaming big and shining bright! ✨🐕 #cryptocurrency",
    "💡 Need a lightbulb moment? Invest in DOG coins and watch your ideas glow with potential! 💡🚀 #crypto",
    "🎨 Picasso would be proud of our DOG coin meme artists. We're painting the town crypto! 🎨😂 #cryptotwitter",
    "🚀 Strap on your seatbelt, we're about to take off to the moon with DOG coins as our fuel! Destination: lunar lambo land! 🚀🌕 #memecoin"
"🐶 Who let the DOG coins out? It's raining profits, baby! 🌧️💰 #cryptocurrency",
    "🚀 Hold onto your leashes, we're going intergalactic with DOG coins! To infinity and beyond! 🚀🌌 #memecoin",
    "🔥 DOG coins are so hot right now, even the sun wants to invest! 🌞🐾 #crypto",
    "💎 Shine bright like a DOG coin diamond, because we're all about that bling-bling! ✨🐶 #cryptotwitter",
    "🎉 DOG coin celebrations are the best kind - full of gains, laughter, and memes! Let's party! 🎊😂 #crypto",
    "🌈 Follow the DOG coin rainbow to the pot of gold at the end. Spoiler alert: it's full of DOG treats! 🌈🦴 #memecoin",
    "🌟 Reach for the stars with DOG coins in your pocket. The sky's not the limit - it's just the beginning! ✨🚀 #cryptocurrency",
    "💡 Need a bright idea? Invest in DOG coins and watch your portfolio light up like a firework! 💡🎆 #crypto",
    "🎨 Our DOG coin meme artists are painting the town red - and green! Get ready for a masterpiece of gains! 🎨💸 #cryptotwitter",
    "🚀 Buckle up, we're about to blast off to the moon with DOG coins leading the way! Hold onto your hats! 🚀🌕 #memecoin"
"Unleash the power of DOG coin and watch it fetch you some serious profits! 🐕💰 Don't miss out on the bark-tastic opportunities ahead! #DOGcoin #crypto #meme",
"Bark up the right tree with DOG coin 🐶🌕 Join the pack and watch your investments grow! #DOGcoin #cryptocurrency #meme"]



in_reply_to_tweet_id = ["1771927340349632973", "1771927230362669138"]

num_of_account = 10
if num_of_account > len(accounts) or num_of_account <= 0:
    raise ValueError(f"Max account is {len(accounts)} accounts")

for i in in_reply_to_tweet_id:
    time.sleep(120)
    tweets = random.sample(tweet_ideas, num_of_account)
    images = random.sample(range(1, 93), num_of_account)
    for index, account in enumerate(accounts):
        if index < num_of_account:
            time.sleep(random.randint(60,120))
            auth = OAuth1(account["consumer_key"], account["consumer_secret"], account["access_token"], account["access_token_secret"])
            try:
                image_path = f'C:\\Users\\lenovo\\OneDrive\\Bitcoin\\Twitter\\Image\\{images[index]}.jpg'

                image_file = open(image_path, 'rb')
                media_data = {
                    'media': image_file
                }
                media_response = requests.post('https://upload.twitter.com/1.1/media/upload.json', auth=auth, files=media_data)


                if media_response.status_code == 200:
                    media_id = str(media_response.json()['media_id'])
                    tweet_data = {
                        'text': tweets[index],
                        "reply": {"in_reply_to_tweet_id": i},
                        "media": {"media_ids": [media_id]}
                    }
                    response = requests.post('https://api.twitter.com/2/tweets', auth=auth, json=tweet_data)

                    if response.status_code == 201:
                        print("Reply with image posted successfully! Tweet id: ",i)
                    else:
                        print("Failed to post reply with image. Status code:", response.status_code)
                        print("Error message:", response.text)
                else:
                    print("Failed to upload image as media. Status code:", media_response.status_code)
                    print("Error message:", media_response.text)

                image_file.close()
            except requests.exceptions.RequestException as e:
                print(e)
