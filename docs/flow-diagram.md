# CSV Upload System Flow

## Complete Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CSV UPLOAD SYSTEM FLOW                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   INPUT DATA    │    │   WINDMILL      │    │   MOCKAPI.IO    │
│                 │    │   PLATFORM      │    │   ENDPOINT      │
│ • CSV Content   │───▶│ • Flow Runner   │───▶│ • Customer API  │
│ • API Config    │    │ • Scripts       │    │ • Auth/Retry    │
│ • Transform     │    │ • Error Handle  │    │ • Response      │
│   Config        │    │ • Reporting     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Detailed Processing Stages

### Stage 1: CSV Parsing & Validation
```
CSV Content → CSV Parser → Validation → Parsed Data
     │             │           │            │
     ▼             ▼           ▼            ▼
┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐
│Raw CSV  │  │Encoding  │  │Required │  │Clean     │
│String   │  │Detection │  │Fields   │  │Row Data  │
└─────────┘  └──────────┘  └─────────┘  └──────────┘
```

### Stage 2: Data Transformation
```
Parsed Data → Transformer → Business Rules → Customer Objects
     │            │              │               │
     ▼            ▼              ▼               ▼
┌──────────┐  ┌─────────┐  ┌──────────────┐  ┌─────────────┐
│Row Data  │  │Field    │  │Custom Logic  │  │Structured   │
│          │  │Mapping  │  │Validation    │  │Customers    │
└──────────┘  └─────────┘  └──────────────┘  └─────────────┘
```

### Stage 3: API Integration
```
Customer Objects → API Client → MockAPI.io → Created Customers
       │              │            │              │
       ▼              ▼            ▼              ▼
┌─────────────┐  ┌──────────┐  ┌─────────┐  ┌──────────────┐
│Transformed  │  │Retry     │  │HTTP     │  │API Response  │
│Data         │  │Logic     │  │Requests │  │& Results     │
└─────────────┘  └──────────┘  └─────────┘  └──────────────┘
```

### Stage 4: Error Handling & Reporting
```
All Stages → Error Handler → Comprehensive Report → Final Results
     │             │               │                    │
     ▼             ▼               ▼                    ▼
┌─────────┐  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐
│Errors   │  │Error     │  │Processing    │  │Success/Failure  │
│Warnings │  │Tracking  │  │Statistics    │  │Summary          │
└─────────┘  └──────────┘  └──────────────┘  └─────────────────┘
```

## Component Interactions

### Main Flow Orchestrator
- **File**: `csv_upload_flow.py`
- **Function**: `main()`
- **Role**: Coordinates all processing stages
- **Input**: CSV content, API URL, configuration
- **Output**: Complete processing results

### CSV Parser
- **File**: `csv_parser.py`
- **Functions**: `parse_csv_content()`, `validate_csv_structure()`
- **Role**: Parse and validate CSV data
- **Features**: Auto-encoding detection, delimiter detection, error handling

### Data Transformer
- **File**: `data_transformer.py`
- **Classes**: `CustomerTransformer`, `TransformationRule`
- **Role**: Transform CSV data to customer objects
- **Features**: Custom field mapping, validation, business rules

### API Client
- **File**: `api_client.py`
- **Classes**: `MockAPIClient`, `RetryConfig`
- **Role**: Handle API integration
- **Features**: Authentication, retry logic, error handling

### Error Handler
- **File**: `error_handler.py`
- **Classes**: `ErrorHandler`, `ProcessingReport`
- **Role**: Track errors and generate reports
- **Features**: Comprehensive error tracking, detailed reporting

## Data Flow

### Input → Processing → Output

```
CSV File/Content
       ↓
┌─────────────────────────────────────┐
│           WINDMILL FLOW             │
│                                     │
│  ┌─────────┐  ┌─────────┐  ┌──────┐ │
│  │CSV      │  │Data     │  │API   │ │
│  │Parser   │→ │Transform│→ │Client│ │
│  └─────────┘  └─────────┘  └──────┘ │
│       ↓           ↓           ↓     │
│  ┌─────────────────────────────────┐ │
│  │        Error Handler            │ │
│  │  (tracks errors from all stages)│ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│         FINAL RESULTS               │
│                                     │
│ • Processing Report                 │
│ • Success/Failure Statistics       │
│ • Error Details                    │
│ • Created Customer Data            │
└─────────────────────────────────────┘
```

## Error Handling Flow

```
Error Occurs → Error Classification → Error Tracking → Continue Processing
     │                │                    │                  │
     ▼                ▼                    ▼                  ▼
┌─────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│Any      │    │Severity      │    │Error        │    │Process       │
│Stage    │    │Level         │    │Record       │    │Valid Rows    │
└─────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

## Customization Points

### 1. Field Mapping
```python
custom_mapping = {
    "business_name": "name",
    "email_address": "email"
}
```

### 2. Validation Rules
```python
def validate_phone(phone: str) -> bool:
    return phone.startswith('+')
```

### 3. Business Logic
```python
def add_segment(customer: dict) -> dict:
    customer["segment"] = "enterprise"
    return customer
```

### 4. API Configuration
```python
retry_config = RetryConfig(
    max_retries=5,
    base_delay=2.0
)
```
