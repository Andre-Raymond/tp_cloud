from constructs import Construct
from cdktf import App, TerraformStack, TerraformAsset, AssetType
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.lambda_event_source_mapping import LambdaEventSourceMapping
from cdktf_cdktf_provider_aws.sqs_queue import SqsQueue
from cdktf_cdktf_provider_aws.cloudwatch_log_group import CloudwatchLogGroup

# Socard André-Raymond
class GradedLabStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Fournisseur AWS
        AwsProvider(self, "AWS", region="us-east-1")

        # File SQS entrée
        input_queue = SqsQueue(self, "InputQueue", name="lab-input-queue")

        # File SQS sortie
        output_queue = SqsQueue(self, "OutputQueue", name="lab-output-queue")

        # Fichier Lambda
        asset = TerraformAsset(self, "LambdaCode",
            path="lambda",  
            type=AssetType.ARCHIVE
        )

        # Lambda avec rôle existant
        lambda_function = LambdaFunction(self, "LabLambda",
            function_name="sqs-processor",
            runtime="python3.9",
            handler="index.lambda_handler",
            filename=asset.path,
            role="arn:aws:iam::177000578119:role/LabRole",  # Utilise le rôle existant
            environment={
                "variables": {
                    "OUTPUT_QUEUE_URL": output_queue.url
                }
            }
        )

        # Trigger SQS
        LambdaEventSourceMapping(self, "EventSourceMapping",
            event_source_arn=input_queue.arn,
            function_name=lambda_function.arn
        )

# Déploiement de la stack
app = App()
GradedLabStack(app, "graded_lab")
app.synth()
