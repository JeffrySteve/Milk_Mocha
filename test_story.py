"""
Quick test for story generation functionality
"""
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.gemini_service import GeminiService

def test_story_generation():
    print("🧪 Testing story generation functionality...")
    
    # Create GeminiService instance
    gemini = GeminiService()
    
    # Test the story prompt that's used in the pet
    story_prompt = (
        "Tell a very short, funny story (under 100 words) from the perspective of "
        "Milk Mocha, a cute desktop pet. The story should be humorous, family-friendly, "
        "and relate to computer/digital life. Include emojis and make it entertaining! "
        "Start with either '📚' or '📖' emoji."
    )
    
    print("📚 Testing story generation...")
    
    # Test the get_message_with_timeout method
    try:
        story = gemini.get_message_with_timeout("random", story_prompt, timeout=5)
        print(f"✅ Story generated successfully:")
        print(f"   {story}")
        print(f"   Length: {len(story)} characters")
        
        # Test if it's a fallback story (fallback stories contain specific keywords)
        if "Once upon a time" in story or "True story" in story or "antivirus" in story:
            print("⚠️ This appears to be a fallback story (AI not available)")
        else:
            print("🤖 This appears to be an AI-generated story!")
            
    except Exception as e:
        print(f"❌ Error testing story: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_story_generation()
