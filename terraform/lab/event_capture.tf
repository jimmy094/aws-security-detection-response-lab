resource "aws_cloudwatch_log_group" "security_events" {
  name              = "/aws/events/aws-security-lab"
  retention_in_days = 14
}

resource "aws_cloudwatch_event_rule" "security_group_changes" {
  name        = "aws-security-lab-sg-changes"
  description = "Capture successful inbound rule changes to the lab test group."

  event_pattern = jsonencode({
    source        = ["aws.ec2"]
    "detail-type" = ["AWS API Call via CloudTrail"]

    detail = {
      eventSource = ["ec2.amazonaws.com"]
      eventName = [
        "AuthorizeSecurityGroupIngress",
        "ModifySecurityGroupRules"
      ]

      errorCode = [{
        exists = false
      }]

      requestParameters = {
        groupId = [aws_security_group.security_test.id]
      }
    }
  })
}

data "aws_iam_policy_document" "event_capture" {
  statement {
    sid    = "AllowEventBridgeLogDelivery"
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "${aws_cloudwatch_log_group.security_events.arn}:*"
    ]

    principals {
      type = "Service"
      identifiers = [
        "events.amazonaws.com",
        "delivery.logs.amazonaws.com"
      ]
    }
  }
}

resource "aws_cloudwatch_log_resource_policy" "event_capture" {
  policy_name     = "aws-security-lab-event-capture"
  policy_document = data.aws_iam_policy_document.event_capture.json
}

resource "aws_cloudwatch_event_target" "security_event_log" {
  rule      = aws_cloudwatch_event_rule.security_group_changes.name
  target_id = "security-event-log"
  arn       = aws_cloudwatch_log_group.security_events.arn

  depends_on = [
    aws_cloudwatch_log_resource_policy.event_capture
  ]
}