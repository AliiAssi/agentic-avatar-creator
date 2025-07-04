# AI Image Analyzer & Creator

A Flask web application that uses Google's Gemini to analyze images and create new ones based on text prompts or analysis results.

## Features

- **Image Analysis**: Upload images and get detailed AI-powered analysis
- **Image Generation**: Create images from text descriptions  
- **Complete Pipeline**: Analyze an image and automatically generate a new image based on the analysis
- **Modern Web UI**: Responsive interface with drag-and-drop file uploads
- **Agent-based Architecture**: Modular design with separate analyzer and creator agents

## Requirements

- Python 3.8+
- Google AI API access
- Flask and dependencies (see requirements.txt)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AliiAssi/agentic-avatar-creator.git
   cd agentic-avatar-creator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export GOOGLE_API_KEY="your_google_api_key_here"
   ```
   
   Or create a `.env` file:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Create necessary directories**
   ```bash
   mkdir uploads
   mkdir templates
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Usage Examples

### Analyze an image
```bash
curl -X POST -F "image=@photo.jpg" http://localhost:5000/api/analyze
```

### Generate an image
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"prompt":"a sunset over mountains"}' \
  http://localhost:5000/api/create
```

### Complete pipeline (analyze then create)
```bash
curl -X POST -F "image=@photo.jpg" -F "caption=enhance this" \
  http://localhost:5000/api/process
```

## API Endpoints

### GET /api/agents
Get list of registered agents and their capabilities.

### POST /api/analyze
Analyze an uploaded image.
- **Body**: FormData with `image` file and optional `caption` text
- **Response**: Analysis result with description

### POST /api/create
Generate an image from a text prompt.
- **Body**: JSON with `prompt` string
- **Response**: Generated image data or description

### POST /api/process
Run complete pipeline: analyze image then create new image.
- **Body**: FormData with `image` file and optional `caption` text
- **Response**: Both analysis and creation results

## Project Structure

```
├── .env
├── README.md
├── agents
│   ├── analyzer.py
│   └── creator.py
├── prompts
│   ├── analyzing.py
│   └── creating.py
├── run.py
├── templates
│   ├── base.html
│   └── index.html
├── uploads
├── orchestrator.py
├── app.py
├── requirements.txt
```

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for accessing Google AI APIs

### Supported File Types
- Images: PNG, JPG, JPEG, GIF, BMP, WebP
- Maximum file size: 16MB

## Agent Architecture

### AnalyzerAgent
- Uses Gemini 2.0 Flash model for image analysis
- Accepts image files and optional analysis prompts
- Returns detailed descriptions and insights

### CreatorAgent
- Uses Imagen 3.0 model for image generation
- Accepts text prompts and generation parameters
- Returns generated images or descriptions

### Orchestrator
- Manages agent registration and coordination
- Handles complex workflows like the complete pipeline
- Provides agent capability discovery

## Development

### Running in Debug Mode
```bash
export FLASK_DEBUG=1
python app.py
```

### Adding New Agents
1. Create a new agent class following the existing pattern
2. Register it with the orchestrator in `app.py`
3. Add appropriate API endpoints if needed

## Error Handling

The application includes comprehensive error handling for:
- Missing API keys
- File upload errors
- API request failures
- Invalid file types
- Network timeouts

## Security Considerations

- Store API keys securely using environment variables or `.env` files
- Never commit API keys to version control
- Consider rate limiting for production deployments
- Validate all file uploads for security

## Troubleshooting

### Common Issues

1. **"API key not configured" error**
   - Ensure `GOOGLE_API_KEY` environment variable is set
   - Verify the API key has access to required services

2. **File upload failures**
   - Check file size (max 16MB)
   - Ensure file type is supported
   - Verify uploads directory exists and is writable

3. **Agent registration errors**
   - Check API key validity
   - Ensure all dependencies are installed
   - Review console output for specific error messages

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## License

This project is provided as-is for educational and development purposes.

## Support

For issues and questions, please open an issue on the GitHub repository.
