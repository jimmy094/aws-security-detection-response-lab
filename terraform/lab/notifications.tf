resource "aws_sns_topic" "security_findings" {
  name = "aws-security-lab-findings"
}

resource "aws_sns_topic_subscription" "alert_email" {
  topic_arn = aws_sns_topic.security_findings.arn
  protocol  = "email"
  endpoint  = var.alert_email
}
