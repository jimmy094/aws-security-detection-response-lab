provider "aws" {
  region = var.aws_region

  assume_role {
    role_arn     = var.terraform_execution_role_arn
    session_name = "aws-security-lab-terraform"
  }

  default_tags {
    tags = {
      Project     = "aws-security-detection-response-lab"
      Environment = "lab"
      ManagedBy   = "Terraform"
    }
  }
}
