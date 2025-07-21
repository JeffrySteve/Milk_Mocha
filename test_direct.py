"""
Direct test for Gemini story generation
"""
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.safe_gemini import SafeGeminiService
    
    print("🧪 Testing Gemini AI story generation...")
    
    # Create service
    service = SafeGeminiService()
    
    # Test story prompt
    story_prompt = (
        "Tell a very short, funny story (under 100 words) from the perspective of "
        "Milk Mocha, a cute desktop pet. The story should be humorous, family-friendly, "
        "and relate to computer/digital life. Include emojis and make it entertaining! "
        "Start with either '📚' or '📖' emoji."
    )
    
    print("📚 Requesting AI story...")
    
    # Get story
    story = service.get_message_with_timeout("random", story_prompt)
    
    print(f"\n✅ Story received:")
    print(f"{'='*50}")
    print(story)
    print(f"{'='*50}")
    print(f"Length: {len(story)} characters")
    
    # Check if it's AI generated
    if "📚" in story or "📖" in story:
        print("🤖 This appears to be an AI-generated story!")
    else:
        print("⚠️ This might be a fallback message")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
