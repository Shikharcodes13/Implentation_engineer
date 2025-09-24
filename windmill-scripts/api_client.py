import requests
import time
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class APIErrorType(Enum):
    NETWORK_ERROR = "network_error"
    AUTHENTICATION_ERROR = "authentication_error"
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_type: Optional[APIErrorType] = None
    status_code: Optional[int] = None
    retry_count: int = 0

@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0
    retry_on_status_codes: List[int] = None
    
    def __post_init__(self):
        if self.retry_on_status_codes is None:
            self.retry_on_status_codes = [429, 500, 502, 503, 504]

class MockAPIClient:
    """
    Client for interacting with MockAPI.io customer endpoint.
    Includes authentication, retry logic, and comprehensive error handling.
    """
    
    def __init__(
        self, 
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        retry_config: RetryConfig = None
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig()
        self.session = requests.Session()
        
        # Set up default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    def _classify_error(self, response: requests.Response, exception: Exception = None) -> Tuple[APIErrorType, str]:
        """Classify API errors for appropriate handling."""
        
        if exception:
            if isinstance(exception, requests.exceptions.ConnectionError):
                return APIErrorType.NETWORK_ERROR, "Network connection error"
            elif isinstance(exception, requests.exceptions.Timeout):
                return APIErrorType.NETWORK_ERROR, "Request timeout"
            else:
                return APIErrorType.NETWORK_ERROR, f"Network error: {str(exception)}"
        
        status_code = response.status_code
        
        if status_code == 401:
            return APIErrorType.AUTHENTICATION_ERROR, "Authentication failed"
        elif status_code == 403:
            return APIErrorType.AUTHENTICATION_ERROR, "Access forbidden"
        elif status_code == 422:
            return APIErrorType.VALIDATION_ERROR, "Validation error"
        elif status_code == 429:
            return APIErrorType.RATE_LIMIT_ERROR, "Rate limit exceeded"
        elif 500 <= status_code < 600:
            return APIErrorType.SERVER_ERROR, f"Server error: {status_code}"
        else:
            return APIErrorType.UNKNOWN_ERROR, f"Unknown error: {status_code}"
    
    def _should_retry(self, error_type: APIErrorType, status_code: int) -> bool:
        """Determine if a request should be retried based on error type and status code."""
        
        retryable_errors = {
            APIErrorType.NETWORK_ERROR,
            APIErrorType.SERVER_ERROR,
            APIErrorType.RATE_LIMIT_ERROR
        }
        
        return (
            error_type in retryable_errors or 
            status_code in self.retry_config.retry_on_status_codes
        )
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        delay = self.retry_config.base_delay * (self.retry_config.backoff_factor ** attempt)
        return min(delay, self.retry_config.max_delay)
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None
    ) -> APIResponse:
        """Make HTTP request with retry logic."""
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        last_exception = None
        
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                # Make request
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    timeout=self.timeout
                )
                
                # Check for success
                if response.status_code in [200, 201]:
                    return APIResponse(
                        success=True,
                        data=response.json() if response.content else None,
                        status_code=response.status_code,
                        retry_count=attempt
                    )
                
                # Handle error response
                error_type, error_message = self._classify_error(response)
                
                # Check if we should retry
                if attempt < self.retry_config.max_retries and self._should_retry(error_type, response.status_code):
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                    continue
                
                # Don't retry or max retries reached
                return APIResponse(
                    success=False,
                    error=error_message,
                    error_type=error_type,
                    status_code=response.status_code,
                    retry_count=attempt
                )
                
            except Exception as e:
                last_exception = e
                error_type, error_message = self._classify_error(None, e)
                
                # Check if we should retry
                if attempt < self.retry_config.max_retries and self._should_retry(error_type, 0):
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                    continue
                
                # Don't retry or max retries reached
                return APIResponse(
                    success=False,
                    error=error_message,
                    error_type=error_type,
                    retry_count=attempt
                )
        
        # This should never be reached, but just in case
        return APIResponse(
            success=False,
            error="Maximum retries exceeded",
            error_type=APIErrorType.UNKNOWN_ERROR,
            retry_count=self.retry_config.max_retries
        )
    
    def create_customer(self, customer_data: Dict[str, Any]) -> APIResponse:
        """
        Create a single customer via API.
        
        Args:
            customer_data: Customer object to create
        
        Returns:
            APIResponse with result
        """
        return self._make_request('POST', '/customers', data=customer_data)
    
    def create_customers_batch(self, customers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple customers with individual error handling.
        
        Args:
            customers: List of customer objects
        
        Returns:
            Batch processing results
        """
        results = {
            "successful_creations": [],
            "failed_creations": [],
            "summary": {
                "total_customers": len(customers),
                "successful_count": 0,
                "failed_count": 0,
                "api_errors": {}
            }
        }
        
        for i, customer in enumerate(customers):
            response = self.create_customer(customer)
            
            if response.success:
                results["successful_creations"].append({
                    "customer_index": i,
                    "customer_data": customer,
                    "api_response": response.data,
                    "retry_count": response.retry_count
                })
                results["summary"]["successful_count"] += 1
            else:
                # Track error types for reporting
                error_type = response.error_type.value if response.error_type else "unknown"
                if error_type not in results["summary"]["api_errors"]:
                    results["summary"]["api_errors"][error_type] = 0
                results["summary"]["api_errors"][error_type] += 1
                
                results["failed_creations"].append({
                    "customer_index": i,
                    "customer_data": customer,
                    "error": response.error,
                    "error_type": error_type,
                    "status_code": response.status_code,
                    "retry_count": response.retry_count
                })
                results["summary"]["failed_count"] += 1
        
        return results
    
    def get_customer(self, customer_id: str) -> APIResponse:
        """Get a customer by ID."""
        return self._make_request('GET', f'/customers/{customer_id}')
    
    def list_customers(self, limit: int = 100, page: int = 1) -> APIResponse:
        """List customers with pagination."""
        params = {'limit': limit, 'page': page}
        return self._make_request('GET', '/customers', params=params)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> APIResponse:
        """Update a customer."""
        return self._make_request('PUT', f'/customers/{customer_id}', data=customer_data)
    
    def delete_customer(self, customer_id: str) -> APIResponse:
        """Delete a customer."""
        return self._make_request('DELETE', f'/customers/{customer_id}')

def create_api_client(
    base_url: str,
    api_key: Optional[str] = None,
    timeout: int = 30,
    max_retries: int = 3,
    base_delay: float = 1.0
) -> MockAPIClient:
    """
    Factory function to create an API client with custom configuration.
    
    Args:
        base_url: Base URL for the API
        api_key: Optional API key for authentication
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        base_delay: Base delay for exponential backoff
    
    Returns:
        Configured MockAPIClient instance
    """
    
    retry_config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay
    )
    
    return MockAPIClient(
        base_url=base_url,
        api_key=api_key,
        timeout=timeout,
        retry_config=retry_config
    )

def main(
    customers: List[Dict[str, Any]],
    api_base_url: str,
    api_key: Optional[str] = None,
    batch_size: int = 10,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Main function for API integration.
    
    Args:
        customers: List of customer objects to create
        api_base_url: Base URL for MockAPI.io endpoint
        api_key: Optional API key
        batch_size: Number of customers to process in parallel (future enhancement)
        max_retries: Maximum retry attempts per request
    
    Returns:
        API processing results
    """
    
    # Create API client
    client = create_api_client(
        base_url=api_base_url,
        api_key=api_key,
        max_retries=max_retries
    )
    
    # Process customers
    results = client.create_customers_batch(customers)
    
    return results
