import openai
import tweepy
import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Twitter API v2 setup using Client
client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# Define eagch type of prompt for the content

def get_vocab_list_with_examples():
    prompt = """
    あなたは日本人の英語学習者をサポートする英語教師です。大学院生以上のレベルかつ、特定のテーマに基づいた英単語リストを日本語で作成し、丁寧語で、日本人のような自然なトーンでツイートしてください。リストは10～30語程度で、テーマ（身近なもののテーマや、アカデミックまで。ただ上級者を対象にして）や内容を毎回必ずランダムにして、最後にシェア、インプレッションが最も発生するようなハッシュタグをつけて、280文字以内に収めてください。例えば(あくまで一例だけど、同じようなフォーマットで投稿内容を作成して）、こんなツイートです: 自然災害の英単語:
1. earthquake - 地震
2. tsunami - 津波
3. hurricane - ハリケーン
4. flood - 洪水
5. tornado - 竜巻
6. landslide - 地滑り
7. wildfire - 山火事
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()


# List of content generation functions
content_generators = [
    get_vocab_list_with_examples
]

def tweet_content():
    """Tweet randomly selected content."""
    try:
        # Select a random content generator
        content_func = random.choice(content_generators)
        content = content_func()

        # Post the tweet
        response = client.create_tweet(text=content)
        tweet_id = response.data['id']
        print(f"Tweeted: {content} (Tweet ID: {tweet_id})")
    except tweepy.TooManyRequests as e:
        print("Rate limit reached. Exiting script...")
    except Exception as e:
        print(f"Error tweeting: {e}")

if __name__ == "__main__":
    tweet_content()  # Run the content generation and tweeting once
