import boto3
import os

# Load environment variables from .env file if using dotenv
#from dotenv import load_dotenv
#load_dotenv()

# S3 bucket name
s3_bucket_name = os.getenv('S3_BUCKET_NAME')

# Initialize S3 client
s3 = boto3.client('s3')

def upload_image_to_s3(image_path):
    try:
        # Extract file name from path
        file_name = os.path.basename(image_path)
        
        # Specify S3 object key (use a unique name or prefix if necessary)
        object_key = file_name
        
        # Upload the file to S3 bucket
        with open(image_path, 'rb') as file:
            s3.put_object(Bucket=s3_bucket_name, Key=object_key, Body=file)
        
        # Print success message
        print(f"Image uploaded to S3: s3://{s3_bucket_name}/{object_key}")
    
    except Exception as e:
        print(f"Error uploading image to S3: {e}")

if __name__ == "__main__":
    # Path to the image file to upload
    image_path = 'shi.jpg'  # Replace with your actual image file path
    
    # Call function to upload image to S3
    upload_image_to_s3(image_path)
