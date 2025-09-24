import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

@dataclass
class TransformationRule:
    """Configuration for a single transformation rule."""
    field_mapping: Dict[str, str]  # CSV field -> output field mapping
    validation_rules: Dict[str, Callable]  # field -> validation function
    transformation_functions: Dict[str, Callable]  # field -> transformation function
    business_rules: List[Callable]  # List of business logic functions

class CustomerTransformer:
    """
    Modular transformer for converting CSV data to customer objects.
    Easily extensible for different business requirements.
    """
    
    def __init__(self, rules: TransformationRule = None):
        self.rules = rules or self._get_default_rules()
    
    def _get_default_rules(self) -> TransformationRule:
        """Get default transformation rules for customer data."""
        
        def validate_email(email: str) -> bool:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email.strip())) if email else False
        
        def validate_phone(phone: str) -> bool:
            if not phone:
                return True
            # Allow various phone formats
            cleaned = re.sub(r'[^\d+]', '', phone)
            # Accept phones with 7+ digits (including country codes)
            return len(cleaned) >= 7
        
        def clean_phone(phone: str) -> str:
            if not phone:
                return ""
            cleaned = re.sub(r'[^\d+]', '', phone)
            if cleaned.startswith('+'):
                return cleaned
            elif len(cleaned) == 10:
                return f"+1-{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}"
            return phone
        
        def normalize_company_size(size: str) -> str:
            if not size:
                return "unknown"
            size_lower = size.lower()
            if any(x in size_lower for x in ['1-10', '1-9', 'startup']):
                return "1-10"
            elif any(x in size_lower for x in ['10-50', '11-50']):
                return "10-50"
            elif any(x in size_lower for x in ['50-100', '51-100']):
                return "50-100"
            elif any(x in size_lower for x in ['100-500', '101-500']):
                return "100-500"
            elif any(x in size_lower for x in ['500-1000', '501-1000']):
                return "500-1000"
            elif any(x in size_lower for x in ['1000+', 'enterprise', 'large']):
                return "1000+"
            return size
        
        def create_full_name(first_name: str, last_name: str) -> str:
            return f"{first_name.strip()} {last_name.strip()}".strip()
        
        def standardize_address(address: str) -> str:
            if not address:
                return ""
            return re.sub(r'\s+', ' ', address.strip())
        
        return TransformationRule(
            field_mapping={
                "company_name": "name",
                "contact_email": "email",
                "contact_first_name": "firstName",
                "contact_last_name": "lastName",
                "phone_number": "phone",
                "address": "address",
                "city": "city",
                "country": "country",
                "postal_code": "postalCode",
                "tax_id": "taxId",
                "company_size": "companySize"
            },
            validation_rules={
                "email": validate_email,
                "phone": validate_phone
            },
            transformation_functions={
                "phone": clean_phone,
                "companySize": normalize_company_size,
                "address": standardize_address
            },
            business_rules=[
                lambda row: self._add_contact_name(row),
                lambda row: self._add_timestamp(row),
                lambda row: self._add_metadata(row)
            ]
        )
    
    def _add_contact_name(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Add full contact name from first and last name."""
        if row.get("firstName") and row.get("lastName"):
            row["contactName"] = f"{row['firstName']} {row['lastName']}"
        return row
    
    def _add_timestamp(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Add creation timestamp."""
        from datetime import datetime
        row["createdAt"] = datetime.utcnow().isoformat() + "Z"
        return row
    
    def _add_metadata(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Add processing metadata."""
        row["metadata"] = {
            "source": "csv_upload",
            "processed_at": row.get("createdAt"),
            "original_fields": list(row.keys())
        }
        return row
    
    def transform_row(self, csv_row: Dict[str, Any], row_index: int) -> Dict[str, Any]:
        """
        Transform a single CSV row to customer object.
        
        Args:
            csv_row: Raw CSV row data
            row_index: Row index for error tracking
        
        Returns:
            Transformed customer object
        """
        try:
            # Initialize result object
            customer = {}
            
            # Apply field mapping
            for csv_field, output_field in self.rules.field_mapping.items():
                if csv_field in csv_row:
                    customer[output_field] = csv_row[csv_field]
            
            # Apply transformations
            for field, transform_func in self.rules.transformation_functions.items():
                if field in customer:
                    customer[field] = transform_func(customer[field])
            
            # Apply business rules
            for rule_func in self.rules.business_rules:
                customer = rule_func(customer)
            
            return customer
            
        except Exception as e:
            raise ValueError(f"Transformation failed for row {row_index}: {str(e)}")
    
    def validate_row(self, customer: Dict[str, Any], row_index: int) -> List[str]:
        """
        Validate a transformed customer object.
        
        Args:
            customer: Transformed customer object
            row_index: Row index for error tracking
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        required_fields = ["name", "email", "firstName", "lastName"]
        for field in required_fields:
            if not customer.get(field, "").strip():
                errors.append(f"Missing required field: {field}")
        
        # Apply validation rules
        for field, validation_func in self.rules.validation_rules.items():
            if field in customer:
                if not validation_func(customer[field]):
                    errors.append(f"Invalid {field}: {customer[field]}")
        
        return errors
    
    def transform_batch(self, csv_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transform a batch of CSV rows.
        
        Args:
            csv_data: List of CSV row dictionaries
        
        Returns:
            Transformation results with success/failure details
        """
        results = {
            "successful_transformations": [],
            "failed_transformations": [],
            "validation_errors": [],
            "summary": {
                "total_rows": len(csv_data),
                "successful_count": 0,
                "failed_count": 0,
                "validation_error_count": 0
            }
        }
        
        for i, csv_row in enumerate(csv_data):
            try:
                # Transform row
                customer = self.transform_row(csv_row, i + 1)
                
                # Validate row
                validation_errors = self.validate_row(customer, i + 1)
                
                if validation_errors:
                    results["validation_errors"].append({
                        "row_index": i + 1,
                        "errors": validation_errors,
                        "data": customer
                    })
                    results["summary"]["validation_error_count"] += 1
                else:
                    results["successful_transformations"].append(customer)
                    results["summary"]["successful_count"] += 1
                
            except Exception as e:
                results["failed_transformations"].append({
                    "row_index": i + 1,
                    "error": str(e),
                    "data": csv_row
                })
                results["summary"]["failed_count"] += 1
        
        return results

def create_custom_transformer(
    field_mapping: Dict[str, str],
    custom_validations: Dict[str, Callable] = None,
    custom_transformations: Dict[str, Callable] = None,
    custom_business_rules: List[Callable] = None
) -> CustomerTransformer:
    """
    Factory function to create a custom transformer with specific rules.
    
    Args:
        field_mapping: Custom field mapping
        custom_validations: Custom validation functions
        custom_transformations: Custom transformation functions
        custom_business_rules: Custom business logic functions
    
    Returns:
        Configured CustomerTransformer instance
    """
    
    default_rules = CustomerTransformer()._get_default_rules()
    
    # Merge with custom rules
    final_field_mapping = {**default_rules.field_mapping, **field_mapping}
    final_validations = {**default_rules.validation_rules, **(custom_validations or {})}
    final_transformations = {**default_rules.transformation_functions, **(custom_transformations or {})}
    final_business_rules = default_rules.business_rules + (custom_business_rules or [])
    
    custom_rules = TransformationRule(
        field_mapping=final_field_mapping,
        validation_rules=final_validations,
        transformation_functions=final_transformations,
        business_rules=final_business_rules
    )
    
    return CustomerTransformer(custom_rules)

def main(csv_data: List[Dict[str, Any]], transformation_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main function for data transformation.
    
    Args:
        csv_data: Parsed CSV data
        transformation_config: Optional configuration for custom transformations
    
    Returns:
        Transformation results
    """
    
    # Create transformer with optional custom configuration
    if transformation_config:
        transformer = create_custom_transformer(
            field_mapping=transformation_config.get("field_mapping", {}),
            custom_validations=transformation_config.get("custom_validations"),
            custom_transformations=transformation_config.get("custom_transformations"),
            custom_business_rules=transformation_config.get("custom_business_rules")
        )
    else:
        transformer = CustomerTransformer()
    
    # Transform the data
    results = transformer.transform_batch(csv_data)
    
    return results
