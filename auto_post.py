import os
import random
import tweepy
from openai import OpenAI

# ===== OpenAI（文章生成AI）=====
openai_client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

# ===== X（投稿用）=====
client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
)

# ===== ネタ被り防止用テーマ =====
topics = [
    "宇宙", "人間の体", "歴史", "動物",
    "心理学", "科学", "食べ物", "言語"
]

topic = random.choice(topics)

prompt = f"""
Xに投稿する短い雑学を1文で作ってください。
テーマは「{topic}」。
80文字以内、日本語、わかりやすく。
"""

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

text = response.choices[0].message.content.strip()

# 投稿
client.create_tweet(text=text)
