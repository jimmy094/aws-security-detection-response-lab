resource "aws_vpc" "security_test" {
  cidr_block = "10.77.0.0/24"

  tags = {
    Name    = "aws-security-lab-test-vpc"
    Purpose = "Isolated security detection tests"
  }
}

resource "aws_security_group" "security_test" {
  name_prefix = "aws-security-lab-test-"
  description = "Unattached security group for controlled detection tests"
  vpc_id      = aws_vpc.security_test.id

  ingress = []
  egress  = []

  tags = {
    Name            = "aws-security-lab-test-sg"
    Purpose         = "Security detection test target"
    SecurityLabTest = "true"
  }
}

output "test_security_group_id" {
  description = "Security group used for controlled rule-change tests."
  value       = aws_security_group.security_test.id
}
