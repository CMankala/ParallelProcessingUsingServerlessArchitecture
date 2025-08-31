import json
import os

def lambda_handler(event, context):
    print("--- Inference Batch Error Detected ---")
    print(f"Lambda Request ID: {context.aws_request_id}")
    print(f"Function Name: {context.function_name}")
    print(f"Remaining Time in Milliseconds: {context.get_remaining_time_in_millis()}")

    print("Error Event Details (full payload from Step Functions):")
    print(json.dumps(event, indent=2))

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Error details logged by InferenceErrorHandler"})
    }