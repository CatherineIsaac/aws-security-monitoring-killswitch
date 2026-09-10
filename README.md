# AWS Security Monitoring & Automated IAM Containment

Event-driven detection and automated containment pipeline for sensitive AWS Secrets Manager access.

## Architecture

### Detection Flow 1 — CloudWatch

CloudTrail → CloudWatch Logs → Metric Filter → CloudWatch Alarm → SNS

Detects `secretsmanager:GetSecretValue` events using a CloudWatch Logs metric filter. A custom metric increments on matching activity and triggers an alarm when the value reaches `>= 1` within a 60-second evaluation period.

### Detection Flow 2 — EventBridge

CloudTrail → EventBridge → SNS
                         └→ Lambda → IAM Permissions Boundary

An EventBridge rule matches `GetSecretValue` activity and sends the event to two targets:

- SNS for notification
- Lambda for automated containment

The Lambda function applies a deny-all `QuarantineBoundary` to the designated IAM identity.

## Security Controls

| Control | Implementation |
|---|---|
| API audit logging | AWS CloudTrail |
| Sensitive resource | AWS Secrets Manager honeytoken |
| Metric-based detection | CloudWatch Logs metric filter + alarm |
| Event-driven detection | Amazon EventBridge |
| Alerting | Amazon SNS |
| Automated containment | AWS Lambda |
| IAM quarantine | Permissions boundary with explicit deny |
| Post-containment verification | CloudTrail `AccessDenied` event |

## Detection Logic

Monitored API operation:

`secretsmanager:GetSecretValue`

Protected resource:

`Production_Database_Credentials`

CloudWatch alarm condition:

`SensitiveSecretAccessCount >= 1` within `60 seconds`

EventBridge processes the corresponding CloudTrail management event directly and invokes both notification and containment targets.

## Automated Containment

The containment Lambda validates the identity in the triggering CloudTrail event before taking action.

For the designated test identity, the function calls:

`iam:PutUserPermissionsBoundary`

and attaches:

`QuarantineBoundary`

The boundary contains an explicit deny across AWS actions, overriding the IAM user's existing allow policy and preventing subsequent resource access.
