const apiUrl = 'https://ociit27b9c.execute-api.us-east-1.amazonaws.com/prod/';
// Your actual Cognito configuration
const poolData = {
    UserPoolId: 'us-east-1_JTP87lSRF',
    ClientId: '3aeh5e5d0rpvf41fj468rqdck3'
};

// Global variables to store authentication data
let idToken = null;

// Initialize the Cognito authentication
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

// Handle form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Set result area
    const resultArea = document.getElementById('result');
    resultArea.innerHTML = 'Authenticating...';

    // IMPORTANT CHANGE: Using ADMIN_USER_PASSWORD_AUTH or USER_PASSWORD_AUTH flow
    // instead of the default SRP flow

    const userData = {
        Username: email,
        Pool: userPool
    };

    const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

    // Use explicit authentication parameters
    const authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
        Username: email,
        Password: password
    });

    // Set authentication flow type explicitly to use USER_PASSWORD_AUTH
    const authParameters = {
        AuthFlow: 'USER_PASSWORD_AUTH',
        ClientId: poolData.ClientId
    };

    // Authenticate user with explicit parameters
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result) {
            // Get the tokens
            idToken = result.getIdToken().getJwtToken();

            // Simply log the complete JWT token to console
            console.log('JWT Token:');
            console.log(idToken);

            // Display success message
            resultArea.innerHTML = 'Successfully authenticated! Check browser console for the full JWT token (F12 > Console)';

            // Enable the API call button
            document.getElementById('callApi').style.display = 'block';
        },

        onFailure: function(err) {
            resultArea.innerHTML = 'Authentication failed: ' + err.message || JSON.stringify(err);
            console.error('Auth Error:', err);
        },

        // Use the specific auth flow that your app client supports
        authParameters: authParameters
    });
});

// Handle API call button
document.getElementById('callApi').addEventListener('click', function() {
    if (!idToken) {
        document.getElementById('apiResult').innerHTML = 'Please login first to get a token';
        return;
    }

    document.getElementById('apiResult').innerHTML = 'Calling API...';

    // Log the token being used for API call
    console.log('Using this JWT token for API call:');
    console.log(idToken);

    // Call the API with the token
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Authorization': idToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('API call failed with status: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('apiResult').innerHTML = 'API Response:<br>' + JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('apiResult').innerHTML = 'Error calling API: ' + error.message;
        console.error('API Error:', error);
    });
});

// Add a debug info section on page load
window.addEventListener('load', function() {
    console.log('App initialized with User Pool ID:', poolData.UserPoolId);
    console.log('Client ID:', poolData.ClientId);
    console.log('Target API:', apiUrl);
});