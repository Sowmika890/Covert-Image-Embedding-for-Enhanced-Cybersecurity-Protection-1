from PIL import Image

# Convert image to binary
def image_to_binary(image):
    binary_data = []
    for pixel in list(image.getdata()):
        for value in pixel[:3]:  # Only RGB, ignore alpha if present
            binary_data.append(format(value, '08b'))  # Convert to 8-bit binary
    return ''.join(binary_data)

# Convert binary to image
def binary_to_image(binary_data, image_size):
    binary_values = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    pixel_data = [int(b, 2) for b in binary_values]

    # Ensure pixel data length is divisible by 3
    if len(pixel_data) % 3 != 0:
        raise ValueError("Binary data length is not divisible by 3, data might be corrupted.")

    image = Image.new("RGB", image_size)
    image.putdata([tuple(pixel_data[i:i + 3]) for i in range(0, len(pixel_data), 3)])
    return image

# Hide the secret image in the cover image
def hide_image(cover_image_path, secret_image_path, output_image_path):
    cover_image = Image.open(cover_image_path).convert("RGB")
    secret_image = Image.open(secret_image_path).convert("RGB")

    if cover_image.size[0] * cover_image.size[1] < secret_image.size[0] * secret_image.size[1]:
        raise ValueError("Secret image is too large to fit inside the cover image")

    cover_pixels = list(cover_image.getdata())
    secret_binary = image_to_binary(secret_image)
    modified_pixels = []
    secret_index = 0

    for pixel in cover_pixels:
        new_pixel = list(pixel)
        for i in range(3):  # Modify R, G, B values
            if secret_index < len(secret_binary):
                new_pixel[i] = (new_pixel[i] & 0xFE) | int(secret_binary[secret_index])
                secret_index += 1
        modified_pixels.append(tuple(new_pixel))

    cover_image.putdata(modified_pixels)
    cover_image.save(output_image_path)
    print("Secret image has been hidden successfully!")

# Extract the hidden image from the stego image
def extract_image(stego_image_path, secret_image_size, output_image_path):
    stego_image = Image.open(stego_image_path).convert("RGB")
    stego_pixels = list(stego_image.getdata())

    binary_data = ""
    for pixel in stego_pixels:
        for i in range(3):  # Get LSB of R, G, B values
            binary_data += str(pixel[i] & 0x01)

    # Calculate expected binary data length
    expected_length = secret_image_size[0] * secret_image_size[1] * 24  # 24 bits per pixel

    # Trim the binary data if it's too long
    if len(binary_data) > expected_length:
        binary_data = binary_data[:expected_length]

    secret_image = binary_to_image(binary_data, secret_image_size)
    secret_image.save(output_image_path)
    print("Secret image has been extracted successfully!")

# Main execution block
if __name__ == "__main__":
    # Paths to the images
    cover_image_path = "C:/Users/sowmika/OneDrive/Desktop/image_stegnography(1)/test_images/cover_image.png"
    secret_image_path = "C:/Users/sowmika/OneDrive/Desktop/image_stegnography(1)/test_images/secret_image.png"
    output_image_path = "C:/Users/sowmika/OneDrive/Desktop/image_stegnography(1)/static/output_image.png"
    
    # Hide the secret image
    hide_image(cover_image_path, secret_image_path, output_image_path)
    
    # For extraction, you need to provide the size of the secret image
    secret_image_size = (50, 50)  # Set the correct height and width for your secret image
    extracted_image_path = "C:/Users/sowmika/OneDrive/Desktop/image_stegnography(1)/static/extracted_image.png"
    
    # Extract the hidden image
    extract_image(output_image_path, secret_image_size, extracted_image_path)
