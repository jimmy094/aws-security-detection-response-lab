import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from handler import lambda_handler


class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.permission = {
            "ipProtocol": "tcp",
            "fromPort": 22,
            "toPort": 22,
            "ipRanges": {"items": [{"cidrIp": "203.0.113.10/32"}]},
        }

        self.event = {
            "id": "test-event-1",
            "source": "aws.ec2",
            "detail-type": "AWS API Call via CloudTrail",
            "detail": {
                "eventSource": "ec2.amazonaws.com",
                "eventName": "AuthorizeSecurityGroupIngress",
                "requestParameters": {
                    "groupId": "sg-example",
                    "ipPermissions": {"items": [self.permission]},
                },
            },
        }

    def test_restricted_ssh_produces_no_finding(self):
        output = io.StringIO()

        with patch.dict("os.environ", {"TARGET_SECURITY_GROUP_ID": "sg-example"}):
            with redirect_stdout(output):
                result = lambda_handler(self.event, None)

        self.assertIs(result, False)
        self.assertEqual(
            json.loads(output.getvalue()),
            {
                "result": "no_public_ssh_match",
                "event_id": "test-event-1",
                "target_group_id": "sg-example",
            },
        )

    def test_public_ssh_logs_a_finding(self):
        self.permission["ipRanges"]["items"][0]["cidrIp"] = "0.0.0.0/0"
        output = io.StringIO()

        with patch.dict("os.environ", {"TARGET_SECURITY_GROUP_ID": "sg-example"}):
            with redirect_stdout(output):
                result = lambda_handler(self.event, None)

        self.assertIs(result, True)
        self.assertEqual(
            json.loads(output.getvalue()),
            {
                "finding": "public_ssh_ingress",
                "group_id": "sg-example",
                "public_sources": ["0.0.0.0/0"],
                "event_id": "test-event-1",
            },
        )