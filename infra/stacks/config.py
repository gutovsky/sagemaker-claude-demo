from dataclasses import dataclass


@dataclass
class DemoStackConfig:
    """Configuration for the demo CDK stack."""

    stack_name: str = "SageMakerAiAgentDemo"
    notebook_instance_type: str = "ml.t3.medium"
    notebook_volume_size_gb: int = 20
    dataset_url: str = (
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )
    dataset_s3_key: str = "data/titanic.csv"
    idle_timeout_minutes: int = 60
