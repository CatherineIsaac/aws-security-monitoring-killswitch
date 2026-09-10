import boto3
from botocore.exceptions import ClientError

iam = boto3.client("iam")

TARGET_USER = "Victim"
QUARANTINE_BOUNDARY_ARN = (
    "arn:aws:iam::<ACCOUNT_ID>:policy/QuarantineBoundary"
)


def lambda_handler(event, context):
    print("Received event:", event)

    identity = event.get("detail", {}).get("userIdentity", {})
    user_type = identity.get("type")
    user_name = identity.get("userName")

    # Safety guard: only act on the designated Victim IAM user
    if user_type != "IAMUser" or user_name != TARGET_USER:
        print(
            f"No action taken for user_type={user_type}, "
            f"user_name={user_name}"
        )
        return {
            "contained": False,
            "reason": "Identity is not the designated Victim user"
        }

    try:
        iam.put_user_permissions_boundary(
            UserName=TARGET_USER,
            PermissionsBoundary=QUARANTINE_BOUNDARY_ARN
        )

        print(
            f"Quarantine boundary successfully applied to {TARGET_USER}"
        )

        return {
            "contained": True,
            "user": TARGET_USER,
            "boundary": QUARANTINE_BOUNDARY_ARN
        }

    except ClientError as e:
        print("Failed to apply quarantine boundary:", e)
        raise
