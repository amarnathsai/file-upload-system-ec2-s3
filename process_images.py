import boto3
from PIL import Image

BUCKET_NAME = "image-processing-amarnath"
INPUT_PREFIX = "Input/"
OUTPUT_PREFIX = "Output/"

s3 = boto3.client("s3")


def process_image(key):
    filename = key.split("/")[-1]
    download_path = f"/tmp/{filename}"
    output_path = f"/tmp/processed-{filename}"

    print(f"Downloading: {key}")
    s3.download_file(BUCKET_NAME, key, download_path)

    print("Processing image...")
    img = Image.open(download_path)

    # Resize image
    img = img.resize((400, 400))

    # Save compressed image
    img.save(output_path, optimize=True, quality=60)

    output_key = OUTPUT_PREFIX + "processed-" + filename

    print(f"Uploading processed image to: {output_key}")
    s3.upload_file(output_path, BUCKET_NAME, output_key)

    print("Done")


def main():
    print("Listing input images...")

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=INPUT_PREFIX
    )

    if "Contents" not in response:
        print("No images found in Input/")
        return

    for obj in response["Contents"]:
        key = obj["Key"]

        if key.endswith("/"):
            continue

        process_image(key)


if __name__ == "__main__":
    main()