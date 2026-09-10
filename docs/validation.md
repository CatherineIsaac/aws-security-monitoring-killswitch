# Validation

## Test Identity

A dedicated IAM user, `Victim`, was configured with least-privilege access to call `secretsmanager:GetSecretValue` against the monitored secret.

## Initial Access Test

The detection pipeline was triggered using the AWS CLI:

```bash
aws secretsmanager get-secret-value \
  --secret-id Production_Database_Credentials \
  --region us-east-1 \
  --profile victim \
  --query ARN \
  --output text
```

The request succeeded.

CloudTrail recorded:

- `eventName`: `GetSecretValue`
- `userName`: `Victim`
- `awsRegion`: `us-east-1`
- `secretId`: `Production_Database_Credentials`

Both detection flows were triggered.

## Detection

### Flow 1 — CloudWatch

The CloudWatch metric filter matched the CloudTrail event and incremented `SensitiveSecretAccessCount`.

`SensitiveSecretAccessAlarm` transitioned from `OK` to `ALARM` after the configured threshold was met.

### Flow 2 — EventBridge

`SensitiveSecretAccessEventRule` matched the CloudTrail `GetSecretValue` event.

The rule forwarded the event to two targets:

1. Amazon SNS for notification
2. `SensitiveSecretKillSwitch` Lambda for containment

## Automated Containment

The Lambda function validated that the triggering identity was the designated `Victim` IAM user and applied the `QuarantineBoundary` permissions boundary.

The user's original Secrets Manager read policy remained attached, but the explicit deny in the permissions boundary restricted the user's effective permissions.

## Post-Containment Test

The same `GetSecretValue` request was issued again:

```bash
aws secretsmanager get-secret-value \
  --secret-id Production_Database_Credentials \
  --region us-east-1 \
  --profile victim \
  --query ARN \
  --output text
```

The request failed with:

```text
AccessDeniedException
```

CloudTrail recorded:

```text
eventName: GetSecretValue
errorCode: AccessDenied
```

The CloudTrail error identified the `QuarantineBoundary` permissions boundary as the source of the explicit deny.

## Observed Results

| Stage | Result |
|---|---|
| Initial `GetSecretValue` | Allowed |
| CloudWatch detection | Triggered |
| EventBridge detection | Triggered |
| SNS notification | Delivered |
| Lambda containment | Executed |
| `QuarantineBoundary` | Applied |
| Second `GetSecretValue` | `AccessDenied` |
| CloudTrail post-containment event | Confirmed |
