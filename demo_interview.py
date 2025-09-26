#!/usr/bin/env python3
"""
Demo script for CEREBUS Interview Question functionality
Demonstrates the new interview features added to the malware analysis system
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from interview_questions import InterviewQuestionGenerator
except ImportError:
    print("❌ Cannot import interview_questions module")
    sys.exit(1)

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧠 CEREBUS - {title}")
    print("="*60)

def print_section(title):
    """Print a section header"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_basic_functionality():
    """Demonstrate basic question generation"""
    print_section("Basic Question Generation")
    
    generator = InterviewQuestionGenerator()
    
    # Get a random question
    question = generator.get_random_question()
    print(f"Random Question:")
    print(f"Topic: {question['topic']} | Difficulty: {question['difficulty']}")
    print(f"Q: {question['question']}")
    print(f"A: {question['answer']}")
    
    # Get filtered questions
    print(f"\nFiltered Question (Malware Analysis, Beginner):")
    filtered_q = generator.get_random_question(topic='malware_analysis', difficulty='beginner')
    print(f"Q: {filtered_q['question']}")
    print(f"A: {filtered_q['answer']}")

def demo_question_sets():
    """Demonstrate question set generation"""
    print_section("Question Set Generation")
    
    generator = InterviewQuestionGenerator()
    
    # Generate a small question set
    questions = generator.get_question_set(count=3, topic='malware_analysis')
    
    print(f"Generated {len(questions)} questions for malware analysis:")
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. [{question['difficulty'].upper()}] {question['question']}")
    
    # Generate with scenarios
    print(f"\nQuestion set with scenarios:")
    scenario_questions = generator.get_question_set(count=4, include_scenarios=True)
    
    for i, question in enumerate(scenario_questions, 1):
        if question.get('type') == 'scenario':
            print(f"\n{i}. [SCENARIO] {question['question'][:80]}...")
            print(f"   Expected approach: {len(question['expected_approach'])} steps")
        else:
            print(f"\n{i}. [{question['difficulty'].upper()}] {question['question'][:80]}...")

def demo_statistics():
    """Demonstrate statistics and metadata"""
    print_section("Question Statistics")
    
    generator = InterviewQuestionGenerator()
    
    # Show available topics and difficulties
    topics = generator.get_available_topics()
    difficulties = generator.get_available_difficulties()
    
    print(f"Available Topics: {', '.join(topics)}")
    print(f"Difficulty Levels: {', '.join(difficulties)}")
    
    # Show detailed statistics
    stats = generator.get_topic_stats()
    print(f"\nDetailed Statistics:")
    
    total_questions = 0
    for topic, counts in stats.items():
        print(f"  {topic.replace('_', ' ').title()}:")
        for difficulty, count in counts.items():
            if difficulty != 'total':
                print(f"    {difficulty.title()}: {count} questions")
        print(f"    Total: {counts['total']} questions")
        total_questions += counts['total']
    
    print(f"\n📊 Total Questions Available: {total_questions}")
    print(f"📋 Total Scenarios: {len(generator.scenarios)}")

def demo_api_simulation():
    """Simulate API endpoint responses"""
    print_section("API Endpoint Simulation")
    
    generator = InterviewQuestionGenerator()
    
    # Simulate GET /interview/question?difficulty=intermediate
    print("GET /interview/question?difficulty=intermediate")
    api_response = generator.get_random_question(difficulty='intermediate')
    print(json.dumps(api_response, indent=2)[:300] + "...")
    
    # Simulate POST /interview/question-set
    print(f"\nPOST /interview/question-set")
    print("Request body: {'count': 2, 'topic': 'incident_response'}")
    question_set_response = {
        "questions": generator.get_question_set(count=2, topic='incident_response'),
        "count": 2,
        "filters": {"topic": "incident_response", "difficulty": None}
    }
    print(f"Response: {len(question_set_response['questions'])} questions returned")
    
    # Simulate GET /api/interview/topics
    print(f"\nGET /api/interview/topics")
    topics_response = {
        "topics": generator.get_available_topics(),
        "difficulties": generator.get_available_difficulties(),
        "stats": generator.get_topic_stats()
    }
    print(f"Response: {len(topics_response['topics'])} topics, {len(topics_response['difficulties'])} difficulty levels")

def demo_interview_session():
    """Simulate an interview session"""
    print_section("Simulated Interview Session")
    
    generator = InterviewQuestionGenerator()
    
    print("Starting a practice interview session...")
    print("Configuration: Mixed topics, Intermediate level, 3 questions")
    
    questions = generator.get_question_set(
        count=3, 
        difficulty='intermediate',
        include_scenarios=True
    )
    
    print(f"\n📝 Interview Session - {len(questions)} Questions Generated")
    print(f"⏰ Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*50}")
        print(f"Question {i}/{len(questions)}")
        print(f"Topic: {question['topic'].replace('_', ' ').title()} | Difficulty: {question['difficulty'].title()}")
        
        if question.get('type') == 'scenario':
            print(f"Type: Scenario Question")
            print(f"\nScenario:")
            print(f"{question['question']}")
            print(f"\nExpected Approach ({len(question['expected_approach'])} steps):")
            for j, step in enumerate(question['expected_approach'], 1):
                print(f"  {j}. {step}")
        else:
            print(f"\nQuestion:")
            print(f"{question['question']}")
            print(f"\nAnswer:")
            print(f"{question['answer']}")
    
    print(f"\n✅ Interview session completed!")

def demo_export_functionality():
    """Demonstrate export functionality"""
    print_section("Export/Import Functionality")
    
    generator = InterviewQuestionGenerator()
    
    # Export to a temporary file
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file.close()
    
    print(f"Exporting questions to: {temp_file.name}")
    success = generator.export_questions(temp_file.name)
    
    if success:
        print("✅ Export successful!")
        
        # Show file size
        file_size = os.path.getsize(temp_file.name)
        print(f"📁 File size: {file_size:,} bytes")
        
        # Show structure
        with open(temp_file.name, 'r') as f:
            data = json.load(f)
        
        print(f"📊 Export contains:")
        print(f"   - {len(data['questions'])} topic categories")
        print(f"   - {len(data['scenarios'])} scenarios")
        print(f"   - {data['metadata']['total_questions']} total questions")
        
        # Cleanup
        os.unlink(temp_file.name)
        print("🗑️ Temporary file cleaned up")
    else:
        print("❌ Export failed!")

def main():
    """Main demo function"""
    print_header("Interview Question System Demo")
    print("🛡️ AI-Powered Malware Analysis Shield - Educational Features")
    
    print("\nThis demo showcases the new interview question functionality")
    print("added to the CEREBUS malware analysis system.")
    
    try:
        demo_basic_functionality()
        demo_question_sets()
        demo_statistics()
        demo_api_simulation()
        demo_interview_session()
        demo_export_functionality()
        
        print_header("Demo Complete")
        print("🎉 All interview features demonstrated successfully!")
        print("\n📚 Educational Benefits:")
        print("   • Practice cybersecurity interview questions")
        print("   • Test malware analysis knowledge")
        print("   • Scenario-based learning")
        print("   • Adaptive difficulty levels")
        print("   • API integration for custom applications")
        
        print("\n🌐 Web Interface:")
        print("   • Visit /interview for the web interface")
        print("   • Practice sessions at /interview/practice")
        print("   • API endpoints at /api/interview/*")
        
        print("\n🔗 Integration:")
        print("   • Seamlessly integrated with existing CEREBUS features")
        print("   • Complements malware analysis workflows")
        print("   • Enhances training and skill assessment")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)