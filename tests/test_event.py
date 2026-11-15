import unittest

from detector import detect_public_ssh


class IngressEventTests(unittest.TestCase):
    def setUp(self):
        self.group_id = "sg-lab-example"
        self.event = {
            "source": "aws.ec2",
            "detail": {
                "eventName": "AuthorizeSecurityGroupIngress",
                "requestParameters": {
                    "groupId": self.group_id,
                    "ipPermissions": {
                        "items": [{
                            "ipProtocol": "tcp",
                            "fromPort": 22,
                            "toPort": 22,
                            "ipRanges": {"items": [{"cidrIp": "0.0.0.0/0"}]},
                        }]
                    },
                },
            },
        }

    def test_finds_public_ssh_in_lab_event(self):
        self.assertEqual(
            detect_public_ssh(self.event, self.group_id), ["0.0.0.0/0"]
        )

    def test_ignores_a_different_group(self):
        self.assertEqual(detect_public_ssh(self.event, "sg-other"), [])

    def test_denied_request_is_not_a_rule_change(self):
        self.event["detail"]["errorCode"] = "Client.UnauthorizedOperation"
        self.assertEqual(detect_public_ssh(self.event, self.group_id), [])