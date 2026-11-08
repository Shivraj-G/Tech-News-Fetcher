import feedparser
import requests
import os
from dotenv import load_dotenv
load_dotenv()
webhook_url = os.getenv("WEBHOOK")

sourse_url = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai/index.xml",
    "Ars Technica AI": "https://arstechnica.com/ai/feed/",
    "Google AI Blog": "https://blog.google/technology/ai/rss/",
    "OpenAI": "https://openai.com/news/rss.xml",
    "Anthropic": "https://www.anthropic.com/rss.xml",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
    "Google Research": "https://research.google/blog/rss/",
    "Microsoft Research": "https://www.microsoft.com/en-us/research/feed/",
    "NVIDIA Developer Blog": "https://developer.nvidia.com/blog/feed/",
} 


limit = 5

def get_latest_news(sourse_url,limit):

    all_news = {}
    for sourse,url in sourse_url.items():
        news =  feedparser.parse(url)

        #print("+"*30)
        #print(sourse)
        #print("+"*30)
        #print(news)
        try:
            if sourse not in all_news:
                    all_news[sourse]=[]
            for entry in news.entries[:limit]:
                #print("="*50)
                #print("\n",entry.published,"\n",entry.title,"\n",entry.summary,"\n",entry.link)
                all_news[sourse].append({"Title":entry.title,"Published at":entry.published,"Summery":entry.summary,"Link":entry.link})
        except Exception as e:
            print(f"An error occured while fetching {sourse} : {e}")
    return all_news


def build_embeds(news):
    embeds = []
    for source, articles in news.items():
        for article in articles:
            embeds.append({
                "title": article["Title"],
                "description": article["Summery"],
                "url": article["Link"],
                "color": 3447003,
                "author": {"name": source},
                "footer": {"text": article["Published at"]}
            })
    return embeds

def send_to_discord(webhook_url, news_dict):
    embeds = build_embeds(news_dict)

    for i in range(0, len(embeds), 10):
        batch = embeds[i:i + 10]
        response = requests.post(webhook_url, json={"embeds": batch})
        print(response.status_code, response.text)

news = get_latest_news(sourse_url,limit)
send_to_discord(webhook_url,news)
