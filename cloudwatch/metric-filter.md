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

## Alarm Configuration

**Alarm name:** `SensitiveSecretAccessAlarm`

| Setting | Value |
|---|---|
| Metric | `SensitiveSecretAccessCount` |
| Namespace | `SecurityMonitoringforCatherine` |
| Statistic | `Sum` |
| Period | `60 seconds` |
| Threshold | `>= 1` |
| Datapoints to alarm | `1 out of 1` |
| Missing data | Treat missing data as good / not breaching |
| SNS topic | `SensitiveSecretAccessAlerts` |

The alarm transitions to `ALARM` when at least one matching `GetSecretValue` event is detected within a one-minute evaluation period.
