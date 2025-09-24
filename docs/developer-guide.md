# Developer Guide - CSV Upload System

This guide explains how to modify and extend the CSV upload system for different business requirements.

## Architecture Overview

The system is built with a modular architecture that separates concerns:

```
CSV Upload Flow
├── CSV Parser (csv_parser.py)
├── Data Transformer (data_transformer.py)
├── API Client (api_client.py)
└── Error Handler (error_handler.py)
```

## Core Components

### 1. CSV Parser (`csv_parser.py`)

Handles CSV file parsing with robust error handling and encoding detection.

**Key Functions:**
- `parse_csv_content()`: Main parsing function
- `validate_csv_structure()`: Structure validation
- `main()`: Entry point for CSV processing

**Extensibility Points:**
- Custom encoding detection
- Custom delimiter detection
- Field validation rules

### 2. Data Transformer (`data_transformer.py`)

Converts CSV data to customer objects with customizable transformation rules.

**Key Classes:**
- `CustomerTransformer`: Main transformer class
- `TransformationRule`: Configuration for transformations
- `create_custom_transformer()`: Factory function for custom transformers

**Extensibility Points:**
- Custom field mappings
- Custom validation rules
- Custom transformation functions
- Custom business logic

### 3. API Client (`api_client.py`)

Handles API integration with MockAPI.io, including authentication and retry logic.

**Key Classes:**
- `MockAPIClient`: Main API client
- `RetryConfig`: Retry configuration
- `APIResponse`: Standardized response format

**Extensibility Points:**
- Custom retry strategies
- Custom authentication methods
- Custom error handling

### 4. Error Handler (`error_handler.py`)

Comprehensive error tracking and reporting system.

**Key Classes:**
- `ErrorHandler`: Main error handling class
- `ErrorRecord`: Individual error records
- `ProcessingReport`: Comprehensive reports

**Extensibility Points:**
- Custom error categories
- Custom reporting formats
- Custom severity levels

## Customization Examples

### Example 1: Custom Field Mapping

```python
# Create custom field mapping
custom_mapping = {
    "business_name": "name",           # Map business_name to name
    "email_address": "email",          # Map email_address to email
    "contact_person": "firstName",     # Map contact_person to firstName
    "company_id": "externalId"         # Add new field
}

# Create custom transformer
transformer = create_custom_transformer(field_mapping=custom_mapping)
```

### Example 2: Custom Validation Rules

```python
def validate_company_size(size: str) -> bool:
    """Custom validation for company size."""
    valid_sizes = ["startup", "small", "medium", "large", "enterprise"]
    return size.lower() in valid_sizes

def validate_phone_format(phone: str) -> bool:
    """Custom phone validation for specific format."""
    import re
    pattern = r'^\+\d{1,3}-\d{3}-\d{3}-\d{4}$'
    return bool(re.match(pattern, phone))

# Create transformer with custom validations
custom_validations = {
    "companySize": validate_company_size,
    "phone": validate_phone_format
}

transformer = create_custom_transformer(custom_validations=custom_validations)
```

### Example 3: Custom Transformation Functions

```python
def normalize_company_name(name: str) -> str:
    """Normalize company names."""
    # Remove common suffixes
    suffixes = [" Inc", " LLC", " Corp", " Ltd"]
    normalized = name
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)]
    
    # Title case
    return normalized.title()

def extract_domain_from_email(email: str) -> str:
    """Extract domain from email address."""
    if "@" in email:
        return email.split("@")[1]
    return ""

# Create transformer with custom transformations
custom_transformations = {
    "name": normalize_company_name,
    "emailDomain": extract_domain_from_email
}

transformer = create_custom_transformer(custom_transformations=custom_transformations)
```

### Example 4: Custom Business Rules

```python
def add_customer_segment(customer: dict) -> dict:
    """Add customer segment based on company size."""
    size = customer.get("companySize", "").lower()
    
    if size in ["startup", "1-10"]:
        customer["segment"] = "startup"
    elif size in ["10-50", "50-100"]:
        customer["segment"] = "small_business"
    elif size in ["100-500", "500-1000"]:
        customer["segment"] = "medium_business"
    else:
        customer["segment"] = "enterprise"
    
    return customer

def add_geographic_region(customer: dict) -> dict:
    """Add geographic region based on country."""
    country = customer.get("country", "").upper()
    
    if country in ["USA", "CANADA"]:
        customer["region"] = "North America"
    elif country in ["UK", "GERMANY", "FRANCE"]:
        customer["region"] = "Europe"
    else:
        customer["region"] = "Other"
    
    return customer

# Create transformer with custom business rules
custom_business_rules = [
    add_customer_segment,
    add_geographic_region
]

transformer = create_custom_transformer(custom_business_rules=custom_business_rules)
```

### Example 5: Custom API Configuration

```python
# Custom retry configuration
retry_config = RetryConfig(
    max_retries=5,
    base_delay=2.0,
    max_delay=120.0,
    backoff_factor=1.5,
    retry_on_status_codes=[429, 500, 502, 503, 504]
)

# Create API client with custom configuration
api_client = MockAPIClient(
    base_url="https://your-api.com/api/v1",
    api_key="your-api-key",
    timeout=60,
    retry_config=retry_config
)
```

## Adding New Transformation Rules

### Step 1: Define the Rule

Create a new transformation rule in your configuration:

```python
def my_custom_rule(customer: dict) -> dict:
    """Your custom transformation logic."""
    # Add your logic here
    customer["customField"] = "custom_value"
    return customer
```

### Step 2: Apply the Rule

Add it to your transformation configuration:

```python
transformation_config = {
    "custom_business_rules": [my_custom_rule]
}
```

### Step 3: Use in Flow

Pass the configuration to the main flow:

```python
result = main(
    csv_content=csv_data,
    api_base_url=api_url,
    transformation_config=transformation_config
)
```

## Error Handling Extensions

### Custom Error Categories

```python
from error_handler import ErrorCategory

# Add custom error category
class CustomErrorCategory(ErrorCategory):
    BUSINESS_LOGIC = "business_logic"
    DATA_CLEANING = "data_cleaning"
```

### Custom Error Handling

```python
def handle_business_logic_error(self, error_message: str, row_index: int, customer_data: dict):
    """Handle custom business logic errors."""
    self.add_error(
        message=f"Business logic error in row {row_index}",
        category=CustomErrorCategory.BUSINESS_LOGIC,
        severity=ErrorSeverity.MEDIUM,
        details={"error": error_message},
        row_index=row_index,
        customer_data=customer_data,
        error_code="BUSINESS_LOGIC_ERROR"
    )
```

## Testing Your Changes

### Unit Testing

```python
def test_custom_transformation():
    """Test custom transformation logic."""
    # Your test data
    test_data = [{"company_name": "Test Corp", "email": "test@example.com"}]
    
    # Your custom configuration
    config = {
        "custom_business_rules": [my_custom_rule]
    }
    
    # Test transformation
    result = transform_data(test_data, config)
    
    # Assertions
    assert result["summary"]["successful_count"] == 1
    assert "customField" in result["successful_transformations"][0]
```

### Integration Testing

```python
def test_end_to_end_flow():
    """Test complete flow with custom configuration."""
    # Your test CSV
    csv_content = "company_name,email\nTest Corp,test@example.com"
    
    # Your configuration
    config = {
        "field_mapping": {"company_name": "name"},
        "custom_business_rules": [my_custom_rule]
    }
    
    # Test complete flow
    result = main(
        csv_content=csv_content,
        api_base_url="https://test-api.com",
        transformation_config=config
    )
    
    # Assertions
    assert result["success"] == True
    assert result["quick_summary"]["success_rate"] == 100
```

## Best Practices

### 1. Modularity
- Keep transformation rules focused on single responsibilities
- Use composition over inheritance
- Make functions pure when possible

### 2. Error Handling
- Always validate inputs
- Provide meaningful error messages
- Log errors with sufficient context

### 3. Testing
- Write unit tests for custom transformations
- Test edge cases and error conditions
- Use integration tests for end-to-end validation

### 4. Documentation
- Document custom transformation rules
- Provide examples for complex logic
- Keep configuration examples up to date

### 5. Performance
- Avoid expensive operations in transformation loops
- Use efficient data structures
- Consider caching for repeated operations

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all modules are in the same directory or properly configured in the Python path.

2. **Field Mapping Issues**: Verify that CSV field names match exactly (case-sensitive).

3. **Validation Failures**: Check that validation functions return boolean values.

4. **API Errors**: Verify API URL format and authentication credentials.

5. **Memory Issues**: For large CSV files, consider processing in batches.

### Debug Mode

Enable debug mode by setting environment variables:

```python
import os
os.environ["DEBUG"] = "true"
```

This will provide additional logging and error details.

## Contributing

When adding new features:

1. Follow the existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Consider backward compatibility
5. Add error handling for edge cases

## Resources

- [Windmill Documentation](https://docs.windmill.dev/)
- [MockAPI.io Documentation](https://mockapi.io/docs)
- [Python CSV Module](https://docs.python.org/3/library/csv.html)
- [Requests Library](https://docs.python-requests.org/)
