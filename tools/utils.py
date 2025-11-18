from src.argos.service import AcfService
import os

def get_acf_service() -> AcfService:
    api_token = os.getenv("ARGOS_API_TOKEN")
    assert api_token is not None, "ARGOS_API_TOKEN environment variable is not set"
    acf_service = AcfService(
        config={
            "api_url": "https://argos.ebrand.com",
            "api_token": api_token,
        }
    )
    return acf_service