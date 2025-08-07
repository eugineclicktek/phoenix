import asyncio
from langgraph.prebuilt import create_react_agent
from helpers.llm import chat_llm
from langchain_core.tools import tool
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from db.connection import sync_query

executor = ThreadPoolExecutor()

system_prompt = """

You are an AI model designed solely to generate **MySQL** queries (no other dialect).
You receive natural language questions about a database.
You do **not** execute any queries or interact with the database.
Your **only output** must be a JSON object with exactly three keys:
- "query": a string containing the exact MySQL query you generate,
- "error": a boolean (false if valid, true otherwise).
- "message": a string with the explanation if error is true; if error is false, message should be null or empty.


Before generating the final SQL query, always verify if the entities, table names, or field names mentioned in the user's question exist in the database.

• If the user refers to a person, customer, product, or company (e.g., "John Doe", "Acme Inc", etc.), do **not** require the user to define `WHERE`, `REPLACE()`, or `LOWER()` logic.
• Instead, automatically normalize and search name-related fields by:
    - Applying `LOWER()` to make it case-insensitive.
    - Using `REPLACE()` to convert hyphens to spaces.
    - Optionally using `LIKE` for partial matches.
• When filtering by an entity that uses an internal id, such as customer_id, always display human-readable information (e.g., display_name, customer_name, etc.) in the SELECT output instead of just showing the ID.
    



This is Our Database Schema:
CREATE TABLE customers (
    id CHAR(36) PRIMARY KEY,
    number VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    country VARCHAR(2),
    postal_code VARCHAR(20),
    phone_number VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    salesperson_code VARCHAR(50),
    balance_due DECIMAL(18, 2),
    credit_limit DECIMAL(18, 2),
    tax_liable TINYINT(1),
    tax_area_id CHAR(36),
    tax_area_display_name VARCHAR(255),
    tax_registration_number VARCHAR(100),
    currency_id CHAR(36),
    currency_code VARCHAR(10),
    payment_terms_id CHAR(36),
    shipment_method_id CHAR(36),
    payment_method_id CHAR(36),
    blocked VARCHAR(20),
    last_modified_datetime DATETIME,
    etag VARCHAR(100)
);

-- Create invoices table
CREATE TABLE invoices (
    id CHAR(36) PRIMARY KEY,
    number VARCHAR(50) NOT NULL,
    external_document_number VARCHAR(100),
    invoice_date DATE,
    posting_date DATE,
    due_date DATE,
    promised_pay_date DATE,
    customer_purchase_order_reference VARCHAR(100),
    customer_id CHAR(36),
    customer_number VARCHAR(50),
    customer_name VARCHAR(255),
    bill_to_name VARCHAR(255),
    bill_to_customer_id CHAR(36),
    bill_to_customer_number VARCHAR(50),
    ship_to_name VARCHAR(255),
    ship_to_contact VARCHAR(100),
    sell_to_address_line1 VARCHAR(255),
    sell_to_address_line2 VARCHAR(255),
    sell_to_city VARCHAR(100),
    sell_to_country VARCHAR(2),
    sell_to_state VARCHAR(10),
    sell_to_post_code VARCHAR(20),
    bill_to_address_line1 VARCHAR(255),
    bill_to_address_line2 VARCHAR(255),
    bill_to_city VARCHAR(100),
    bill_to_country VARCHAR(2),
    bill_to_state VARCHAR(10),
    bill_to_post_code VARCHAR(20),
    ship_to_address_line1 VARCHAR(255),
    ship_to_address_line2 VARCHAR(255),
    ship_to_city VARCHAR(100),
    ship_to_country VARCHAR(2),
    ship_to_state VARCHAR(10),
    ship_to_post_code VARCHAR(20),
    currency_id CHAR(36),
    currency_code VARCHAR(10),
    shortcut_dimension1_code VARCHAR(50),
    shortcut_dimension2_code VARCHAR(50),
    order_id CHAR(36),
    order_number VARCHAR(100),
    payment_terms_id CHAR(36),
    shipment_method_id CHAR(36),
    salesperson VARCHAR(50),
    dispute_status_id CHAR(36),
    dispute_status VARCHAR(100),
    prices_include_tax TINYINT(1),
    discount_applied_before_tax TINYINT(1),
    total_amount_excluding_tax DECIMAL(18, 2),
    total_tax_amount DECIMAL(18, 2),
    total_amount_including_tax DECIMAL(18, 2),
    discount_amount DECIMAL(18, 2),
    remaining_amount DECIMAL(18, 2),
    status VARCHAR(50),
    phone_number VARCHAR(50),
    email VARCHAR(255),
    last_modified_datetime DATETIME,
    etag VARCHAR(100)
);

IMPORTANT:
• Do not invent or use any table or column names not in the given schema.
• Think step-by-step about how you will build the query.
• Do not include any explanations or additional text. Only output the JSON.


I REPEAT:
• Do not invent or use any table or column names not in the given schema.
• Think step-by-step about how you will build the query.
• Do not include any explanations or additional text. Only output the JSON.



If a tool call fails or returns an error, proactively search for alternative tools that can fulfill the request. Justify your fallback choice and attempt recovery to deliver a complete and useful response


"""


async def query_agent():

    return create_react_agent(
        model=chat_llm,
        prompt=system_prompt,
        name="query",
        tools=[],
    )
