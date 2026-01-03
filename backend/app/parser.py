from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Optional
import os

# Define the expected output structure
class ListingInfo(BaseModel):
    location: str = Field(description="The city or neighborhood name, strictly without timestamps or 'ago'.")
    date_posted: Optional[str] = Field(description="The posted date in YYYY-MM-DD format if available, else null.")
    date_updated: Optional[str] = Field(description="The updated date in YYYY-MM-DD format if available, else null.")

class Parser:
    def __init__(self):
        # Initialize Ollama - pointing to host.docker.internal for Mac/Docker
        try:
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
            self.llm = ChatOllama(model="mistral", temperature=0, format="json", base_url=ollama_url)
            self.parser = JsonOutputParser(pydantic_object=ListingInfo)
        except Exception as e:
            print(f"Error initializing Parser: {e}")
            self.llm = None

    async def parse_listing_fragment(self, raw_location: str, raw_date_text: str) -> dict:
        """
        Parses raw location string (e.g., '5 mins agosanta cruz') and date text
        into a clean structure.
        """
        print(f"[Parser] Input: raw_location='{raw_location}', raw_date='{raw_date_text}'")

        if not self.llm:
            print("[Parser] LLM not initialized, returning raw data")
            return {"location": raw_location, "date_posted": None, "date_updated": None}

        # Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a specialized data cleaning assistant. Extract the city/neighborhood name and dates from the provided raw text snippets. Remove any relative time phrases like '5 mins ago' or '2h ago'. Return ONLY JSON."),
            ("user", """
            Raw Location Text: {raw_location}
            Raw Date Text: {raw_date_text}
            
            Format instructions:
            {format_instructions}
            """)
        ])

        chain = prompt | self.llm | self.parser

        try:
            response = await chain.ainvoke({
                "raw_location": raw_location,
                "raw_date_text": raw_date_text,
                "format_instructions": self.parser.get_format_instructions()
            })
            print(f"[Parser] Success: {response}")
            return response
        except Exception as e:
            print(f"[Parser] Failed: {e}")
            return {"location": raw_location, "date_posted": None, "date_updated": None}

# Global instance
parser = Parser()
