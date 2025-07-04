from flask import Flask, request, jsonify, render_template
import os
import json
from werkzeug.utils import secure_filename

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from orchestrator import Orchestrator
from agents.creator import CreatorAgent
from agents.analyzer import AnalyzerAgent

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the orchestrator and agents
orchestrator = Orchestrator()

# Load API keys from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Warning: GOOGLE_API_KEY environment variable is not set.")
    print("Please set it before running the application.")

try:
    # Register the agents
    if api_key:
        analyzer_agent = AnalyzerAgent(api_key)
        creator_agent = CreatorAgent(api_key)
        orchestrator.register_agent(analyzer_agent.get_name(), analyzer_agent)
        orchestrator.register_agent(creator_agent.get_name(), creator_agent)
        print("Agents registered successfully!")
    else:
        print("Skipping agent registration due to missing API key.")
except Exception as e:
    print(f"Error initializing agents: {e}")

# Helper function to check allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get list of registered agents and their capabilities"""
    try:
        agents = orchestrator.list_agents()
        capabilities = orchestrator.get_agent_capabilities()
        return jsonify({
            "success": True,
            "agents": agents,
            "capabilities": capabilities
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/create', methods=['POST'])
def create_image():
    """Create an image based on text prompt"""
    try:
        data = request.json
        prompt = data.get('prompt')
        agent_name = data.get('agent', 'CreatorAgent')
        
        if not prompt:
            return jsonify({"success": False, "error": "Prompt is required"}), 400
        
        if not api_key:
            return jsonify({"success": False, "error": "API key not configured"}), 500
        
        response = orchestrator.create_image(agent_name, prompt)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """Analyze an uploaded image"""
    try:
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400
        
        file = request.files['image']
        caption = request.form.get('caption', 'Analyze this image')
        agent_name = request.form.get('agent', 'AnalyzerAgent')
        
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "File type not allowed"}), 400
        
        if not api_key:
            return jsonify({"success": False, "error": "API key not configured"}), 500
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analyze the image
        response = orchestrator.analyze_image(agent_name, file_path, caption)
        
        # Clean up uploaded file after analysis
        try:
            os.remove(file_path)
        except:
            pass  # Ignore cleanup errors
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/process', methods=['POST'])
def run_full_process():
    """Run the complete process: analyze image then create new image based on analysis"""
    try:
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400
        
        file = request.files['image']
        caption = request.form.get('caption', 'Analyze this image')
        
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "File type not allowed"}), 400
        
        if not api_key:
            return jsonify({"success": False, "error": "API key not configured"}), 500
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Run the complete process
        response = orchestrator.run_process(file_path, caption)
        
        # Clean up uploaded file after processing
        try:
            os.remove(file_path)
        except:
            pass  # Ignore cleanup errors
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"success": False, "error": "File too large"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

if __name__ == '__main__':
    print("Starting Flask application...")
    print(f"Registered agents: {orchestrator.list_agents()}")
    app.run(debug=True, host='0.0.0.0', port=5000)