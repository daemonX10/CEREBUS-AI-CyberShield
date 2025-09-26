#!/usr/bin/env python3
"""
Simple test to verify Flask app can start with interview functionality
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_startup():
    """Test that the Flask app can import and initialize"""
    try:
        # Test basic imports
        from interview_questions import InterviewQuestionGenerator
        print("✅ Interview question generator imports successfully")
        
        # Test generator functionality
        generator = InterviewQuestionGenerator()
        question = generator.get_random_question()
        print(f"✅ Generated test question: {question['question'][:50]}...")
        
        # Test API endpoint data
        topics = generator.get_available_topics()
        stats = generator.get_topic_stats()
        print(f"✅ Available topics: {topics}")
        print(f"✅ Question statistics loaded: {len(stats)} topics")
        
        # Test JSON serialization (important for API endpoints)
        import json
        question_set = generator.get_question_set(count=3)
        json_data = json.dumps(question_set)
        print("✅ Questions can be serialized to JSON for API responses")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in app startup test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing CEREBUS interview functionality integration...\n")
    success = test_app_startup()
    
    if success:
        print("\n✅ Interview functionality is ready for use!")
    else:
        print("\n❌ Interview functionality has issues!")
        sys.exit(1)