#!/usr/bin/env python3
"""
Check deployment status and provide deployment links
"""

import requests
import time
import sys

def check_url(url, name):
    """Check if a URL is accessible"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {name}: {url} - LIVE")
            return True
        else:
            print(f"❌ {name}: {url} - Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name}: {url} - Not accessible ({str(e)})")
        return False

def main():
    print("🔍 Checking Deployment Status for K-Means Clustering Tool")
    print("=" * 60)
    
    # Possible deployment URLs
    urls = {
        "Vercel": "https://k-means-clutering-tool.vercel.app",
        "Railway": "https://k-means-clutering-tool.up.railway.app", 
        "Render": "https://k-means-clutering-tool.onrender.com",
        "Heroku": "https://k-means-clustering-tool.herokuapp.com"
    }
    
    live_deployments = []
    
    for name, url in urls.items():
        if check_url(url, name):
            live_deployments.append((name, url))
        time.sleep(1)  # Be nice to servers
    
    print("\n" + "=" * 60)
    
    if live_deployments:
        print("🎉 Live Deployments Found:")
        for name, url in live_deployments:
            print(f"   🌐 {name}: {url}")
        
        print(f"\n📱 Test your clustering tool at any of the above URLs!")
        print("📋 Upload a CSV file and start clustering!")
        
    else:
        print("❌ No live deployments found yet.")
        print("\n🚀 To deploy:")
        print("1. Push code to GitHub")
        print("2. Connect to Vercel/Railway/Render")
        print("3. Deploy with one click")
        print("\n📖 See GITHUB_DEPLOY.md for detailed instructions")
    
    print(f"\n📊 Repository: https://github.com/Ahmadjamil888/K_means-clutering-tool")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Check cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have internet connectivity")