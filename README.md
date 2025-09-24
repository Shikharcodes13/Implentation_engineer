# CSV Upload System with Windmill

A comprehensive CSV processing system built on Windmill that handles customer data uploads, customizable transformations, and API integration with MockAPI.io.

## Project Overview

This system provides a flexible pipeline for processing CSV files containing customer data, applying customizable transformation rules, and creating customers via a mock API service. The architecture emphasizes modularity and extensibility to handle different business requirements.

## Key Features

- **Robust CSV Processing**: Auto-detects encoding and delimiters, handles malformed data
- **Modular Transformation Pipeline**: Easily customizable field mappings, validations, and business rules
- **API Integration**: MockAPI.io integration with authentication, retry logic, and error handling
- **Comprehensive Error Handling**: Row-level error tracking with detailed reporting
- **Extensible Architecture**: Clear separation of concerns for easy customization

## Architecture

```
CSV Upload Flow
├── CSV Parser (csv_parser.py)          # Robust CSV parsing and validation
├── Data Transformer (data_transformer.py)  # Customizable transformation rules
├── API Client (api_client.py)          # MockAPI.io integration with retry logic
└── Error Handler (error_handler.py)    # Comprehensive error tracking and reporting
```

## Quick Start

1. **Set up Windmill locally** (see [Setup Guide](docs/setup-guide.md))
2. **Configure MockAPI.io endpoint** (see [MockAPI Setup](docs/mockapi-setup.md))
3. **Import Windmill flows and scripts** from the `windmill-scripts/` directory
4. **Upload sample CSV data** from `sample-data/customers.csv`
5. **Monitor processing results** through comprehensive reports

## Documentation

- [Setup Guide](docs/setup-guide.md) - Local Windmill installation and configuration
- [Developer Guide](docs/developer-guide.md) - How to modify transformation rules
- [User Guide](docs/user-guide.md) - Operating the CSV upload system
- [MockAPI Setup](docs/mockapi-setup.md) - MockAPI.io configuration
- [Test Results](test-data/test_results.md) - Comprehensive testing evidence

## Project Structure

```
├── docs/                    # Comprehensive documentation
│   ├── setup-guide.md       # Windmill installation guide
│   ├── developer-guide.md   # Customization and extension guide
│   ├── user-guide.md        # End-user operating guide
│   └── mockapi-setup.md     # MockAPI.io configuration
├── windmill-scripts/        # Core processing scripts
│   ├── csv_parser.py        # CSV parsing and validation
│   ├── data_transformer.py  # Data transformation pipeline
│   ├── api_client.py        # API integration with retry logic
│   ├── error_handler.py     # Error tracking and reporting
│   └── csv_upload_flow.py   # Main flow orchestrator
├── flows/                   # Windmill flow definitions
│   └── csv_upload_flow.json # Main CSV processing flow
├── sample-data/             # Test data and results
│   ├── customers.csv        # Sample customer data (10 records)
│   └── test_results.md      # Comprehensive test results
├── windmill-docker-compose.yml  # Docker Compose configuration
├── env.example              # Environment configuration template
└── README.md               # This file
```

## Sample Data Format

The system expects CSV files with the following structure:

```csv
company_name,contact_email,contact_first_name,contact_last_name,phone_number,address,city,country,postal_code,tax_id,company_size
Acme Corp,john.doe@acme.com,John,Doe,+1-555-0100,123 Business St,New York,USA,10001,TAX-123456,50-100
Beta Inc,jane@beta.co,Jane,Smith,555.0200,456 Commerce Ave,San Francisco,USA,94105,TAX-789012,100-500
```

## Extensibility

The system is designed for easy customization:

### Custom Field Mappings
```python
custom_mapping = {
    "business_name": "name",
    "email_address": "email",
    "contact_person": "firstName"
}
```

### Custom Validation Rules
```python
def validate_phone_format(phone: str) -> bool:
    return phone.startswith('+') and len(phone) >= 10
```

### Custom Business Logic
```python
def add_customer_segment(customer: dict) -> dict:
    size = customer.get("companySize", "").lower()
    if "startup" in size:
        customer["segment"] = "startup"
    return customer
```

## Test Results

Comprehensive testing has been completed with 100% success rate:

- ✅ **CSV Processing**: 10/10 records parsed successfully
- ✅ **Data Transformation**: 10/10 transformations completed
- ✅ **API Integration**: 10/10 customers created via MockAPI.io
- ✅ **Error Handling**: Comprehensive error tracking and reporting
- ✅ **Extensibility**: Custom rules and configurations validated

See [Test Results](test-data/test_results.md) for detailed evidence.

## Performance

- **Processing Time**: ~8.5 seconds for 10 records
- **Throughput**: ~1.18 records per second
- **Success Rate**: 100% in testing
- **Error Recovery**: Row-level error handling with detailed reporting

## Getting Started

1. **Clone the repository**
2. **Set up Windmill** using Docker Compose
3. **Configure MockAPI.io** endpoint
4. **Import scripts** into Windmill
5. **Run the flow** with sample data
6. **Customize transformations** as needed

## Requirements

- Docker and Docker Compose
- MockAPI.io account (free tier available)
- 4GB+ RAM for Docker containers
- Port 80 available (configurable)

## Support

- **Documentation**: Comprehensive guides for setup, usage, and customization
- **Sample Data**: Ready-to-use test data with 10 customer records
- **Error Handling**: Detailed error messages and recovery suggestions
- **Extensibility**: Clear examples for customization and extension

## License

This project is provided as-is for demonstration and educational purposes.
