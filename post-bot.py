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

# Define each type of prompt for the content

def get_better_phrases():
    prompt = """
「[シチュエーション]に役立つ英語フレーズを紹介し、最も基本的な表現と、より自然な言い回しを提供してください。さらに、そのフレーズを日常会話で使うことで、よりフレンドリーや自信を持って話せる点を強調します。絵文字は使用せず、シンプルで明確な言葉を使用してください。」

例1:
シチュエーション: "遅刻したとき"

「英語で『遅れてすみません』はどう言う？
基本的な表現→「I’m sorry I’m late」
でも、もっとカジュアルで自然に言いたいなら→
「Sorry I kept you waiting」
会話の中でこのフレーズを使うことで、より親しみやすく聞こえるよ！」
例2:
シチュエーション: "会議をキャンセルしたいとき"

「英語で『会議をキャンセルしたい』はどう言う？
基本的な表現→「I need to cancel the meeting」
でも、もっと柔らかく伝えたいなら→
「Would it be possible to reschedule the meeting?」
この言い回しを使うと、相手に対して配慮を示しながら伝えることができる！」
例3:
シチュエーション: "感謝の気持ちを伝えたいとき"

「英語で『ありがとう』はどう言う？
基本的な表現→「Thank you」
でも、感謝の気持ちをもっと強調したいなら→
「I really appreciate it」
より深い感謝を伝えたいときにぴったりなフレーズ！」
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_vocab_list_with_examples():
    prompt = """
    あなたは日本人の英語学習者をサポートする英語教師です。大学院生以上のレベルかつ、特定のテーマに基づいた英単語リストを日本語で作成し、丁寧語で、日本人のような自然なトーンでツイートしてください。リストは10～30語程度で、テーマ（身近なもののテーマや、アカデミックまで）や内容を毎回必ずランダムにして、最後にシェア、インプレッションが最も発生するようなハッシュタグをつけて、280文字以内に収めてください。例えば(あくまで一例だけど、同じようなフォーマットで投稿内容を作成して）、こんなツイートです: 自然災害の英単語:
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

def get_useful_phrases():
    prompt = """
  英語を学びたい中級者～超上級者向けに、簡単で実用的なフレーズを紹介するTwitter投稿を作成してください。
条件:
投稿は1ツイートで140文字以内に収めること。
フレーズは3～5個の具体的な例を挙げ、短い日本語の説明をつけること。
「忙しいとき」「予定を断るとき」など、シーンを明確にする。
読者にアクションを促す一文を最後につける。
カジュアルだけれど、丁寧な（丁寧語で）トーンで書くこと。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# List of content generation functions
content_generators = [
    get_better_phrases,
    get_vocab_list_with_examples,
    get_useful_phrases
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
