"""
Centralized configuration for Expat Rental Assistant
"""
import os
from pathlib import Path

# Read version from version.txt (try root first, then backend, fallback to hardcoded)
VERSION = "1.0.0"  # Default fallback
for version_path in [Path(__file__).parent.parent / "version.txt", Path(__file__).parent / "version.txt"]:
    if version_path.exists():
        with open(version_path, "r") as f:
            VERSION = f.read().strip()
        break

# Application metadata
APP_NAME = "Expat Rental Assistant API"
APP_DESCRIPTION = "AI-powered chatbot for helping expats navigate the Dutch rental market"

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")  # Smaller, faster model
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "150"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Price data (2024 averages in euros)
RENTAL_PRICES = {
    "Amsterdam": {"1-bed": (1500, 1900), "2-bed": (2000, 2600)},
    "Utrecht": {"1-bed": (1200, 1500), "2-bed": (1600, 2000)},
    "Rotterdam": {"1-bed": (1000, 1300), "2-bed": (1400, 1800)},
    "The Hague": {"1-bed": (1100, 1400), "2-bed": (1500, 1900)},
}
UTILITIES_RANGE = (120, 180)  # Monthly utilities in euros

# Cities list
MAJOR_CITIES = ["Amsterdam", "Utrecht", "Rotterdam", "The Hague"]

# Document checklist
REQUIRED_DOCUMENTS = [
    "Valid passport or ID",
    "BSN (Burgerservicenummer) from municipality registration",
    "Proof of income with 3 recent payslips or employment contract",
    "Dutch bank account from ING ABN AMRO or Rabobank",
    "Residence permit if non-EU",
    "Proof of rental insurance sometimes required",
    "References from previous landlord optional but helpful"
]

# Scam warning keywords
SCAM_WARNINGS = [
    "Never pay deposit before viewing property in person",
    "Avoid landlords who claim to be abroad and cannot show property",
    "Be suspicious of prices far below market rate",
    "Never wire money via Western Union or untraceable methods",
    "Verify landlord identity and property ownership",
    "Use official platforms like Funda Pararius Kamernet",
    "Watch for urgent pressure to pay immediately"
]

# Contract analysis configuration
CONTRACT_ANALYSIS_MAX_CHARS = 2000
CONTRACT_ANALYSIS_PROMPT_TEMPLATE = """Analyze this Dutch rental contract and provide key information:

Contract excerpt:
{contract_text}

Please identify and summarize:
1. Rental price and what it includes (utilities, service costs, etc.)
2. Contract duration and notice period
3. Deposit amount
4. Any unusual clauses or red flags
5. Your overall assessment (fair/unfair/needs attention)

Keep your response concise and focused on expat concerns."""

# System prompt template
SYSTEM_PROMPT_TEMPLATE = """You are an Expat Rental Assistant specialized in helping international professionals and families find rental properties in the Netherlands.

Core Topics:
- Expat-friendly neighborhoods and cities in {cities}
- Dutch rental contracts and legal requirements such as huurcontract and huurcommissie
- Visa and residency considerations for renting including BSN and residence permit
- International tenant rights in the Netherlands
- Cultural differences in Dutch rental markets
- Furnished vs unfurnished rentals common in expat areas
- Utilities like gas water electricity, deposits, and service costs
- Expat community resources and international schools
- Transportation including OV-chipkaart and cycling culture

Special Features:

Price Fairness Checker - When users ask about rental prices provide context based on 2024 averages:
{price_data}
Utilities typically add {utilities_min}-{utilities_max} euro per month
Note if price seems fair high or low and mention factors that affect pricing.

Document Checklist - Provide complete list:
{documents}

Scam Detection - Warn about common scams:
{scam_warnings}

Important Guidelines:
Keep responses SHORT and CONCISE with 2-5 sentences maximum
Break information into clear separate sentences
Use simple language and natural conversational tone
Be direct and practical
Focus on Netherlands rental market for expats
Politely redirect if asked about buying property or topics outside expat rentals"""


def get_system_prompt():
    """Generate system prompt with current configuration"""
    # Format price data
    price_lines = []
    for city, prices in RENTAL_PRICES.items():
        bed1 = prices["1-bed"]
        bed2 = prices["2-bed"]
        price_lines.append(f"{city} 1-bed {bed1[0]}-{bed1[1]} euro, 2-bed {bed2[0]}-{bed2[1]} euro")
    price_data = "\n".join(price_lines)

    # Format documents
    documents = "\n".join(REQUIRED_DOCUMENTS)

    # Format scam warnings
    scam_warnings = "\n".join(SCAM_WARNINGS)

    return SYSTEM_PROMPT_TEMPLATE.format(
        cities=", ".join(MAJOR_CITIES),
        price_data=price_data,
        utilities_min=UTILITIES_RANGE[0],
        utilities_max=UTILITIES_RANGE[1],
        documents=documents,
        scam_warnings=scam_warnings
    )
