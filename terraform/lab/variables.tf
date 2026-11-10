variable "aws_region" {
  description = "AWS region used by the security lab."
  type        = string
  default     = "us-east-1"
}

variable "terraform_execution_role_arn" {
  description = "ARN of the role Terraform assumes when provisioning resources."
  type        = string
  sensitive   = true

  validation {
    condition = can(
      regex(
        "^arn:aws:iam::[0-9]{12}:role/terraform-execution-role$",
        var.terraform_execution_role_arn
      )
    )

    error_message = "The value must be the ARN of terraform-execution-role."
  }
}
