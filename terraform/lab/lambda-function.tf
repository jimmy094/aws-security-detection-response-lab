locals {
  detector_zip_path = "${path.module}/../../build/public-ssh-detector.zip"
}

resource "aws_lambda_function" "public_ssh_detector" {
  function_name    = "aws-security-lab-public-ssh-detector"
  role             = aws_iam_role.detector_lambda.arn
  runtime          = "python3.13"
  handler          = "handler.lambda_handler"
  filename         = local.detector_zip_path
  source_code_hash = filebase64sha256(local.detector_zip_path)

  environment {
    variables = {
      TARGET_SECURITY_GROUP_ID = aws_security_group.security_test.id
    }
  }

  depends_on = [aws_iam_role_policy_attachment.detector_lambda_logs]
}
