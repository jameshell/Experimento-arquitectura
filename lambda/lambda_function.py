def lambda_handler(event, context):
    # User claims will be available in the event object
    claims = event['requestContext']['authorizer']['claims']

    # Extract user groups/roles if they exist
    groups = claims.get('cognito:groups', '')

    # Check roles and return different responses
    if 'Admins' in groups:
        return {
            'statusCode': 200,
            'body': 'Admin view: Full access granted'
        }
    elif 'Users' in groups:
        return {
            'statusCode': 200,
            'body': 'User view: Limited access granted'
        }
    else:
        return {
            'statusCode': 403,
            'body': 'Access denied: Insufficient permissions'
        }
