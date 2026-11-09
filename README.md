# AWS Security Detection and Automated Response Lab

## Why I am building this

I have experience troubleshooting production systems, building monitoring, and creating automated alerts. I wanted to apply those skills to cloud security by building something hands-on instead of only completing courses and tutorials.

This project will create a small AWS environment that can record security activity, detect specific events, send alerts, and run a controlled automated response.

## Project goal

The finished lab will:

- Deploy AWS infrastructure using Terraform
- Collect security events from AWS services
- Detect suspicious or risky activity
- Send useful alerts with investigation details
- Run a scoped Python response when appropriate
- Produce test evidence showing that each part works

## Planned event flow

```text
Safe test event
      ↓
CloudTrail / GuardDuty / logs
      ↓
EventBridge detection rule
      ↓
Python Lambda response
      ↓
Alert, evidence, and optional containment

## Repository structure

```text
terraform/             Terraform infrastructure
lambda/                Python response functions
scripts/               Testing and utility scripts
tests/                 Automated tests
docs/architecture/     Architecture diagrams
docs/evidence/         Redacted test evidence
docs/incident-reports/ Incident investigation write-ups
```

## Safety and scope

This project is built only inside my own AWS account. Testing will use AWS-provided sample findings and controlled configuration changes. It will not target systems or accounts that I do not own.
