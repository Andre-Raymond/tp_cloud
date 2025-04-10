import json
import boto3
import os

sqs = boto3.client('sqs')
output_url = os.getenv("OUTPUT_QUEUE_URL")

def lambda_handler(event, context):
    print("Received event:", event)
    for record in event["Records"]:
        message = json.loads(record["body"])
        number1 = message.get("number1")
        number2 = message.get("number2")
        op = message.get("operation")

        if op == "+":
            result = number1 + number2
        elif op == "-":
            result = number1 - number2
        elif op == "*":
            result = number1 * number2
        elif op == "/":
            if number2 == 0:
            result = "Erreur : division par zéro"
        else:
            result = number1 / number2
        else:
            result = "Operation non supportée"

        print(f"Result: {result}")

        sqs.send_message(
            QueueUrl=output_url,
            MessageBody=json.dumps({
                "inputs": [number1, number2],
                "operation": op,
                "result": result
            })
        )

    return {
        "statusCode": 200,
        "body": json.dumps("All messages processed")
    }
