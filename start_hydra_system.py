#!/usr/bin/env python3
"""
HYDRA System Startup Script
Launches all components of the HYDRA competitive intelligence system
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(command, description, background=False):
    """Run a command and handle errors"""
    print(f"🚀 {description}...")
    try:
        if background:
            process = subprocess.Popen(command, shell=True)
            print(f"✅ {description} started (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {description} completed")
            return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_docker():
    """Check if Docker is running"""
    try:
        subprocess.run(["docker", "version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🐉 HYDRA SYSTEM STARTUP                   ║
    ║                                                              ║
    ║  Starting the Competitive Intelligence Monster...            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    
    if not check_docker():
        print("❌ Docker is not running. Please start Docker first.")
        sys.exit(1)
    
    print("✅ Docker is running")
    
    # Step 1: Start PostgreSQL and n8n with Docker Compose
    print("\n📦 Starting infrastructure services...")
    run_command("docker-compose up -d", "Starting PostgreSQL and n8n")
    
    # Wait for PostgreSQL to be ready
    print("⏳ Waiting for PostgreSQL to be ready...")
    time.sleep(10)
    
    # Step 2: Initialize database
    print("\n🗄️  Initializing database...")
    run_command("python -c \"from backend.core.database import init_db; init_db()\"", "Database initialization")
    
    # Step 3: Start Ollama (if available)
    print("\n🤖 Starting Ollama...")
    ollama_process = run_command("ollama serve", "Ollama server", background=True)
    
    if ollama_process:
        time.sleep(5)
        run_command("ollama pull llama3.1:8b", "Downloading Llama model")
    
    # Step 4: Start HYDRA Brain
    print("\n🧠 Starting HYDRA Brain...")
    brain_process = run_command(
        "cd backend && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000",
        "HYDRA Brain API server",
        background=True
    )
    
    # Step 5: Start Frontend (if Node.js is available)
    print("\n🖥️  Starting Frontend...")
    try:
        frontend_process = run_command(
            "cd frontend && npm install && npm start",
            "React frontend",
            background=True
        )
    except FileNotFoundError:
        print("⚠️  Node.js not found. Frontend will need to be started manually.")
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎉 HYDRA IS READY!                       ║
    ║                                                              ║
    ║  Services:                                                   ║
    ║  • PostgreSQL: localhost:5432                               ║
    ║  • n8n Dashboard: http://localhost:5678                     ║
    ║  • HYDRA API: http://localhost:8000                         ║
    ║  • Frontend: http://localhost:3000                          ║
    ║  • Ollama: http://localhost:11434                           ║
    ║                                                              ║
    ║  Next Steps:                                                ║
    ║  1. Import n8n workflow from n8n/workflows/hydra_main.json  ║
    ║  2. Add your Bright Data credentials in n8n                 ║
    ║  3. Configure competitors in the dashboard                  ║
    ║  4. Watch the intelligence flow!                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down HYDRA...")
        run_command("docker-compose down", "Stopping Docker services")
        print("✅ HYDRA shutdown complete")

if __name__ == "__main__":
    main()
