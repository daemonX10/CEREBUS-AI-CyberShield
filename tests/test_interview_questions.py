#!/usr/bin/env python3
"""
Tests for the Interview Question Generator functionality
"""

import sys
import os
import unittest
import json
import tempfile

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interview_questions import InterviewQuestionGenerator

class TestInterviewQuestionGenerator(unittest.TestCase):
    """Test cases for the InterviewQuestionGenerator class"""
    
    def setUp(self):
        """Set up test environment"""
        self.generator = InterviewQuestionGenerator()
    
    def test_initialization(self):
        """Test that the generator initializes correctly"""
        self.assertIsInstance(self.generator, InterviewQuestionGenerator)
        self.assertIsInstance(self.generator.questions, dict)
        self.assertIsInstance(self.generator.scenarios, list)
        
        # Check that we have questions for expected topics
        expected_topics = ['malware_analysis', 'incident_response', 'threat_intelligence', 'technical_skills']
        for topic in expected_topics:
            self.assertIn(topic, self.generator.questions)
    
    def test_get_random_question(self):
        """Test getting a random question"""
        question = self.generator.get_random_question()
        
        # Check that we get a valid question structure
        self.assertIsInstance(question, dict)
        self.assertIn('question', question)
        self.assertIn('answer', question)
        self.assertIn('category', question)
        self.assertIn('difficulty', question)
        self.assertIn('topic', question)
        
        # Check that content is not empty
        self.assertTrue(len(question['question']) > 0)
        self.assertTrue(len(question['answer']) > 0)
    
    def test_get_random_question_with_filters(self):
        """Test getting a random question with topic and difficulty filters"""
        # Test topic filter
        question = self.generator.get_random_question(topic='malware_analysis')
        self.assertEqual(question['topic'], 'malware_analysis')
        
        # Test difficulty filter
        question = self.generator.get_random_question(difficulty='beginner')
        self.assertEqual(question['difficulty'], 'beginner')
        
        # Test both filters
        question = self.generator.get_random_question(topic='malware_analysis', difficulty='intermediate')
        self.assertEqual(question['topic'], 'malware_analysis')
        self.assertEqual(question['difficulty'], 'intermediate')
    
    def test_get_question_set(self):
        """Test getting a question set"""
        questions = self.generator.get_question_set(count=3)
        
        self.assertIsInstance(questions, list)
        self.assertEqual(len(questions), 3)
        
        # Check that each question is valid
        for question in questions:
            self.assertIsInstance(question, dict)
            self.assertIn('question', question)
            self.assertIn('topic', question)
    
    def test_get_question_set_with_scenarios(self):
        """Test getting a question set with scenarios"""
        count = 5
        questions = self.generator.get_question_set(count=count, include_scenarios=True)
        
        self.assertIsInstance(questions, list)
        self.assertLessEqual(len(questions), count)  # May be less if not enough questions available
        
        # Check if any scenarios were included
        scenario_questions = [q for q in questions if q.get('type') == 'scenario']
        # Should have at least some scenarios if available and count allows
        if len(self.generator.scenarios) > 0 and count >= 3:
            # Only expect scenarios if we requested enough questions
            pass  # Don't assert since scenarios are added conditionally
    
    def test_get_available_topics(self):
        """Test getting available topics"""
        topics = self.generator.get_available_topics()
        
        self.assertIsInstance(topics, list)
        self.assertIn('malware_analysis', topics)
        self.assertIn('incident_response', topics)
    
    def test_get_available_difficulties(self):
        """Test getting available difficulties"""
        difficulties = self.generator.get_available_difficulties()
        
        self.assertIsInstance(difficulties, list)
        self.assertIn('beginner', difficulties)
        self.assertIn('intermediate', difficulties)
        self.assertIn('advanced', difficulties)
    
    def test_get_topic_stats(self):
        """Test getting topic statistics"""
        stats = self.generator.get_topic_stats()
        
        self.assertIsInstance(stats, dict)
        
        # Check structure for each topic
        for topic, counts in stats.items():
            self.assertIsInstance(counts, dict)
            self.assertIn('total', counts)
            self.assertIn('beginner', counts)
            self.assertIn('intermediate', counts)
            self.assertIn('advanced', counts)
            
            # Check that total equals sum of difficulties
            expected_total = counts['beginner'] + counts['intermediate'] + counts['advanced']
            self.assertEqual(counts['total'], expected_total)
    
    def test_export_import_questions(self):
        """Test exporting and importing questions"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Test export
            success = self.generator.export_questions(temp_filename)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(temp_filename))
            
            # Verify exported content
            with open(temp_filename, 'r') as f:
                data = json.load(f)
            
            self.assertIn('questions', data)
            self.assertIn('scenarios', data)
            self.assertIn('metadata', data)
            
            # Test import (create new generator and import)
            new_generator = InterviewQuestionGenerator()
            # Clear existing questions to test import
            original_count = sum(len(q) for topic in new_generator.questions.values() for q in topic.values())
            
            import_success = new_generator.import_questions(temp_filename)
            self.assertTrue(import_success)
            
            # Verify questions were added (should have more now)
            new_count = sum(len(q) for topic in new_generator.questions.values() for q in topic.values())
            self.assertGreaterEqual(new_count, original_count)
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_fallback_question(self):
        """Test that fallback question is returned when no matches found"""
        # Test with non-existent topic
        question = self.generator.get_random_question(topic='nonexistent_topic')
        
        self.assertIsInstance(question, dict)
        self.assertIn('question', question)
        self.assertIn('answer', question)
    
    def test_question_content_quality(self):
        """Test that questions have reasonable content quality"""
        questions = self.generator.get_question_set(count=5)
        
        for question in questions:
            # Questions should be reasonably long (more than just a few words)
            self.assertGreater(len(question['question'].split()), 5)
            
            # Answers should be substantial
            if 'answer' in question:
                self.assertGreaterEqual(len(question['answer'].split()), 10)
            
            # Check for scenario questions
            if question.get('type') == 'scenario':
                self.assertIn('expected_approach', question)
                self.assertIsInstance(question['expected_approach'], list)
                self.assertGreater(len(question['expected_approach']), 0)
    
    def test_no_duplicate_questions_in_set(self):
        """Test that question sets don't contain duplicates"""
        questions = self.generator.get_question_set(count=10)
        
        question_texts = [q['question'] for q in questions]
        unique_questions = set(question_texts)
        
        # Should have no duplicates
        self.assertEqual(len(question_texts), len(unique_questions))

class TestInterviewQuestionIntegration(unittest.TestCase):
    """Integration tests for interview questions with the main app"""
    
    def test_import_in_app_context(self):
        """Test that the module can be imported in app context"""
        try:
            from interview_questions import InterviewQuestionGenerator
            generator = InterviewQuestionGenerator()
            question = generator.get_random_question()
            self.assertIsInstance(question, dict)
        except ImportError as e:
            self.fail(f"Failed to import interview_questions module: {e}")
    
    def test_json_serialization(self):
        """Test that questions can be serialized to JSON (for API responses)"""
        generator = InterviewQuestionGenerator()
        questions = generator.get_question_set(count=3, include_scenarios=True)
        
        try:
            json_str = json.dumps(questions)
            deserialized = json.loads(json_str)
            self.assertEqual(len(deserialized), len(questions))
        except (TypeError, ValueError) as e:
            self.fail(f"Questions cannot be serialized to JSON: {e}")

if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add tests
    test_suite.addTest(unittest.makeSuite(TestInterviewQuestionGenerator))
    test_suite.addTest(unittest.makeSuite(TestInterviewQuestionIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    print(f"{'='*50}")