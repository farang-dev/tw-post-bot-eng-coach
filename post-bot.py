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
def get_learning_advice():
    prompt = """
    あなたは日本人の英語学習者をサポートする英語コーチです。初心者から上級者まで、英語を学び続けるためのモチベーションアップのアドバイスや実用的な学習法を、日本語でツイートしてください。内容の難易度はランダムに設定されるようにしてください。丁寧で親切、日本人のような自然なトーンでツイートしてください。内容は280文字以内に収めてください。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_grammar_explanation():
    prompt = """
    あなたは日本人向けの英語教師です。初心者から上級者までの学習者に合わせて、よく使われる英語の文法ルールを日本語でわかりやすく説明し、簡単な例文を付け加えたツイートを作成してください。丁寧で親切、日本人のような自然なトーンでツイートしてください。内容のレベルはランダムにし、280文字以内に収めてください。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_vocab_list_with_examples():
    prompt = """
    あなたは日本人の英語学習者をサポートする英語教師です。初心者から上級者までのレベルに合わせて、特定のテーマに基づいた英単語リストを日本語で作成し、例文と共にツイートしてください。丁寧で親切、日本人のような自然なトーンでツイートしてください。リストは7～10語程度で、テーマや難易度をランダムにして280文字以内に収めてください。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_test_preparation_tips():
    prompt = """
    あなたは日本人の英語試験対策コーチです。TOEFL、TOEIC、IELTSのいずれかの試験に関する攻略法やスコアアップのコツを日本語でツイートしてください。丁寧で親切、日本人のような自然なトーンでツイートしてください。短期間で効果が出る勉強法や具体的なアドバイスを280文字以内で提供してください。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# List of content generation functions
content_generators = [
    get_learning_advice,
    get_grammar_explanation,
    get_vocab_list_with_examples,
    get_test_preparation_tips
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
