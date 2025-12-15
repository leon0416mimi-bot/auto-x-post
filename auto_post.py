import os
import time
import random
import tweepy
from openai import OpenAI

# ===== API設定 =====
client_ai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

client_x = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"]
)

# ===== ネタ被り防止 =====
USED_FILE = "used_topics.txt"

def load_used():
    if not os.path.exists(USED_FILE):
        return set()
    with open(USED_FILE, "r", encoding="utf-8") as f:
        return set(f.read().splitlines())

def save_used(topic):
    with open(USED_FILE, "a", encoding="utf-8") as f:
        f.write(topic + "\n")

# ===== 雑学生成 =====
def generate_trivia(used):
    prompt = f"""
短くてわかりやすい雑学を1つ作ってください。
・60文字以内
・日本語
・すでに使ったネタは避ける
使用済みネタ一覧：{list(used)}
"""
    res = client_ai.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return res.output_text.strip()

# ===== 投稿処理 =====
def post_once():
    used = load_used()
    text = generate_trivia(used)
    client_x.create_tweet(text=text)
    save_used(text)
    print("投稿成功:", text)

# ===== 1日3回投稿 =====
for i in range(3):
    post_once()
    if i < 2:
        time.sleep(2 * 60 * 60)  # 2時間待つ
