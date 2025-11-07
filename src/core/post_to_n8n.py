"""
Module for posting incident data to n8n webhook.
Handles communication with n8n automation workflows.
"""

import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime


class N8NWebhookClient:
    """
    Client for posting incident data to n8n webhooks.
    Manages the communication with n8n automation platform.
    """
    
    def __init__(self, webhook_url: str, timeout: int = 30):
        """
        Initialize the n8n webhook client.
        
        Args:
            webhook_url: The n8n webhook URL (e.g., https://your-n8n.com/webhook/incident)
            timeout: Request timeout in seconds (default: 30)
        """
        self.webhook_url = webhook_url
        self.timeout = timeout
    
    def post_incident(
        self,
        policy_id: str,
        customer_name: str,
        incident_date: str,
        incident_type: str,
        description: str,
        location: str,
        estimated_damage: float
    ) -> Dict[str, Any]:
        """
        Post an incident report to the n8n webhook.
        
        Args:
            policy_id: Policy identifier (e.g., "POL-001")
            customer_name: Full name of the customer
            incident_date: Date of incident in YYYY-MM-DD format
            incident_type: Type of incident (e.g., "Auto Accident", "Property Damage")
            description: Detailed description from voice conversation
            location: Location where incident occurred
            estimated_damage: Estimated damage amount in currency units
            
        Returns:
            Dictionary containing the response from n8n webhook
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Construct the payload matching the n8n expected format
        payload = {
            "policyId": policy_id,
            "customerName": customer_name,
            "incidentDate": incident_date,
            "incidentType": incident_type,
            "description": description,
            "location": location,
            "estimatedDamage": estimated_damage
        }
        
        print(f"[N8NWebhookClient] Posting incident to n8n webhook...")
        print(f"[N8NWebhookClient] Policy: {policy_id}, Customer: {customer_name}")
        
        try:
            # Make POST request to n8n webhook
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            print(f"[N8NWebhookClient] ✅ Successfully posted to n8n (Status: {response.status_code})")
            
            # Try to parse JSON response, fallback to text if not JSON
            try:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response": response.json()
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response": response.text
                }
                
        except requests.exceptions.Timeout:
            error_msg = f"Request timed out after {self.timeout} seconds"
            print(f"[N8NWebhookClient] ❌ Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"[N8NWebhookClient] ❌ Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
    
    def post_incident_from_dict(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post an incident using a dictionary of data.
        Convenience method for when you already have the data structured.
        
        Args:
            incident_data: Dictionary containing all incident fields
            
        Returns:
            Dictionary containing the response from n8n webhook
        """
        return self.post_incident(
            policy_id=incident_data["policyId"],
            customer_name=incident_data["customerName"],
            incident_date=incident_data["incidentDate"],
            incident_type=incident_data["incidentType"],
            description=incident_data["description"],
            location=incident_data["location"],
            estimated_damage=incident_data["estimatedDamage"]
        )
    
    def validate_incident_data(self, incident_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate incident data before posting.
        Checks for required fields and data types.
        
        Args:
            incident_data: Dictionary containing incident fields to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = [
            "policyId", "customerName", "incidentDate", 
            "incidentType", "description", "location", "estimatedDamage"
        ]
        
        # Check for missing fields
        for field in required_fields:
            if field not in incident_data:
                return False, f"Missing required field: {field}"
        
        # Validate date format (basic check)
        try:
            datetime.strptime(incident_data["incidentDate"], "%Y-%m-%d")
        except ValueError:
            return False, "incidentDate must be in YYYY-MM-DD format"
        
        # Validate estimated damage is numeric
        if not isinstance(incident_data["estimatedDamage"], (int, float)):
            return False, "estimatedDamage must be a number"
        
        return True, None


def create_incident_payload(
    policy_id: str,
    customer_name: str,
    incident_type: str,
    description: str,
    location: str,
    estimated_damage: float,
    incident_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Helper function to create a properly formatted incident payload.
    
    Args:
        policy_id: Policy identifier
        customer_name: Customer's full name
        incident_type: Type of incident
        description: Detailed description
        location: Location of incident
        estimated_damage: Estimated damage amount
        incident_date: Date of incident (defaults to today if not provided)
        
    Returns:
        Dictionary with properly formatted incident data
    """
    if incident_date is None:
        incident_date = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "policyId": policy_id,
        "customerName": customer_name,
        "incidentDate": incident_date,
        "incidentType": incident_type,
        "description": description,
        "location": location,
        "estimatedDamage": estimated_damage
    }
