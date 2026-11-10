data "aws_caller_identity" "current" {}

check "terraform_execution_role_is_active" {
  assert {
    condition = strcontains(
      data.aws_caller_identity.current.arn,
      "assumed-role/terraform-execution-role/"
    )

    error_message = "Terraform did not authenticate through terraform-execution-role."
  }
}

output "execution_role_verified" {
  description = "Confirms that the AWS provider authenticated through the execution role."
  value = strcontains(
    data.aws_caller_identity.current.arn,
    "assumed-role/terraform-execution-role/"
  )
}

output "configured_region" {
  description = "AWS region configured for the lab."
  value       = var.aws_region
}
