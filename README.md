# Tech News Fetcher

A small Python script that pulls the latest AI/tech articles from a set of RSS and Atom feeds and posts them as Discord webhook embeds.

## What it does

1. Reads `WEBHOOK` from a `.env` file.
2. Parses 12 tech/AI news sources with [`feedparser`](https://pypi.org/project/feedparser/).
3. Keeps the first `limit` (default **5**) entries from each source.
4. Converts each entry into a Discord embed (title, summary, link, source name, publish date).
5. Sends the embeds to the Discord webhook in batches of 10 per message.

Each run produces `12 sources × 5 articles = 60` embeds, delivered as 6 Discord messages.

## Sources

| Source | Feed |
| --- | --- |
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` |
| VentureBeat AI | `https://venturebeat.com/category/ai/feed/` |
| MIT Technology Review AI | `https://www.technologyreview.com/topic/artificial-intelligence/feed/` |
| The Verge AI | `https://www.theverge.com/rss/ai/index.xml` |
| Ars Technica AI | `https://arstechnica.com/ai/feed/` |
| Google AI Blog | `https://blog.google/technology/ai/rss/` |
| OpenAI | `https://openai.com/news/rss.xml` |
| Anthropic | `https://www.anthropic.com/rss.xml` |
| Hugging Face | `https://huggingface.co/blog/feed.xml` |
| Google Research | `https://research.google/blog/rss/` |
| Microsoft Research | `https://www.microsoft.com/en-us/research/feed/` |
| NVIDIA Developer Blog | `https://developer.nvidia.com/blog/feed/` |

## Project structure

```
Tech News Fetcher/
├── .env                # webhook URL (git-ignored)
├── .gitignore          # ignores .env
├── news_fetcher.py     # the whole script
├── pyproject.toml      # project metadata + dependencies
└── README.md
```

## Requirements

- Python 3.8+

## Install

```bash
pip install .
```

Or for an editable (development) install:

```bash
pip install -e ".[dev]"
```

Dependencies (`feedparser`, `requests`, `python-dotenv`) are declared in `pyproject.toml` and installed automatically.

## Setup

1. Create a Discord webhook: in your Discord channel open **Edit Channel → Integrations → Webhooks → New Webhook**, then copy the URL.
2. Create a `.env` file in the project root:

   ```env
   WEBHOOK=https://discord.com/api/webhooks/<id>/<token>
   ```

3. Run the script:

   ```bash
   python news_fetcher.py
   ```

   or, after installing the package, via the console script:

   ```bash
   tech-news-fetcher
   ```

The script prints the HTTP status code and response body for each batch, e.g. `204 ` for a successful Discord post.

> `.env` is listed in `.gitignore`, so your webhook stays out of version control. If you ever commit it, rotate the webhook immediately.

## Configuration

| Setting | Where | Default |
| --- | --- | --- |
| `WEBHOOK` | `.env` | required |
| `limit` | `news_fetcher.py` | `5` |
| `source_urls` | `news_fetcher.py` | 12 feeds |
| Embed color | `build_embeds()` | `3447003` (blue) |

Lower `limit` to 1–2 if you want a shorter daily digest, or raise it if your Discord channel can handle the volume.

## Automating it

Run it on a schedule instead of manually. Options:

- **cron** (Linux/macOS): `0 9 * * * cd /path/to/project && python news_fetcher.py`
- **Windows Task Scheduler**: create a task that runs `python "D:\python\Tech News Fetcher\news_fetcher.py"` daily.
- **GitHub Actions**: run the script on a schedule with `WEBHOOK` stored as a repository secret.

## Known limitations

- **Feeds are fetched on every run** with no caching or deduplication, so running it twice in one day repeats the same articles.
- **Hard-coded config**: sources and limits live in the script rather than in the `.env` file.
- **Some entries may lack `entry.published`** (e.g. Atom feeds), which raises an error caught per-source by the `try/except`.
