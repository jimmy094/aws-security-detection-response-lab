def public_ssh_sources(permission):
    """Return internet-wide source ranges that can reach TCP port 22."""
    protocol = str(permission["ipProtocol"]).lower()

    if protocol == "-1":
        # All protocols includes TCP, regardless of the port fields.
        allows_ssh = True
    elif protocol in {"tcp", "6"}:
        allows_ssh = permission["fromPort"] <= 22 <= permission["toPort"]
    else:
        allows_ssh = False

    if not allows_ssh:
        return []

    sources = []
    for item in permission.get("ipRanges", {}).get("items", []):
        if item["cidrIp"] == "0.0.0.0/0":
            sources.append(item["cidrIp"])

    for item in permission.get("ipv6Ranges", {}).get("items", []):
        if item["cidrIpv6"] == "::/0":
            sources.append(item["cidrIpv6"])

    return sources

def detect_public_ssh(event, target_group_id):
    """Return internet-wide SSH sources from a successful ingress addition."""
    detail = event.get("detail") or {}
    if (
        event.get("source") != "aws.ec2"
        or detail.get("eventName") != "AuthorizeSecurityGroupIngress"
        or detail.get("errorCode")
    ):
        return []

    request = detail.get("requestParameters") or {}
    if not target_group_id or request.get("groupId") != target_group_id:
        return []

    matches = []
    for permission in (request.get("ipPermissions") or {}).get("items", []):
        matches.extend(public_ssh_sources(permission))
    return matches