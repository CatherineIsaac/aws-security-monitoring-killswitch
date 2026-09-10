# CloudWatch Sensitive Secret Detection

## Metric Filter

**Filter name:** `SensitiveSecretAccessFilter`

**Log source:** AWS CloudTrail

**Filter pattern:**

```text
{ ($.eventSource = "secretsmanager.amazonaws.com") && ($.eventName = "GetSecretValue") && ($.requestParameters.secretId = "Production_Database_Credentials") }
```

## Metric Transformation

| Setting | Value |
|---|---|
| Namespace | `SecurityMonitoringforCatherine` |
| Metric name | `SensitiveSecretAccessCount` |
| Metric value | `1` |
| Default value | `0` |

The filter increments `SensitiveSecretAccessCount` when CloudTrail records a `GetSecretValue` request for `Production_Database_Credentials`.
