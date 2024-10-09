import os
import uuid
import gradio as gr
from flask import Flask, send_from_directory

# Create an instance of Flask for serving files
app = Flask(__name__)

# Directory where uploaded files will be stored
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask route to serve files
@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Function to handle file upload in Gradio
def upload_files(files):
    file_urls = []
    for idx, file in enumerate(files):
        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}_file_{idx}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the file to the upload directory
        with open(file_path, "wb") as f:
            f.write(file)
        
        # Create a public URL for the uploaded file
        file_url = f"http://127.0.0.1:5000/files/{unique_filename}"
        file_urls.append(file_url)
    
    return file_urls

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("""
    # File Upload and Public URL Generator
    Upload one or more files, and get unique public URLs to access them.
    """)
    file_input = gr.File(label="Upload Files", file_count="multiple", type="binary")
    output = gr.JSON(label="Public URLs of Uploaded Files")
    
    file_input.upload(upload_files, inputs=file_input, outputs=output)

# Run the Gradio app with Flask integration
demo.launch(server_name="0.0.0.0", server_port=7860, inline=False)

# Start Flask server to serve files
app.run(port=5000)
