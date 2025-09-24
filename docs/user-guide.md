# User Guide - CSV Upload System

This guide explains how to use the CSV upload system for processing customer data.

## Overview

The CSV Upload System allows you to upload customer data in CSV format, apply customizable transformations, and create customers via a mock API service. The system provides comprehensive error handling and detailed processing reports.

## Getting Started

### Prerequisites

- Windmill instance running locally (see [Setup Guide](setup-guide.md))
- MockAPI.io endpoint configured (see [MockAPI Setup](mockapi-setup.md))
- CSV file with customer data

### Required CSV Format

Your CSV file should include the following columns:

| Column Name | Required | Description | Example |
|-------------|----------|-------------|---------|
| company_name | Yes | Company or organization name | "Acme Corp" |
| contact_email | Yes | Primary contact email address | "john@acme.com" |
| contact_first_name | Yes | Contact person's first name | "John" |
| contact_last_name | Yes | Contact person's last name | "Doe" |
| phone_number | No | Phone number | "+1-555-0100" |
| address | No | Street address | "123 Business St" |
| city | No | City | "New York" |
| country | No | Country | "USA" |
| postal_code | No | Postal/ZIP code | "10001" |
| tax_id | No | Tax identification number | "TAX-123456" |
| company_size | No | Company size range | "50-100" |

### Sample CSV Format

```csv
company_name,contact_email,contact_first_name,contact_last_name,phone_number,address,city,country,postal_code,tax_id,company_size
Acme Corp,john.doe@acme.com,John,Doe,+1-555-0100,123 Business St,New York,USA,10001,TAX-123456,50-100
Beta Inc,jane@beta.co,Jane,Smith,555.0200,456 Commerce Ave,San Francisco,USA,94105,TAX-789012,100-500
```

## Using the System

### Step 1: Access Windmill

1. Open your browser and navigate to `http://localhost` (or your configured port)
2. Log in to your Windmill account
3. Navigate to the "Flows" section

### Step 2: Import the CSV Upload Flow

1. In Windmill, go to "Flows" → "Import Flow"
2. Upload the flow definition from the `flows/` directory
3. Verify that all required scripts are imported

### Step 3: Configure API Endpoint

1. Open the CSV Upload Flow
2. Navigate to the API Client script configuration
3. Set your MockAPI.io endpoint URL:
   ```
   https://your-project-id.mockapi.io/api/v1
   ```
4. Save the configuration

### Step 4: Upload and Process CSV

1. Prepare your CSV file with customer data
2. In the CSV Upload Flow, click "Run"
3. Upload your CSV file or paste CSV content
4. Click "Execute" to start processing

### Step 5: Review Results

After processing completes, you'll see:

- **Quick Summary**: Overall success rate and key statistics
- **Detailed Report**: Comprehensive processing information
- **Error Details**: Any issues encountered during processing
- **API Results**: Successful customer creations and failures

## Understanding the Results

### Success Indicators

- ✅ **Green checkmark**: Processing completed successfully
- **Success Rate**: Percentage of rows processed successfully
- **API Calls**: Number of customers created via API

### Error Indicators

- ❌ **Red X**: Processing failed or encountered errors
- **Error Details**: Specific information about what went wrong
- **Failed Rows**: List of rows that couldn't be processed

### Processing Stages

The system processes your data in four stages:

1. **CSV Parsing**: Validates and parses your CSV file
2. **Data Transformation**: Converts CSV data to customer objects
3. **API Integration**: Creates customers via MockAPI.io
4. **Error Handling**: Generates comprehensive reports

## Common Issues and Solutions

### Issue: CSV Parsing Errors

**Symptoms:**
- "CSV parsing failed" error
- Empty or malformed data

**Solutions:**
1. Check CSV format - ensure proper headers and commas
2. Verify file encoding (try UTF-8)
3. Check for special characters in data
4. Ensure no empty rows at the beginning

### Issue: Validation Errors

**Symptoms:**
- "Validation failed" messages
- Missing required fields

**Solutions:**
1. Ensure all required fields are present:
   - company_name
   - contact_email
   - contact_first_name
   - contact_last_name
2. Check email format (must be valid email address)
3. Verify phone number format if provided

### Issue: API Errors

**Symptoms:**
- "API call failed" messages
- Network timeout errors

**Solutions:**
1. Verify MockAPI.io endpoint URL is correct
2. Check internet connection
3. Ensure MockAPI.io service is running
4. Check API rate limits

### Issue: Transformation Errors

**Symptoms:**
- "Transformation failed" messages
- Data format issues

**Solutions:**
1. Check for special characters in data
2. Ensure data types are correct
3. Verify field mappings match your CSV headers

## Best Practices

### CSV File Preparation

1. **Use UTF-8 encoding** for international characters
2. **Include headers** in the first row
3. **Remove empty rows** at the beginning or end
4. **Validate email addresses** before upload
5. **Use consistent phone number formats**

### Data Quality

1. **Required fields**: Ensure all required fields have values
2. **Email validation**: Use valid email addresses
3. **Phone numbers**: Use consistent format (e.g., +1-555-0100)
4. **Company names**: Avoid special characters that might cause issues

### Processing Large Files

1. **Batch processing**: Process files in smaller batches (100-500 rows)
2. **Monitor progress**: Check processing reports regularly
3. **Error handling**: Review and fix errors before reprocessing
4. **Backup data**: Keep original CSV files as backup

## Advanced Features

### Custom Transformations

For advanced users, you can customize transformation rules:

1. **Field Mapping**: Map CSV columns to different output fields
2. **Validation Rules**: Add custom validation logic
3. **Data Cleaning**: Apply custom data cleaning functions
4. **Business Logic**: Add company-specific processing rules

See the [Developer Guide](developer-guide.md) for detailed customization instructions.

### Error Recovery

The system includes robust error recovery:

1. **Row-level errors**: Individual row failures don't stop processing
2. **Retry logic**: Automatic retry for transient API errors
3. **Detailed logging**: Comprehensive error information for debugging
4. **Partial success**: Process valid rows even if some fail

## Monitoring and Reporting

### Processing Reports

After each run, you'll receive:

1. **Summary Statistics**:
   - Total rows processed
   - Success/failure rates
   - Processing time

2. **Error Analysis**:
   - Error types and frequencies
   - Failed row details
   - Recovery suggestions

3. **API Results**:
   - Successful customer creations
   - Failed API calls
   - Retry information

### Export Options

Reports can be exported in multiple formats:

1. **JSON**: Machine-readable format for integration
2. **Text Summary**: Human-readable summary
3. **CSV**: Failed rows for manual review

## Troubleshooting

### System Issues

1. **Windmill not responding**: Check Docker containers are running
2. **Import errors**: Verify all scripts are properly imported
3. **Permission errors**: Check file permissions and access rights

### Data Issues

1. **Encoding problems**: Try different file encodings
2. **Delimiter issues**: Ensure consistent comma separation
3. **Format inconsistencies**: Standardize data formats

### API Issues

1. **Authentication errors**: Verify API credentials
2. **Rate limiting**: Reduce batch size or add delays
3. **Network issues**: Check connectivity and firewall settings

## Support

### Getting Help

1. **Documentation**: Check the [Developer Guide](developer-guide.md) for technical details
2. **Error Messages**: Read error details carefully for specific guidance
3. **Sample Data**: Use provided sample CSV for testing
4. **Logs**: Check Windmill logs for detailed error information

### Reporting Issues

When reporting issues, include:

1. **Error messages**: Copy exact error text
2. **CSV sample**: Provide a few rows of your data (sanitized)
3. **Configuration**: Your API endpoint and settings
4. **Steps to reproduce**: Detailed steps that led to the issue

## Sample Workflows

### Basic Customer Import

1. Prepare CSV with required fields
2. Upload to Windmill
3. Configure API endpoint
4. Run processing
5. Review results and fix any errors
6. Reprocess if needed

### Large File Processing

1. Split large CSV into smaller files (500 rows each)
2. Process each file separately
3. Monitor results and fix common errors
4. Combine successful results
5. Handle remaining errors manually

### Error Recovery Workflow

1. Review processing report
2. Export failed rows to CSV
3. Fix data issues in spreadsheet
4. Re-upload corrected data
5. Verify successful processing

## Security Considerations

1. **Data Privacy**: Don't upload sensitive personal information to mock services
2. **API Keys**: Keep API credentials secure
3. **File Access**: Restrict access to uploaded files
4. **Network Security**: Use HTTPS for API communications

## Performance Tips

1. **File Size**: Keep individual files under 10MB
2. **Batch Size**: Process 100-500 rows per batch
3. **Network**: Ensure stable internet connection
4. **Resources**: Monitor system resources during processing
