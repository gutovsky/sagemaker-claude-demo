import base64
from pathlib import Path

import aws_cdk as cdk
from aws_cdk import (
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_sagemaker as sagemaker,
)
from constructs import Construct

from stacks.config import DemoStackConfig


class DemoStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: DemoStackConfig | None = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        config = config or DemoStackConfig()

        # --- S3 Bucket ---
        bucket = s3.Bucket(
            self,
            "DemoDataBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # --- IAM Role ---
        role = iam.Role(
            self,
            "DemoNotebookRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
            ],
        )

        bucket.grant_read_write(role)

        # --- Upload Notebook to S3 ---
        notebook_dir = str(Path(__file__).resolve().parent.parent.parent / "notebooks")
        s3deploy.BucketDeployment(
            self,
            "NotebookDeployment",
            sources=[s3deploy.Source.asset(notebook_dir)],
            destination_bucket=bucket,
            destination_key_prefix="notebook",
        )

        # --- Lifecycle Configuration ---
        # Resolve paths using pathlib for cross-platform compatibility.
        infra_dir = Path(__file__).resolve().parent.parent
        repo_root = infra_dir.parent

        script_path = infra_dir / "scripts" / "on_create.sh"
        notebook_path = repo_root / "notebooks" / "demo_notebook.ipynb"
        idle_check_path = infra_dir / "scripts" / "idle_check.sh"

        try:
            on_create_script = script_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            on_create_script = "#!/bin/bash\necho 'on_create.sh placeholder'"

        # Read and base64-encode the demo notebook and idle_check script
        # so they are embedded directly in the lifecycle config.  The
        # SageMaker instance will decode them to /tmp/ before the main
        # on_create.sh logic runs.
        notebook_b64 = base64.b64encode(
            notebook_path.read_bytes()
        ).decode("ascii")

        idle_check_b64 = base64.b64encode(
            idle_check_path.read_bytes()
        ).decode("ascii")

        # Build a preamble that decodes the embedded files to /tmp/.
        embedded_preamble = (
            "#!/bin/bash\n"
            "set -e\n"
            "\n"
            "# --- Embedded files (injected by CDK at synth time) ---\n"
            f"echo '{notebook_b64}' | base64 --decode > /tmp/demo_notebook.ipynb\n"
            f"echo '{idle_check_b64}' | base64 --decode > /tmp/idle_check.sh\n"
            "chmod +x /tmp/idle_check.sh\n"
            "# --- End embedded files ---\n"
            "\n"
        )

        # Strip the original shebang / set -e lines from on_create.sh so
        # they aren't duplicated after the preamble.
        script_lines = on_create_script.splitlines(keepends=True)
        filtered_lines: list[str] = []
        for line in script_lines:
            stripped = line.strip()
            if stripped in ("#!/bin/bash", "set -e"):
                continue
            filtered_lines.append(line)
        on_create_body = "".join(filtered_lines)

        combined_script = embedded_preamble + on_create_body

        # Replace __BUCKET_NAME__ placeholder with the actual bucket name.
        # Use Fn::Sub so CloudFormation resolves the bucket name at deploy time.
        combined_script = combined_script.replace(
            "__BUCKET_NAME__", "${BucketName}"
        )
        on_create_encoded = cdk.Fn.base64(
            cdk.Fn.sub(
                combined_script,
                {"BucketName": bucket.bucket_name},
            )
        )

        lifecycle_config = sagemaker.CfnNotebookInstanceLifecycleConfig(
            self,
            "OnCreateConfig",
            on_create=[
                sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty(
                    content=on_create_encoded,
                )
            ],
        )

        # --- SageMaker Notebook Instance ---
        notebook = sagemaker.CfnNotebookInstance(
            self,
            "DemoNotebookInstance",
            instance_type=config.notebook_instance_type,
            role_arn=role.role_arn,
            volume_size_in_gb=config.notebook_volume_size_gb,
            direct_internet_access="Enabled",
            lifecycle_config_name=lifecycle_config.attr_notebook_instance_lifecycle_config_name,
        )

        # --- Stack Outputs ---
        CfnOutput(
            self,
            "NotebookInstanceUrl",
            value=cdk.Fn.join("", [
                "https://",
                notebook.attr_notebook_instance_name,
                ".notebook.",
                self.region,
                ".sagemaker.aws/tree",
            ]),
            description="URL to access the SageMaker notebook instance",
        )

        CfnOutput(
            self,
            "NotebookInstanceName",
            value=notebook.attr_notebook_instance_name,
            description="Name of the SageMaker notebook instance",
        )

        CfnOutput(
            self,
            "DataBucketName",
            value=bucket.bucket_name,
            description="Name of the S3 bucket containing the demo dataset",
        )
