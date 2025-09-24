import csv
import io
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import chardet

@dataclass
class CSVParseResult:
    data: List[Dict[str, Any]]
    headers: List[str]
    errors: List[Dict[str, Any]]
    metadata: Dict[str, Any]

def parse_csv_content(
    csv_content: str,
    encoding: Optional[str] = None,
    delimiter: Optional[str] = None,
    skip_empty_rows: bool = True
) -> CSVParseResult:
    """
    Parse CSV content with robust error handling and encoding detection.
    
    Args:
        csv_content: Raw CSV content as string
        encoding: Character encoding (auto-detected if None)
        delimiter: CSV delimiter (auto-detected if None)
        skip_empty_rows: Whether to skip empty rows
    
    Returns:
        CSVParseResult with parsed data, headers, errors, and metadata
    """
    
    errors = []
    data = []
    headers = []
    metadata = {
        "total_rows": 0,
        "valid_rows": 0,
        "encoding": None,
        "delimiter": None
    }
    
    try:
        # Detect encoding if not provided
        if encoding is None:
            detected = chardet.detect(csv_content.encode('utf-8', errors='ignore'))
            encoding = detected.get('encoding', 'utf-8')
            metadata["encoding"] = encoding
        
        # Convert content to proper encoding
        try:
            csv_bytes = csv_content.encode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            csv_bytes = csv_content.encode('utf-8', errors='ignore')
            encoding = 'utf-8'
            metadata["encoding"] = encoding
        
        csv_string = csv_bytes.decode(encoding)
        
        # Detect delimiter if not provided
        if delimiter is None:
            sample = csv_string[:1024]
            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except csv.Error:
                delimiter = ','
            metadata["delimiter"] = delimiter
        
        # Parse CSV
        csv_io = io.StringIO(csv_string)
        reader = csv.DictReader(csv_io, delimiter=delimiter)
        
        headers = reader.fieldnames or []
        metadata["total_rows"] = len(csv_string.splitlines()) - 1
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            try:
                # Skip empty rows if requested
                if skip_empty_rows and not any(value.strip() for value in row.values()):
                    continue
                
                # Clean row data
                cleaned_row = {}
                for key, value in row.items():
                    if key:
                        cleaned_row[key.strip()] = value.strip() if value else ""
                
                # Validate row has required data
                if cleaned_row and any(cleaned_row.values()):
                    data.append(cleaned_row)
                    metadata["valid_rows"] += 1
                
            except Exception as e:
                errors.append({
                    "row_number": row_num,
                    "error": str(e),
                    "row_data": dict(row),
                    "error_type": "parsing"
                })
    
    except Exception as e:
        errors.append({
            "row_number": 0,
            "error": f"CSV parsing failed: {str(e)}",
            "row_data": None,
            "error_type": "critical"
        })
    
    return CSVParseResult(
        data=data,
        headers=headers,
        errors=errors,
        metadata=metadata
    )

def validate_csv_structure(
    data: List[Dict[str, Any]], 
    required_fields: List[str],
    optional_fields: List[str] = None
) -> Dict[str, Any]:
    """
    Validate CSV structure against expected fields.
    
    Args:
        data: Parsed CSV data
        required_fields: List of required field names
        optional_fields: List of optional field names
    
    Returns:
        Validation result with errors and warnings
    """
    
    if not data:
        return {
            "valid": False,
            "errors": ["No data found in CSV"],
            "warnings": [],
            "field_coverage": {}
        }
    
    errors = []
    warnings = []
    field_coverage = {}
    
    # Check if all required fields are present
    sample_row = data[0]
    available_fields = list(sample_row.keys())
    
    missing_required = [field for field in required_fields if field not in available_fields]
    if missing_required:
        errors.append(f"Missing required fields: {', '.join(missing_required)}")
    
    # Check for unexpected fields
    expected_fields = set(required_fields + (optional_fields or []))
    unexpected_fields = [field for field in available_fields if field not in expected_fields]
    if unexpected_fields:
        warnings.append(f"Unexpected fields found: {', '.join(unexpected_fields)}")
    
    # Calculate field coverage
    for field in available_fields:
        non_empty_count = sum(1 for row in data if row.get(field, '').strip())
        field_coverage[field] = {
            "total_rows": len(data),
            "non_empty_rows": non_empty_count,
            "coverage_percentage": (non_empty_count / len(data)) * 100
        }
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "field_coverage": field_coverage,
        "available_fields": available_fields,
        "missing_required": missing_required,
        "unexpected_fields": unexpected_fields
    }

def main(csv_content: str, encoding: str = None, delimiter: str = None) -> Dict[str, Any]:
    """
    Main function for CSV parsing with validation.
    
    Args:
        csv_content: Raw CSV content as string
        encoding: Character encoding (optional)
        delimiter: CSV delimiter (optional)
    
    Returns:
        Parsed and validated CSV data with metadata
    """
    
    # Define expected fields for customer data
    required_fields = ["company_name", "contact_email", "contact_first_name", "contact_last_name"]
    optional_fields = ["phone_number", "address", "city", "country", "postal_code", "tax_id", "company_size"]
    
    # Parse CSV
    parse_result = parse_csv_content(csv_content, encoding, delimiter)
    
    # Validate structure
    validation_result = validate_csv_structure(parse_result.data, required_fields, optional_fields)
    
    return {
        "success": len(parse_result.errors) == 0 and validation_result["valid"],
        "data": parse_result.data,
        "headers": parse_result.headers,
        "parse_errors": parse_result.errors,
        "validation": validation_result,
        "metadata": parse_result.metadata,
        "summary": {
            "total_rows": parse_result.metadata["total_rows"],
            "valid_rows": parse_result.metadata["valid_rows"],
            "parse_errors_count": len(parse_result.errors),
            "validation_errors_count": len(validation_result.get("errors", [])),
            "validation_warnings_count": len(validation_result.get("warnings", []))
        }
    }
