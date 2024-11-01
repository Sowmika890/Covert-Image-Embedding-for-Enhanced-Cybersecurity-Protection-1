from flask import Flask, render_template, request, redirect, url_for
import os
from steganography import hide_image, extract_image

app = Flask(__name__)

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for hiding the secret image
@app.route('/hide', methods=['POST'])
def hide():
    if 'cover_image' not in request.files or 'secret_image' not in request.files:
        return 'No file part'
    
    cover_image = request.files['cover_image']
    secret_image = request.files['secret_image']
    
    cover_image_path = os.path.join('test_images', cover_image.filename)
    secret_image_path = os.path.join('test_images', secret_image.filename)
    output_image_path = os.path.join('static', 'output_image.png')
    
    # Save uploaded files
    cover_image.save(cover_image_path)
    secret_image.save(secret_image_path)
    
    # Hide the secret image
    hide_image(cover_image_path, secret_image_path, output_image_path)
    
    # Render the result template with the path to the output image
    return render_template('result.html', output_image=output_image_path)

# Route for extracting the secret image
@app.route('/extract', methods=['POST'])
def extract():
    if 'stego_image' not in request.files or 'width' not in request.form or 'height' not in request.form:
        return 'Missing required information'
    
    stego_image = request.files['stego_image']
    stego_image_path = os.path.join('test_images', stego_image.filename)
    output_image_path = os.path.join('static', 'extracted_image.png')

    # Save the uploaded stego image
    stego_image.save(stego_image_path)
    
    # Get secret image size from the form
    secret_image_size = (int(request.form['width']), int(request.form['height']))

    # Extract the secret image
    extract_image(stego_image_path, secret_image_size, output_image_path)
    
    # Render the result template with the extracted image
    return render_template('result.html', output_image=output_image_path)

if __name__ == '__main__':
    app.run(debug=True)
