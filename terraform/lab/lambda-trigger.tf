resource "aws_lambda_permission" "eventbridge_detector" {
  statement_id  = "AllowSecurityGroupChangesRule"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.public_ssh_detector.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.security_group_changes.arn
}

resource "aws_cloudwatch_event_target" "security_event_detector" {
  rule      = aws_cloudwatch_event_rule.security_group_changes.name
  target_id = "security-event-detector"
  arn       = aws_lambda_function.public_ssh_detector.arn

  depends_on = [
    aws_lambda_permission.eventbridge_detector
  ]
}
