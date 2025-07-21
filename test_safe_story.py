"""
Simple test for story generation
"""
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.safe_gemini import SafeGeminiService

def test_story_generation():
    print("🧪 Testing story generation with SafeGeminiService...")
    
    # Create SafeGeminiService instance
    gemini = SafeGeminiService()
    
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
        story = gemini.get_message_with_timeout("random", story_prompt)
        print(f"✅ Story generated successfully:")
        print(f"   {story}")
        print(f"   Length: {len(story)} characters")
        
        # Check if it's using fallback messages (contains specific patterns)
        fallback_indicators = ["Hope you're having", "Hello there", "Time for a little break", "Ready for some fun"]
        is_fallback = any(indicator in story for indicator in fallback_indicators)
        
        if is_fallback:
            print("⚠️ This appears to be a fallback message (AI not available)")
            print("📝 This means:")
            print("   - google-generativeai package is not installed, OR")
            print("   - GEMINI_API_KEY environment variable is not set")
        else:
            print("🤖 This appears to be an AI-generated story!")
            
    except Exception as e:
        print(f"❌ Error testing story: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_story_generation()
