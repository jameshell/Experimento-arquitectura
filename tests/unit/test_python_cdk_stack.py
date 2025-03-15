import boto3
import json
import base64
import pytest

# Configuration - you would replace these with your actual values
USER_POOL_ID = "us-east-1_JTP87lSRF"  # From your deployed stack
CLIENT_ID = "3aeh5e5d0rpvf41fj468rqdck3"  # From your deployed stack
TEST_USERNAME = "jaimea111@gmail.com"
TEST_PASSWORD = "YourStrongPassword123!"
EXPECTED_ROLE = "Admins"  # The role you expect the user to have


def test_user_authentication_and_role():
    """
    Test that:
    1. User can authenticate successfully
    2. User has the expected role
    3. JWT token is returned and can be printed
    """
    # Create Cognito client
    cognito_client = boto3.client('cognito-idp')

    # Authenticate the user
    try:
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': TEST_USERNAME,
                'PASSWORD': TEST_PASSWORD
            }
        )

        # Check that we received tokens
        assert 'AuthenticationResult' in response, "Authentication failed - no AuthenticationResult in response"
        assert 'IdToken' in response['AuthenticationResult'], "No ID token in response"

        # Get the ID token (JWT)
        id_token = response['AuthenticationResult']['IdToken']

        # Print the full JWT
        print("\nFull JWT token:")
        print(id_token)

        # Parse and print the JWT payload
        token_parts = id_token.split('.')
        assert len(token_parts) == 3, "JWT token should have 3 parts"

        # Decode the payload part (second part)
        padded_payload = token_parts[1] + '=' * (-len(token_parts[1]) % 4)  # Add padding if needed
        payload = json.loads(base64.b64decode(padded_payload).decode('utf-8'))

        # Print the decoded payload in a readable format
        print("\nDecoded JWT payload:")
        print(json.dumps(payload, indent=2))

        # Check if user has the expected role
        # The claim containing roles might vary depending on your Cognito setup
        # Common locations: 'cognito:groups', 'custom:role', or a custom attribute

        # Option 1: Check in cognito:groups
        if 'cognito:groups' in payload:
            assert EXPECTED_ROLE in payload['cognito:groups'], f"User does not have the expected role: {EXPECTED_ROLE}"
            print(f"\nUser has the expected role '{EXPECTED_ROLE}' in cognito:groups")

        # Option 2: Check in custom role attribute
        elif 'custom:role' in payload:
            assert payload['custom:role'] == EXPECTED_ROLE, f"User does not have the expected role: {EXPECTED_ROLE}"
            print(f"\nUser has the expected role '{EXPECTED_ROLE}' in custom:role")

        # Option 3: Using a specific claim your setup might use
        # elif 'your-custom-role-claim' in payload:
        #     assert EXPECTED_ROLE in payload['your-custom-role-claim'], f"User does not have the expected role: {EXPECTED_ROLE}"

        else:
            # If you're not sure where roles are stored, print a warning
            print("\nWARNING: Could not find a role claim to verify the expected role")
            print("Available claims:", list(payload.keys()))

        print("\nAuthentication test passed successfully!")
        return payload  # Return the payload for any further verification if needed

    except Exception as e:
        print(f"\nAuthentication failed with error: {str(e)}")
        raise
