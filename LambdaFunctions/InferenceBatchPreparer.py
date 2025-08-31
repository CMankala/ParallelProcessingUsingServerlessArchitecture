import json
import boto3
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda handler for the InferenceBatchPreparer.
    Lists objects in a specified S3 bucket and prefix, and
    prepares a list of payloads for the downstream inference Lambda.
    This version returns the list directly in the payload for Inline Map.

    Expects event to contain:
    {
      "input_bucket": "mankala-distilbert-inference-input-data-2025-05-17",
      "output_bucket": "mankala-distilbert-inference-output-results-2025-05-17",
      "input_prefix": "multi_dataset_inputs/local_imdb_filename/" # Use the 6 different file sources
    }

    Returns a list of payloads for the inference Lambda, like:
    [
      { "input_bucket": "...", "input_key": "...", "output_bucket": "...", "output_key": "..." },
      { "input_bucket": "...", "input_key": "...", "output_bucket": "...", "output_key": "..." },
      ...
    ]
    """
    print(f"Received event for InferenceBatchPreparer: {event}")

    input_bucket = event.get('input_bucket')
    output_bucket = event.get('output_bucket')
    input_prefix = event.get('input_prefix', '')

    if not input_bucket or not output_bucket:
        print("Error: input_bucket and output_bucket must be provided in the event.")
        raise ValueError("Missing required parameters: input_bucket or output_bucket.")

    print(f"Listing objects in s3://{input_bucket}/{input_prefix}")

    batches_to_process = [] # Initialize batches_to_process as an empty list

    try:
        # Use the S3 Paginator to handle large numbers of objects efficiently
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=input_bucket, Prefix=input_prefix)

        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    input_key = obj['Key']
                    if input_key.endswith('/'): # Skip S3 'folder' objects
                        continue

                    output_base_prefix = 'processed_results/'
                    relative_key = input_key[len(input_prefix):] if input_key.startswith(input_prefix) else input_key
                    if relative_key.startswith('/'):
                         relative_key = relative_key[1:]

                    output_key = output_base_prefix + relative_key
                    output_key = os.path.splitext(output_key)[0] + '.json'

                    batches_to_process.append({
                        "input_bucket": input_bucket,
                        "input_key": input_key,
                        "output_bucket": output_bucket,
                        "output_key": output_key
                    })

        print(f"Prepared {len(batches_to_process)} batches for processing.")
        # --- CRITICAL: RETURN THE LIST DIRECTLY FOR INLINE MAP ---
        return batches_to_process

    except Exception as e:
        print(f"Error preparing data chunks from s3://{input_bucket}/{input_prefix}: {e}", exc_info=True)
        # It's important to re-raise the exception after logging so Step Functions catches the failure
        raise e

