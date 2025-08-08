#!/usr/bin/env python3
"""
Quick deployment script for the clustering tool
"""

import subprocess
import sys
import os
import webbrowser
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_dependencies():
    """Check if required tools are installed"""
    tools = {
        'python': 'python --version',
        'pip': 'pip --version',
        'docker': 'docker --version',
        'git': 'git --version'
    }
    
    available = {}
    for tool, command in tools.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            available[tool] = True
            print(f"✅ {tool} is available")
        except subprocess.CalledProcessError:
            available[tool] = False
            print(f"❌ {tool} is not available")
    
    return available

def deploy_local():
    """Deploy locally with Python"""
    print("\n🚀 Deploying locally...")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    print("✅ Starting local server...")
    print("🌐 Open http://localhost:5000 in your browser")
    print("⏹️  Press Ctrl+C to stop the server")
    
    # Start the server
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def deploy_docker():
    """Deploy with Docker"""
    print("\n🐳 Deploying with Docker...")
    
    # Build image
    if not run_command("docker build -t clustering-tool .", "Building Docker image"):
        return False
    
    # Run container
    print("🚀 Starting Docker container...")
    print("🌐 Open http://localhost:5000 in your browser")
    print("⏹️  Press Ctrl+C to stop the container")
    
    try:
        subprocess.run("docker run -p 5000:5000 clustering-tool", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Container stopped")

def deploy_docker_compose():
    """Deploy with Docker Compose"""
    print("\n🐳 Deploying with Docker Compose...")
    
    print("🚀 Starting services...")
    print("🌐 Open http://localhost:5000 in your browser")
    print("⏹️  Press Ctrl+C to stop services")
    
    try:
        subprocess.run("docker-compose up --build", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Services stopped")

def main():
    print("🤖 AI-Powered K-Means Clustering Tool - Deployment Script")
    print("=" * 60)
    
    # Check dependencies
    available = check_dependencies()
    
    print("\n📋 Deployment Options:")
    print("1. 🐍 Local Python deployment")
    if available['docker']:
        print("2. 🐳 Docker deployment")
        print("3. 🐳 Docker Compose deployment")
    print("4. ℹ️  Show deployment guide")
    print("5. 🚪 Exit")
    
    while True:
        try:
            choice = input("\n👉 Choose deployment option (1-5): ").strip()
            
            if choice == '1':
                deploy_local()
                break
            elif choice == '2' and available['docker']:
                deploy_docker()
                break
            elif choice == '3' and available['docker']:
                deploy_docker_compose()
                break
            elif choice == '4':
                print("\n📖 Opening deployment guide...")
                if os.path.exists('DEPLOYMENT.md'):
                    with open('DEPLOYMENT.md', 'r') as f:
                        print(f.read())
                else:
                    print("❌ DEPLOYMENT.md not found")
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Deployment cancelled")
            break

if __name__ == "__main__":
    main()