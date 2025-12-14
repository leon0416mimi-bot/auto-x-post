import os
import openai
import tweepy
import random

openai.api_key = os.environ["OPENAI_API_KEY"]

client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"]
)

prompt = "Xに投稿する短い雑学を1文で作ってください（40文字以内）"

res = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

text = res.choices[0].message.content.strip()
client.create_tweet(text=text)
