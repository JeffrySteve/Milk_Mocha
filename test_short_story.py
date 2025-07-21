"""
Test the updated short story generation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.safe_gemini import SafeGeminiService

print("🧪 Testing SHORT story generation...")

service = SafeGeminiService()

# Test the new short story prompt
story_prompt = (
    "Tell a very short, funny story in just 1-2 sentences (under 30 words) from the perspective of "
    "Milk Mocha, a cute desktop pet. Make it humorous about computer life. "
    "Start with '📚' emoji and include one other emoji."
)

print("📚 Getting short story...")
story = service.get_message_with_timeout("random", story_prompt)

print(f"\n✅ SHORT Story:")
print(f"{'='*40}")
print(story)
print(f"{'='*40}")
print(f"Word count: ~{len(story.split())} words")
print(f"Character count: {len(story)} characters")

if len(story.split()) <= 35:
    print("✅ Perfect length! Short and sweet!")
else:
    print("⚠️ Still a bit long, but better than before")
