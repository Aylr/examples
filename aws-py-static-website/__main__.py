import json

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
bucket_slug = config.require("bucket_name")
SLUG = config.require("slug")
ENVIRONMENT = config.require("environment")
TAGS = config.require_object("tags")
bucket_name = f"{bucket_slug}.{ENVIRONMENT}"


def slugify(resource: str) -> str:
    return f"{SLUG}-{resource}-{ENVIRONMENT}"


# Create an S3 bucket configured as a website bucket.
bucket = aws.s3.Bucket(
    slugify("bucket"),
    bucket=bucket_name,
    acl="public-read",
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html", error_document="404.html"
    ),
    force_destroy=False,
    tags=TAGS,
)


def public_read_policy(bucketName):
    """
    Create an S3 Bucket Policy to allow public read of all objects in bucket.

    This reusable function can be pulled out into its own module.
    """
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [
                        f"arn:aws:s3:::{bucketName}/*"  # policy refers to bucket name explicitly
                    ],
                }
            ],
        }
    )


# Set the access policy for the bucket so all objects are readable
bucketPolicy = aws.s3.BucketPolicy(
    slugify("bucket-policy"),
    bucket=bucket.bucket,
    policy=bucket.bucket.apply(public_read_policy),
)

pulumi.export("bucket_url", pulumi.Output.concat("s3://", bucket.bucket))
pulumi.export("bucket_website_endpoint", bucket.website_endpoint)
