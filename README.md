# 📥 Reddit Scraper

A Python-based tool to scrape posts and comments from Reddit, offering data collection and analysis capabilities for research, sentiment analysis, and trend tracking.  

This scraper is designed to efficiently utilize Reddit's free API call limits per minute, ensuring compliance with rate limits while maximizing data collection without interruptions.

---

## 🚀 Features

- **Efficient Data Collection** – Scrapes posts and comments from any subreddit while staying within Reddit's free API call limits per minute.
- **Customizable** – Easily configure subreddit targets and scraping limits via a configuration file.
- **Automated Scheduling** – Supports periodic scraping using the built-in scheduler script for continuous data updates.
- **Data Persistence** – Saves scraped data in CSV format, making it easy to analyze trends and insights later.
- **Duplicate Handling** – Smart tracking system prevents reprocessing of previously collected posts and comments, ensuring data consistency and avoiding redundancy.
- **Error Handling & Logging** – Comprehensive logging to track the scraping process and gracefully handle API rate limits or unexpected errors.

---

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sergiovzambelli/scraper_reddit_free_plan.git
   ```
2. Navigate to the project directory:
   ```
   cd reddit-scraper
   ```
3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set the required environment variables:
   ```
   export CLIENT_ID=your_client_id
   export CLIENT_SECRET=your_client_secret
   export USER_AGENT=your_user_agent
   ```
6. (Optional) Update the `config.ini` file with the desired subreddit name and number of posts to scrape.


---

## Usage

Run the scheduler script to automate the scraping process:
```
python scheduler.py
```
This will scrape posts and comments from the configured subreddit and save the data to a CSV file, once every minute.

---

## API

The main functions in the `scraping.py` file are:

- `initialize_reddit()`: Initializes the Reddit API using the provided environment variables.
- `read_config()`: Reads the subreddit name and number of posts to scrape from the `config.ini` file.
- `scrape_subreddit(reddit, subreddit_name, num_posts)`: Scrapes posts and comments from the specified subreddit.
- `save_to_csv(posts_data, subreddit_name)`: Saves the scraped data to a CSV file.

---

## 📊 Data Output

The scraped data is stored in a structured CSV format with the following key fields:

| Field          | Description                                |
|----------------|--------------------------------------------|
| `title`        | Title of the Reddit post                   |
| `score`        | Upvote score of the post                   |
| `num_comments` | Number of comments on the post             |
| `created_utc`  | Timestamp of post creation                 |
| `author`       | Reddit username of the post author         |
| `post_text`    | Cleaned text content of the post           |
| `comment_text` | Cleaned text content of associated comments|
| `comment_score`| Upvote score of the comment                |
| `comment_author` | Reddit username of the comment author     |

---

## 🛡️ Error Handling and Logging

The scraper includes built-in error handling mechanisms to:

- Manage Reddit API rate limits and request failures.
- Handle missing or deleted posts/comments gracefully.
- Log events and errors into a dedicated log file for troubleshooting.

---

## 🔄 Automation

The `scheduler.py` script automates the scraping process at regular intervals, ensuring continuous data collection without manual intervention. The scheduling interval can be adjusted based on requirements.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE), allowing free use and modification with attribution.

---

## 📫 Contact

For any questions, suggestions, or contributions, feel free to reach out via GitHub Issues.
