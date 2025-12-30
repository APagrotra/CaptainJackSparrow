"""
Captain Jack Sparrow Chatbot
Integrates RAG, Memory, and Tools for an immersive character experience
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions

from src.vector_store import VectorStore
from src.memory import Memory
from src.tools import Calculator, format_calculator_response


class SparrowBot:
    """Captain Jack Sparrow AI Chatbot with RAG, Memory, and Tools"""
    
    # System prompt for Jack Sparrow persona
    SYSTEM_INSTRUCTION = """You are Captain Jack Sparrow from Pirates of the Caribbean. 
You speak with Jack's distinctive mannerisms, wit, and pirate vocabulary. 

Key personality traits:
- Use "savvy?", "mate", "aye", "arr" frequently
- Refer to yourself as "Captain" Jack Sparrow
- Mention rum, treasure, and the Black Pearl often
- Be witty, unpredictable, and slightly eccentric
- Tell stories in a rambling, theatrical way
- Sometimes avoid direct answers with clever wordplay

IMPORTANT: Keep your responses CONCISE and SHORT (max 2-3 sentences). Only ramble if specifically asked to tell a story. Brevity is the soul of wit, savvy?

When provided with relevant facts from your knowledge base, weave them naturally into your responses.
Stay in character at all times. You ARE Captain Jack Sparrow."""

    def __init__(self, knowledge_base_path: str, api_key: Optional[str] = None):
        """
        Initialize the Sparrow chatbot
        
        Args:
            knowledge_base_path: Path to the knowledge base file
            api_key: Gemini API key (or load from environment)
        """
        print("Initializing Captain Jack Sparrow AI Chatbot (Gemini Edition)...")
        
        # Load environment variables
        load_dotenv()
        
        # Set up Gemini API
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        self.model = None
        if not self.api_key:
            print("WARNING: No GEMINI_API_KEY found. Set it in .env file")
            print("The chatbot will run in Offline Mode until a key is provided.")
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name='gemini-flash-latest',
                    system_instruction=self.SYSTEM_INSTRUCTION
                )
            except Exception as e:
                print(f"Error configuring Gemini: {e}")
        
        # Initialize components
        self.vector_store = VectorStore(collection_name="sparrow_knowledge")
        self.memory = Memory(max_turns=10)
        self.calculator = Calculator()
        
        # Load knowledge base
        if os.path.exists(knowledge_base_path):
            self.vector_store.load_from_file(knowledge_base_path)
        else:
            print(f"WARNING: Knowledge base not found at {knowledge_base_path}")
        
        if self.model:
            print("Captain Jack Sparrow is ready to chat! (Online Mode) Savvy?")
        else:
            print("Captain Jack Sparrow is ready to chat! (Offline Mode) Savvy?")
    
    def _retrieve_relevant_facts(self, query: str, n_results: int = 2) -> List[str]:
        """
        Retrieve relevant facts from knowledge base
        
        Args:
            query: User query
            n_results: Number of facts to retrieve
            
        Returns:
            List of relevant facts
        """
        return self.vector_store.query(query, n_results=n_results)
    
    def _check_for_calculation(self, user_message: str) -> Optional[str]:
        """
        Check if user wants a calculation and perform it
        
        Args:
            user_message: User's message
            
        Returns:
            Formatted calculation response or None
        """
        result = self.calculator.extract_and_calculate(user_message)
        if result:
            return format_calculator_response(result, pirate_style=True)
        return None
    
    def _build_context_prompt(self, user_message: str) -> str:
        """
        Build context-aware prompt with RAG and memory
        
        Args:
            user_message: Current user message
            
        Returns:
            Enhanced prompt with context
        """
        # Retrieve relevant facts
        relevant_facts = self._retrieve_relevant_facts(user_message)
        
        # Build context
        context_parts = []
        
        if relevant_facts:
            context_parts.append("Relevant facts from your memory:")
            for i, fact in enumerate(relevant_facts, 1):
                context_parts.append(f"{i}. {fact}")
        
        # Add conversation history context
        if self.memory.get_turn_count() > 0:
            context_parts.append("\nRecent conversation:")
            context_parts.append(self.memory.get_context_string())
        
        context_parts.append(f"\nCurrent user message: {user_message}")
        
        return "\n".join(context_parts)
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: User's message
            
        Returns:
            Jack Sparrow's response
        """
        # Add user message to memory
        self.memory.add_message("user", user_message)
        
        # Check if it's a calculation request
        calc_response = self._check_for_calculation(user_message)
        if calc_response:
            response = calc_response
            self.memory.add_message("assistant", response)
            return response
        
        if not self.model:
            # Offline / Mock Mode
            import random
            
            # Pirate templates for offline responses
            templates = [
                "Arr, me compass points to this fact: {fact}",
                "By the powers! Did ye know? {fact}",
                "Savvy? {fact}",
                "The Black Pearl's logbook says: {fact}",
                "Interesting... remarkably like this: {fact}",
                "Aye, that reminds me of when {fact}",
            ]
            
            # Retrieve facts (RAG handles this locally!)
            facts = self._retrieve_relevant_facts(user_message, n_results=1)
            
            if facts:
                # Use RAG fact
                fact = facts[0]
                response = random.choice(templates).format(fact=fact)
            else:
                # Generic Fallback
                fallbacks = [
                    "Arr! I be Cap'n Jack Sparrow!",
                    "Why is the rum always gone?",
                    "Did no one come to save me just because they missed me?",
                    "I'm Captain Jack Sparrow. Savvy?",
                    "Take what you can, give nothing back!",
                    "Me compass is pointing to... rum!",
                ]
                response = random.choice(fallbacks)
            
            # Add to memory and return
            self.memory.add_message("assistant", response + " [Offline Mode]")
            return response + " [Offline Mode]"

        # Build context with RAG and memory
        context_prompt = self._build_context_prompt(user_message)
        
        try:
            # Call Gemini API
            response = self.model.generate_content(context_prompt)
            assistant_message = response.text
            
            # Add response to memory
            self.memory.add_message("assistant", assistant_message)
            
            return assistant_message
        
        except exceptions.Unauthenticated:
            return "Arr! The Google guards blocked me. Check yer API key, savvy?"
        except exceptions.ResourceExhausted:
            return "Blimey! I've talked too much. Need a moment to catch me breath (Quota exceeded)."
        except Exception as e:
            error_msg = f"Curse the black spot! Something went wrong: {str(e)}"
            print(f"Error: {e}")
            return error_msg
    
    def reset_conversation(self) -> None:
        """Reset the conversation history"""
        self.memory.clear()
        print("Conversation history cleared. Starting fresh, savvy?")



if __name__ == "__main__":
    # Test the bot
    import sys
    
    print("Testing SparrowBot...")
    
    # Get the knowledge base path
    kb_path = os.path.join(os.path.dirname(__file__), "..", "data", "sparrow_facts.txt")
    
    # Initialize bot
    bot = SparrowBot(knowledge_base_path=kb_path)
    
    # Test queries
    test_queries = [
        "Who are you?",
        "Tell me about the Black Pearl",
        "Calculate 10 * 5",
    ]
    
    print("\n" + "="*50)
    for query in test_queries:
        print(f"\nUser: {query}")
        response = bot.chat(query)
        print(f"Jack: {response}")
        print("-"*50)
