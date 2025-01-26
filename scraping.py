import logging
import praw
import pandas as pd
import datetime
import re
import json
import os
import time
from configparser import ConfigParser
from logging_config import setup_logging
from dotenv import load_dotenv

setup_logging()
logger = logging.getLogger('scraper_logger')

# Function to clean text
def clean_text(text):
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove emojis
    text = re.sub(r'[^\w\s,.!?-]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()   # Remove extra spaces
    return text

# Function to load processed IDs from a JSON file
def load_processed_ids(filename="processed_ids.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return set(json.load(file))  # Load already processed IDs
    else:
        return set()  # Return an empty set if the file does not exist

# Function to save processed IDs to a JSON file
def save_processed_ids(processed_ids, filename="processed_ids.json"):
    with open(filename, "w") as file:
        json.dump(list(processed_ids), file)  # Save IDs as a list

# Function to initialize Reddit API
def initialize_reddit():
    load_dotenv()

    client_id=os.getenv("CLIENT_ID")
    client_secret=os.getenv("CLIENT_SECRET")
    user_agent=os.getenv("USER_AGENT")

    # Validate environment variables
    if not all([client_id, client_secret, user_agent]):
        logger.error("Environment variables CLIENT_ID, CLIENT_SECRET, and USER_AGENT must be set.")
        raise ValueError("Environment variables CLIENT_ID, CLIENT_SECRET, and USER_AGENT must be set.")

    try:
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        return reddit
    except Exception as e:
        logger.error(f"Error initializing Reddit API: {e}")
        return None

# Function to read configuration from config.ini
def read_config():
    config = ConfigParser()
    config.read('config.ini')

    subreddit_name = config.get('DEFAULT', 'subreddit_name')
    num_posts = config.getint('DEFAULT', 'num_posts')

    return subreddit_name, num_posts

# Function to scrape posts and comments from a subreddit
def scrape_subreddit(reddit, subreddit_name, num_posts):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []
    processed_posts_ids = load_processed_ids()

    post_call_count = 0
    comment_call_count = 0
    start_time = time.time()

    for post in subreddit.new(limit=num_posts):
        if post_call_count + comment_call_count >= 55:
            elapsed_time = time.time() - start_time
            if elapsed_time < 60:
                time_to_wait = 60 - elapsed_time
                logger.info(f"Rate limit reached for API calls, waiting {time_to_wait:.2f} seconds...")
                time.sleep(time_to_wait)
                start_time = time.time()
                post_call_count = 0
                comment_call_count = 0

        if post.id in processed_posts_ids:
            continue

        processed_posts_ids.add(post.id)
        post_call_count += 1

        cleaned_post_text = clean_text(post.selftext)

        posts_data.append({
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.datetime.fromtimestamp(post.created_utc),
            "author": post.author.name if post.author else "N/A",
            "post_text": cleaned_post_text,
        })

        posts_data.extend(scrape_comments(post, processed_posts_ids))

    return posts_data, processed_posts_ids

# Function to scrape comments from a post
def scrape_comments(post, processed_posts_ids):
    comments_data = []

    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        if comment.id in processed_posts_ids:
            continue

        processed_posts_ids.add(comment.id)

        cleaned_comment_text = clean_text(comment.body)

        comment_data = {
            "title": post.title,
            "post_text": clean_text(post.selftext),
            "comment_text": cleaned_comment_text,
            "comment_author": comment.author.name if comment.author else "N/A",
            "comment_score": comment.score,
            "comment_created_utc": datetime.datetime.fromtimestamp(comment.created_utc),
        }
        comments_data.append(comment_data)

    return comments_data

# Function to save data to CSV
def save_to_csv(posts_data, subreddit_name):
    df = pd.DataFrame(posts_data)

    csv_filename = f"reddit_{subreddit_name}_posts.csv"

    try:
        df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)
        logger.info(f"Data saved to {csv_filename}")
    except Exception as e:
        logger.error(f"Error saving data to CSV: {e}")

# Main function to perform scraping process
def perform_scraping():
    reddit = initialize_reddit()

    if reddit is None:
        return

    subreddit_name, num_posts = read_config()

    posts_data, processed_posts_ids = scrape_subreddit(reddit, subreddit_name, num_posts)

    save_to_csv(posts_data, subreddit_name)

    save_processed_ids(processed_posts_ids)

    logger.info(f"Scraping completed! Data saved in reddit_{subreddit_name}_posts.csv")

perform_scraping()
