import boto3
from botocore.exceptions import ClientError


# Create S3 client using configured AWS credentials
s3 = boto3.client("s3")


def list_buckets():
    """
    Returns a list of all S3 buckets.
    """
    response = s3.list_buckets()
    return response.get("Buckets", [])

def create_bucket(bucket_name, region="ap-south-1"):
    """
    Creates an S3 bucket in the specified region.
    """
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            "LocationConstraint": region
        }
    )
    
def list_objects(bucket_name):
    """
    Lists all objects inside a bucket.
    """
    response = s3.list_objects_v2(Bucket=bucket_name)
    return response.get("Contents", [])

def upload_file(bucket_name, file_obj, object_name):
    """
    Uploads a file object to S3.
    """
    s3.upload_fileobj(file_obj, bucket_name, object_name)

def delete_object(bucket_name, object_name):
    """
    Deletes an object from S3.
    """
    s3.delete_object(Bucket=bucket_name, Key=object_name)

def create_folder(bucket_name, folder_name):
    """
    Creates a folder in S3 by creating an empty object with '/'.
    """
    if not folder_name.endswith("/"):
        folder_name += "/"

    s3.put_object(Bucket=bucket_name, Key=folder_name)

    
def copy_object(src_bucket, src_key, dest_bucket, dest_key):
    """
    Copies an object from source to destination.
    Raises meaningful errors if operation fails.
    """
    try:
        copy_source = {
            "Bucket": src_bucket,
            "Key": src_key
        }

        s3.copy_object(
            CopySource=copy_source,
            Bucket=dest_bucket,
            Key=dest_key
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "NoSuchKey":
            raise ValueError("Source file does not exist.")

        elif error_code == "NoSuchBucket":
            raise ValueError("Source or destination bucket does not exist.")

        elif error_code == "AccessDenied":
            raise ValueError("Access denied. Check permissions.")

        else:
            raise ValueError(f"S3 Error: {error_code}")



def move_object(src_bucket, src_key, dest_bucket, dest_key):
    """
    Moves an object (copy + delete).
    """
    copy_object(src_bucket, src_key, dest_bucket, dest_key)
    delete_object(src_bucket, src_key)


def is_bucket_empty(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    return "Contents" not in response


def delete_bucket_with_contents(bucket_name):
    # Delete all objects first
    response = s3.list_objects_v2(Bucket=bucket_name)

    if "Contents" in response:
        for obj in response["Contents"]:
            s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

    # Now delete bucket
    s3.delete_bucket(Bucket=bucket_name)

def delete_folder(bucket_name, folder_prefix):
    """
    Deletes a folder and all its contents in S3.
    """
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=folder_prefix
    )

    if "Contents" in response:
        for obj in response["Contents"]:
            s3.delete_object(
                Bucket=bucket_name,
                Key=obj["Key"]
            )
def folder_has_files(bucket_name, folder_prefix):
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=folder_prefix
    )

    if "Contents" not in response:
        return False

    # If more than 1 → contains files (not just folder itself)
    return len(response["Contents"]) > 1