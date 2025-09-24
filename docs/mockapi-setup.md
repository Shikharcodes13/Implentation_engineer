# MockAPI.io Setup Guide

This guide will help you set up MockAPI.io for the customer creation endpoint.

## Step 1: Create MockAPI.io Account

1. Go to [MockAPI.io](https://mockapi.io/)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create New Project

1. Click "Create New Project"
2. Name your project: "CSV Customer System"
3. Click "Create Project"

## Step 3: Define Customer Resource

1. Click "Add Resource"
2. Name the resource: "customers"
3. Add the following fields:

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | String | Auto-generated | Unique identifier |
| name | String | Yes | Customer company name |
| email | String | Yes | Primary contact email |
| firstName | String | Yes | Contact first name |
| lastName | String | Yes | Contact last name |
| phone | String | No | Phone number |
| address | String | No | Street address |
| city | String | No | City |
| country | String | No | Country |
| postalCode | String | No | Postal/ZIP code |
| taxId | String | No | Tax identification |
| companySize | String | No | Company size range |
| createdAt | String | Auto-generated | Creation timestamp |

4. Click "Create Resource"

## Step 4: Configure API Settings

1. Go to "Settings" tab
2. Note down your API URL (format: `https://<project-id>.mockapi.io/api/v1/`)
3. Enable CORS if needed
4. Set rate limiting as desired (default is usually sufficient)

## Step 5: Test the Endpoint

You can test your endpoint using curl:

```bash
# Test GET request
curl -X GET "https://<your-project-id>.mockapi.io/api/v1/customers"

# Test POST request
curl -X POST "https://<your-project-id>.mockapi.io/api/v1/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Company",
    "email": "test@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+1-555-0100",
    "address": "123 Test St",
    "city": "Test City",
    "country": "USA",
    "postalCode": "12345"
  }'
```

## Step 6: Configure Windmill Integration

1. In your Windmill environment variables, set:
   ```
   MOCKAPI_BASE_URL=https://<your-project-id>.mockapi.io/api/v1
   MOCKAPI_API_KEY=<your-api-key-if-needed>
   ```

2. Update the API integration script with your endpoint URL

## Expected Response Format

The MockAPI endpoint should return responses in this format:

### Success Response (201 Created)
```json
{
  "id": "1",
  "name": "Acme Corp",
  "email": "john.doe@acme.com",
  "firstName": "John",
  "lastName": "Doe",
  "phone": "+1-555-0100",
  "address": "123 Business St",
  "city": "New York",
  "country": "USA",
  "postalCode": "10001",
  "taxId": "TAX-123456",
  "companySize": "50-100",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Validation failed",
  "message": "Required field 'email' is missing"
}
```

## Troubleshooting

### Issue: CORS Errors
- Enable CORS in MockAPI.io settings
- Ensure your Windmill instance can make external requests

### Issue: Rate Limiting
- MockAPI.io free tier has rate limits
- Consider upgrading or implementing request queuing

### Issue: Authentication
- MockAPI.io free tier doesn't require authentication
- If using paid tier, configure API key in Windmill

## Security Considerations

- MockAPI.io is for development/testing only
- Don't store sensitive real customer data
- Use environment variables for API URLs
- Consider implementing request validation

## Next Steps

After MockAPI.io is configured:

1. Test the endpoint with sample data
2. Configure Windmill scripts with your API URL
3. Import the CSV processing flows
4. Run end-to-end tests
