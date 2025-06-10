import os
from flask import Flask, jsonify, render_template_string
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML template for displaying configs
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>K8s ConfigMap & Secret Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 30px; }
        .config-item {
            margin: 10px 0;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 4px;
        }
        .key { font-weight: bold; color: #0066cc; }
        .value { color: #333; }
        .secret { color: #cc0000; }
        .timestamp { color: #999; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kubernetes ConfigMap & Secret Demo</h1>
        <p class="timestamp">Generated at: {{ timestamp }}</p>
        
        <h2>ConfigMap Values (from Environment Variables)</h2>
        {% for key, value in configmap_env.items() %}
        <div class="config-item">
            <span class="key">{{ key }}:</span> <span class="value">{{ value }}</span>
        </div>
        {% endfor %}
        
        <h2>Secret Values (from Environment Variables)</h2>
        {% for key, value in secret_env.items() %}
        <div class="config-item">
            <span class="key">{{ key }}:</span> <span class="value secret">{{ value }}</span>
        </div>
        {% endfor %}
        
        <h2>ConfigMap Files (from Volume Mount)</h2>
        {% for filename, content in configmap_files.items() %}
        <div class="config-item">
            <span class="key">{{ filename }}:</span><br>
            <pre class="value">{{ content }}</pre>
        </div>
        {% endfor %}
        
        <h2>Secret Files (from Volume Mount)</h2>
        {% for filename, content in secret_files.items() %}
        <div class="config-item">
            <span class="key">{{ filename }}:</span><br>
            <pre class="value secret">{{ content }}</pre>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

def get_env_configs():
    """Get ConfigMap values from environment variables"""
    configs = {}
    # Look for environment variables that start with APP_CONFIG_
    for key, value in os.environ.items():
        if key.startswith('APP_CONFIG_'):
            configs[key] = value
    return configs

def get_env_secrets():
    """Get Secret values from environment variables"""
    secrets = {}
    # Look for environment variables that start with APP_SECRET_
    for key, value in os.environ.items():
        if key.startswith('APP_SECRET_'):
            secrets[key] = value
    return secrets

def read_mounted_files(path):
    """Read files from a mounted volume"""
    files = {}
    if os.path.exists(path):
        try:
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as f:
                        files[filename] = f.read()
        except Exception as e:
            logger.error(f"Error reading files from {path}: {e}")
            files['error'] = str(e)
    else:
        files['error'] = f"Path {path} does not exist"
    return files

@app.route('/')
def index():
    """Main page showing all configurations"""
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'configmap_env': get_env_configs(),
        'secret_env': get_env_secrets(),
        'configmap_files': read_mounted_files('/etc/config'),
        'secret_files': read_mounted_files('/etc/secrets')
    }
    return render_template_string(HTML_TEMPLATE, **data)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/config')
def api_config():
    """API endpoint returning all configurations as JSON"""
    return jsonify({
        'configmap_env': get_env_configs(),
        'secret_env': get_env_secrets(),
        'configmap_files': read_mounted_files('/etc/config'),
        'secret_files': read_mounted_files('/etc/secrets')
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)