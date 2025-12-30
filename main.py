"""
Main CLI Interface for Captain Jack Sparrow Chatbot
"""

import os
import sys

# Force UTF-8 encoding for stdout (fix for Windows terminals)
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Older python versions might not support reconfigure, but 3.7+ does

from src.chatbot import SparrowBot


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🏴‍☠️  CAPTAIN JACK SPARROW AI CHATBOT  🏴‍☠️           ║
    ║                                                              ║
    ║           "Not all treasure is silver and gold"             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help information"""
    help_text = """
    Commands:
    - Type your message and press Enter to chat
    - 'help' or '?' : Show this help message
    - 'reset' : Clear conversation history
    - 'quit' or 'exit' : Exit the chatbot
    
    Features:
    - Ask about Jack Sparrow, the Black Pearl, and pirate lore
    - Request calculations (e.g., "Calculate 25 * 4")
    - Have continuous conversations with memory
    """
    print(help_text)


def main():
    """Main function to run the chatbot"""
    # Print banner
    print_banner()
    
    # Get knowledge base path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    kb_path = os.path.join(script_dir, "data", "sparrow_facts.txt")
    
    # Initialize the bot
    try:
        bot = SparrowBot(knowledge_base_path=kb_path)
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)
    
    print("\nType 'help' for commands, or start chatting!")
    print("=" * 64)
    
    # Initial greeting
    greeting = bot.chat("Hello!")
    print(f"\n🏴‍☠️ Jack: {greeting}\n")
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                farewell = bot.chat("Goodbye!")
                print(f"\n🏴‍☠️ Jack: {farewell}")
                print("\n⚓ Fair winds and following seas! ⚓\n")
                break
            
            elif user_input.lower() in ['help', '?']:
                print_help()
                continue
            
            elif user_input.lower() == 'reset':
                bot.reset_conversation()
                print("✓ Conversation history cleared!\n")
                continue
            
            # Get bot response
            response = bot.chat(user_input)
            print(f"\n🏴‍☠️ Jack: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\n⚓ Interrupted! Farewell, mate! ⚓\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == "__main__":
    main()
