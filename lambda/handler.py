import json
import os

from detector import detect_public_ssh


def lambda_handler(event, context):
    target_group_id = os.environ["TARGET_SECURITY_GROUP_ID"]
    public_sources = detect_public_ssh(event, target_group_id)

    if not public_sources:
        return False

    finding = {
        "finding": "public_ssh_ingress",
        "group_id": target_group_id,
        "public_sources": public_sources,
        "event_id": event.get("id"),
    }
    print(json.dumps(finding))
    return True