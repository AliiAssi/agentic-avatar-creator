import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("💡 python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

from app import app

def check_requirements():
    """Check if all requirements are met before starting"""
    print("🔍 Checking requirements...")
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set!")
        print("💡 Please set it using: export GOOGLE_API_KEY='your_api_key_here'")
        return False
    
    print("✅ API key found")
    
    # Check if templates directory exists
    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        print(f"📁 Templates directory missing!")
        print("💡 Please ensure templates/index.html exists")
        return False
    
    print("✅ Templates directory found")
    return True

def main():
    """Main function to start the application"""
    print("🚀 Starting AI Image Studio...")
    print("=" * 50)
    
    if not check_requirements():
        print("❌ Requirements check failed!")
        sys.exit(1)
    
    print("✅ All requirements met!")
    print("🌐 Starting Flask server...")
    print("📡 Application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()