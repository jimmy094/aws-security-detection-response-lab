import unittest

from detector import public_ssh_sources


def tcp_rule(start, end, ipv4):
    return {
        "ipProtocol": "tcp",
        "fromPort": start,
        "toPort": end,
        "ipRanges": {"items": [{"cidrIp": ipv4}]},
    }


class PublicSSHTests(unittest.TestCase):
    def test_captured_lab_rule_is_not_internet_wide(self):
        rule = tcp_rule(22, 22, "203.0.113.10/32")
        self.assertEqual(public_ssh_sources(rule), [])

    def test_public_ipv4_ssh_is_flagged(self):
        rule = tcp_rule(22, 22, "0.0.0.0/0")
        self.assertEqual(public_ssh_sources(rule), ["0.0.0.0/0"])

    def test_port_range_that_includes_ssh_is_flagged(self):
        rule = tcp_rule(20, 25, "0.0.0.0/0")
        self.assertEqual(public_ssh_sources(rule), ["0.0.0.0/0"])

    def test_all_protocols_from_public_ipv6_is_flagged(self):
        rule = {
            "ipProtocol": "-1",
            "ipv6Ranges": {"items": [{"cidrIpv6": "::/0"}]},
        }
        self.assertEqual(public_ssh_sources(rule), ["::/0"])

    def test_restricted_ssh_and_public_https_do_not_combine(self):
        rules = [
            tcp_rule(22, 22, "203.0.113.10/32"),
            tcp_rule(443, 443, "0.0.0.0/0"),
        ]
        findings = [source for rule in rules for source in public_ssh_sources(rule)]
        self.assertEqual(findings, [])