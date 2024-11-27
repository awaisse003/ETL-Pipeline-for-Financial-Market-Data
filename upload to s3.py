import boto3
import os



def upload_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket.

    Args:
        file_name (str): File to upload.
        bucket_name (str): Name of the target S3 bucket.
        object_name (str): S3 object name. Defaults to the file_name if not specified.

    Returns:
        bool: True if the upload was successful, else False.
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Create an S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id="xx",
        aws_secret_access_key="xx",
        region_name="us-east-1"
    )
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}.")
        return True
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")
        return False


# Example Usage
if __name__ == "__main__":
    csv_file = "financial_data.csv"  # Ensure this file exists locally
    s3_bucket = "financialdatastorage"  # Replace with your S3 bucket name
    upload_to_s3(csv_file, s3_bucket)