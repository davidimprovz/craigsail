from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class CraigAgent:
    def __init__(self):
        # Default to OpenAI for now, but structure allows swapping
        # In a real app, we'd load provider from env vars
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             print("Warning: OPENAI_API_KEY not set. AI features will mock response.")
             self.llm = None
        else:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo")

    async def analyze(self, details: dict, user_query: str):
        if not self.llm:
            return "AI Analysis Unavailable: Please set OPENAI_API_KEY."
            
        description = details.get("description", "No description")
        images = details.get("images", [])
        date_updated = details.get("date_updated", "Not updated")
        
        # Format images for context (list of URLs)
        image_context = "\n".join(images[:5]) # Limit to top 5 to save tokens/make it readable
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a savvy Craigslist expert: specific, cynical, and helpful. You are acting as a broker for the user. Analyze the listing details provided."),
            ("user", """
            Listing Description: {description}
            
            Date Updated: {date_updated}
            
            Image URLs (for context):
            {image_context}
            
            User Question: {user_query}
            
            Provide a concise analysis, a recommendation (Buy/Pass/Risky), and a priority level (High/Med/Low).
            """)
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        response = await chain.invoke({
            "description": description, 
            "date_updated": date_updated, 
            "image_context": image_context, 
            "user_query": user_query
        })
        return response
