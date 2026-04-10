#!/usr/bin/env python3
"""
Payment Proof Finder — searches web for withdrawal proof screenshots
"""
import requests
import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote

class PaymentProofFinder:
    def __init__(self):
        self.results = []
        
    def search_reddit(self, app_name):
        """Search Reddit for payment proofs"""
        # Using Pushshift API for Reddit
        base_url = "https://api.pushshift.io/reddit/search/submission"
        params = {
            "subreddit": "beermoneyindia,IndiaTax,indiehackers",
            "q": app_name,
            "after": "30d",
            "size": 10,
            "sort": "score"
        }
        try:
            r = requests.get(base_url, params=params, timeout=10)
            data = r.json()
            posts = []
            for post in data.get("data", []):
                posts.append({
                    "title": post.get("title"),
                    "score": post.get("score"),
                    "url": f"https://reddit.com{post.get('permalink')}",
                    "selftext": post.get("selftext", "")[:200]
                })
            return posts
        except Exception as e:
            return [{"error": str(e)}]
    
    def search_twitter(self, app_name):
        """Search Twitter for payment mentions"""
        # Using nitter for Twitter search
        base_url = f"https://nitter.net/search?f=tweets&q={quote(app_name)}"
        return [{"type": "twitter", "url": base_url}]
    
    def search_trustpilot(self, app_name):
        """Check Trustpilot for reviews"""
        url = f"https://www.trustpilot.com/search?query={quote(app_name)}"
        return [{"type": "trustpilot", "url": url}]
    
    def search_google_images(self, app_name):
        """Find screenshot proofs from Google Images"""
        query = f"{app_name} payment proof UPI withdrawal India"
        url = f"https://www.google.com/search?tbm=isch&q={quote(query)}"
        return [{"type": "images", "query": query, "url": url}]
    
    def verify_withdrawal_speed(self, app_name):
        """Analyze payment speed from reviews"""
        posts = self.search_reddit(app_name)
        fast_count = 0
        slow_count = 0
        no_pay = 0
        
        keywords_fast = ["instant", "same day", "received", "paid", "withdrawn", "cleared"]
        keywords_slow = ["days", "week", "pending", "delayed", "waiting"]
        keywords_none = ["scam", "fake", "blocked", "not paid", "fraud"]
        
        for post in posts:
            text = (post.get("title", "") + " " + post.get("selftext", "")).lower()
            if any(k in text for k in keywords_none):
                no_pay += 1
            elif any(k in text for k in keywords_slow):
                slow_count += 1
            elif any(k in text for k in keywords_fast):
                fast_count += 1
        
        total = fast_count + slow_count + no_pay
        if total == 0:
            return {"status": "unknown", "confidence": 0}
        
        fast_pct = (fast_count / total) * 100
        if fast_pct >= 70:
            return {"status": "reliable", "confidence": fast_pct}
        elif fast_pct >= 40:
            return {"status": "mixed", "confidence": fast_pct}
        else:
            return {"status": "risky", "confidence": fast_pct}
    
    def generate_proof_report(self, app_name):
        """Generate full proof report"""
        report = {
            "app_name": app_name,
            "timestamp": datetime.now().isoformat(),
            "reddit_mentions": self.search_reddit(app_name),
            "twitter_mentions": self.search_twitter(app_name),
            "trustpilot": self.search_trustpilot(app_name),
            "image_proofs": self.search_google_images(app_name),
            "withdrawal_speed": self.verify_withdrawal_speed(app_name)
        }
        return report

def main():
    finder = PaymentProofFinder()
    if len(sys.argv) > 1:
        app = " ".join(sys.argv[1:])
        print(f"🔍 Searching proofs for: {app}")
        report = finder.generate_proof_report(app)
        print(json.dumps(report, indent=2))
    else:
        print("Usage: python payment_proof_finder.py <app_name>")

if __name__ == "__main__":
    main()