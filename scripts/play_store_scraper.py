#!/usr/bin/env python3
"""
Play Store App Scraper — for BELLION APP HUNTER
Searches Google Play Store for money-making apps
"""
import requests
import json
import sys
from datetime import datetime

try:
    from google_play_scraper import search, app, reviews
    PLAY_SCRAPER = True
except ImportError:
    PLAY_SCRAPER = False

class AppHunter:
    def __init__(self):
        self.results = []
        self.categories = {
            "micro_tasks": ["earn money", "task", "micro job", "daily earnings"],
            "gaming": ["play and earn", "game rewards", "quiz earn"],
            "reselling": ["reseller", "sell online", "wholesale"],
            "finance": ["loan", "credit", "insurance agent"]
        }
    
    def search_play_store(self, query, lang="en", country="in", limit=50):
        """Search Play Store via gpsear.ch or fallback"""
        try:
            results = search(
                query,
                lang=lang,
                country=country,
                n=limit
            )
            return results
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_app(self, app_id):
        """Deep analyze a specific app"""
        try:
            info = app(app_id, lang="en", country="in")
            return {
                "id": info.get("appId"),
                "title": info.get("title"),
                "rating": info.get("score"),
                "rating_count": info.get("ratings"),
                "installs": info.get("installs"),
                "free": info.get("free"),
                "price": info.get("price"),
                "description": info.get("description"),
                "developer": info.get("developer"),
                "updated": info.get("updated"),
                "genre": info.get("genre"),
                "icon": info.get("icon")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def batch_search(self, queries):
        """Search multiple queries and compile results"""
        all_apps = {}
        for category, search_list in self.categories.items():
            for query in search_list:
                results = self.search_play_store(query)
                for app in results:
                    app_id = app.get("appId")
                    if app_id and app_id not in all_apps:
                        all_apps[app_id] = {
                            **app,
                            "matched_queries": [query],
                            "category": category
                        }
                    elif app_id:
                        all_apps[app_id]["matched_queries"].append(query)
        return list(all_apps.values())
    
    def rank_apps(self, apps, criteria="overall"):
        """Rank apps by criteria"""
        if criteria == "overall":
            # Weighted ranking
            for app in apps:
                score = 0
                # Rating weight: 20
                score += (app.get("score", 0) or 0) * 20
                # Install count weight: 30
                installs = app.get("installs", "0")
                try:
                    install_num = int(installs.replace(",","").replace("+",""))
                    score += min(install_num / 100000, 100)
                except:
                    pass
                # Category boost
                if "money" in str(app.get("title","")).lower():
                    score += 50
                app["bellion_score"] = score
        else:
            for app in apps:
                app["bellion_score"] = app.get("score", 0) or 0
        return sorted(apps, key=lambda x: x.get("bellion_score", 0), reverse=True)
    
    def generate_report(self, apps, output_path="data/rankings.md"):
        """Generate markdown report"""
        ranked = self.rank_apps(apps)
        report = f"# 📊 BELLION APP HUNTER REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += f"Total apps found: {len(apps)}\n\n"
        report += "## 🏆 TOP 10 APPS\n\n"
        report += "| Rank | App | Score | Rating | Installs | Category |\n"
        report += "|------|-----|-------|--------|---------|----------|\n"
        for i, app in enumerate(ranked[:10], 1):
            report += f"| {i} | {app.get('title','N/A')} | {app.get('bellion_score',0):.1f} | {app.get('score','N/A')} | {app.get('installs','N/A')} | {app.get('category','N/A')} |\n"
        report += "\n## 📱 ALL APPS\n\n"
        for app in ranked:
            report += f"### {app.get('title','N/A')}\n"
            report += f"- ID: {app.get('appId','N/A')}\n"
            report += f"- Score: {app.get('bellion_score',0):.1f}\n"
            report += f"- Rating: {app.get('score','N/A')} ({app.get('ratings','N/A')} reviews)\n"
            report += f"- Installs: {app.get('installs','N/A')}\n"
            report += f"- Developer: {app.get('developer','N/A')}\n"
            report += f"- Genre: {app.get('genre','N/A')}\n"
            report += f"- Matched: {', '.join(app.get('matched_queries',[]))}\n\n"
        return report

def main():
    hunter = AppHunter()
    print("🔍 BELLION APP HUNTER — Starting mass search...")
    print(f"Play Store scraper available: {PLAY_SCRAPER}")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else "earn money"
            results = hunter.search_play_store(query)
            print(json.dumps(results[:10], indent=2))
        elif sys.argv[1] == "analyze":
            app_id = sys.argv[2] if len(sys.argv) > 2 else ""
            if app_id:
                result = hunter.analyze_app(app_id)
                print(json.dumps(result, indent=2))
        elif sys.argv[1] == "batch":
            apps = hunter.batch_search(hunter.categories)
            report = hunter.generate_report(apps)
            print(report)
        elif sys.argv[1] == "rank":
            apps = hunter.batch_search(hunter.categories)
            ranked = hunter.rank_apps(apps)
            for i, app in enumerate(ranked[:5], 1):
                print(f"{i}. {app.get('title')} — Score: {app.get('bellion_score')}")
    else:
        # Default: batch search all categories
        print("Running batch search across all categories...")
        apps = hunter.batch_search(hunter.categories)
        ranked = hunter.rank_apps(apps)
        print(f"\n✅ Found {len(apps)} unique apps")
        print("\n🏆 TOP 5:")
        for i, app in enumerate(ranked[:5], 1):
            print(f"  {i}. {app.get('title')} (score: {app.get('bellion_score',0):.1f})")

if __name__ == "__main__":
    main()