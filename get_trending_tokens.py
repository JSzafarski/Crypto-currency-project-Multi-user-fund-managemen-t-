# get like top 10 tokens for ppl to raid (update every 12h)
import cloudscraper

scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
content = scraper.get("https://dexscreener.com/solana/dsuvc5qf5ljhhv5e2td184ixotsncnwj7i4jja4xsrmt").text

print(content)
