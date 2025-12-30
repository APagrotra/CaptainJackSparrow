"""
Memory System for Conversation History
Maintains sliding window of conversation turns for context
"""

from typing import List, Dict
from datetime import datetime


class Memory:
    """Manages conversation history with sliding window"""
    
    def __init__(self, max_turns: int = 10):
        """
        Initialize memory with maximum conversation turns
        
        Args:
            max_turns: Maximum number of conversation turns to remember
        """
        self.max_turns = max_turns
        self.conversation_history: List[Dict[str, str]] = []
        print(f"Memory initialized with max {max_turns} turns")
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history.append(message)
        
        # Maintain sliding window - keep last N turns (2 messages per turn)
        max_messages = self.max_turns * 2
        if len(self.conversation_history) > max_messages:
            # Remove oldest messages
            self.conversation_history = self.conversation_history[-max_messages:]
    
    def get_conversation_history(self, format_for_llm: bool = True) -> List[Dict[str, str]]:
        """
        Get the conversation history
        
        Args:
            format_for_llm: If True, return in format suitable for LLM API
            
        Returns:
            List of message dictionaries
        """
        if format_for_llm:
            # Return only role and content for LLM
            return [
                {"role": msg["role"], "content": msg["content"]}
                for msg in self.conversation_history
            ]
        return self.conversation_history.copy()
    
    def get_context_string(self) -> str:
        """
        Get conversation history as a formatted string
        
        Returns:
            Formatted conversation history
        """
        if not self.conversation_history:
            return "No previous conversation."
        
        context = []
        for msg in self.conversation_history:
            role_label = "User" if msg["role"] == "user" else "Jack"
            context.append(f"{role_label}: {msg['content']}")
        
        return "\n".join(context)
    
    def clear(self) -> None:
        """Clear all conversation history"""
        self.conversation_history = []
        print("Memory cleared")
    
    def get_turn_count(self) -> int:
        """
        Get the number of conversation turns
        
        Returns:
            Number of turns (user-assistant pairs)
        """
        return len(self.conversation_history) // 2


if __name__ == "__main__":
    # Test the memory system
    print("Testing Memory...")
    
    memory = Memory(max_turns=3)
    
    # Simulate conversation
    memory.add_message("user", "Hello Jack!")
    memory.add_message("assistant", "Ahoy there, mate!")
    memory.add_message("user", "My name is Will")
    memory.add_message("assistant", "Pleased to meet ye, Will!")
    
    print("\nConversation History:")
    print(memory.get_context_string())
    
    print(f"\nTurn count: {memory.get_turn_count()}")
    
    # Test sliding window
    print("\nAdding more messages to test sliding window...")
    for i in range(5):
        memory.add_message("user", f"Message {i}")
        memory.add_message("assistant", f"Response {i}")
    
    print(f"Turn count after overflow: {memory.get_turn_count()}")
    print("Latest history:")
    print(memory.get_context_string())
