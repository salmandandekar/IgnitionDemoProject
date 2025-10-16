"""
ISO/SEI-aligned configuration for context management.
- Centralized so auditors can see allowed tenants, strategy order, and policy flags.
- No code changes required for operational updates.
"""

CONFIG = {
    # Allowed tenants (whitelist) — ISO 27001 input validation
    "ALLOWED_TENANTS": ["PlantA", "PlantB", "HQ"],

    # Strategy chain (resolution order)
    "STRATEGY_ORDER": [
        "from_incoming",
        "from_session_props",
        "from_jwt_claims",
        "from_user_directory",
        "from_host_mapping",
    ],

    # Default tenant behavior
    "ALLOW_DEFAULT": False,
    "DEFAULT_TENANT": None,

    # Hostname → tenant mapping for edge gateways
    "HOST_TO_TENANT": {
        "gw-plant-a": "PlantA",
        "gw-plant-b": "PlantB",
    },

    # Logging level for context operations
    "LOG_LEVEL": "DEBUG",
}