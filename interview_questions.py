#!/usr/bin/env python3
"""
Interview Question Generator for Cybersecurity and Malware Analysis
Provides educational interview questions related to the CEREBUS system's capabilities
"""

import random
import json
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class InterviewQuestionGenerator:
    """
    Generates cybersecurity and malware analysis interview questions
    categorized by difficulty and topic area
    """
    
    def __init__(self):
        self.questions = {
            'malware_analysis': {
                'beginner': [
                    {
                        'question': 'What is the difference between static and dynamic malware analysis?',
                        'answer': 'Static analysis examines malware without executing it, looking at code structure, strings, and metadata. Dynamic analysis involves running malware in a controlled environment to observe its behavior.',
                        'category': 'fundamentals',
                        'difficulty': 'beginner'
                    },
                    {
                        'question': 'What information can you extract from a PE file header?',
                        'answer': 'PE headers contain compilation timestamp, target architecture, number of sections, entry point, imported/exported functions, and file characteristics.',
                        'category': 'pe_analysis',
                        'difficulty': 'beginner'
                    },
                    {
                        'question': 'What is entropy in the context of malware analysis?',
                        'answer': 'Entropy measures the randomness of data in a file. High entropy often indicates encrypted, compressed, or packed malware trying to evade detection.',
                        'category': 'fundamentals',
                        'difficulty': 'beginner'
                    },
                    {
                        'question': 'What are IoCs (Indicators of Compromise)?',
                        'answer': 'IoCs are forensic artifacts that indicate potential intrusion or malicious activity, such as file hashes, IP addresses, domain names, and file paths.',
                        'category': 'fundamentals',
                        'difficulty': 'beginner'
                    },
                    {
                        'question': 'Why is sandboxing important in malware analysis?',
                        'answer': 'Sandboxing provides an isolated environment to safely execute and analyze malware behavior without risking the host system or network.',
                        'category': 'dynamic_analysis',
                        'difficulty': 'beginner'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'Explain the process injection technique and how to detect it.',
                        'answer': 'Process injection involves writing code into another process\'s memory space. Detection includes monitoring APIs like VirtualAllocEx, WriteProcessMemory, and CreateRemoteThread.',
                        'category': 'evasion_techniques',
                        'difficulty': 'intermediate'
                    },
                    {
                        'question': 'What are packers and how do they complicate malware analysis?',
                        'answer': 'Packers compress/encrypt malware to reduce size and evade signature detection. They complicate analysis by hiding the actual malicious code until runtime.',
                        'category': 'evasion_techniques',
                        'difficulty': 'intermediate'
                    },
                    {
                        'question': 'How can you identify if a malware sample is using anti-VM techniques?',
                        'answer': 'Look for VM detection artifacts like specific registry keys, hardware IDs, running processes (VMware tools), timing attacks, or CPUID instruction usage.',
                        'category': 'evasion_techniques',
                        'difficulty': 'intermediate'
                    },
                    {
                        'question': 'What is API hooking and why do malware use it?',
                        'answer': 'API hooking intercepts and modifies system calls. Malware uses it to hide their presence, steal data, or modify system behavior without direct file system changes.',
                        'category': 'advanced_techniques',
                        'difficulty': 'intermediate'
                    },
                    {
                        'question': 'Explain the difference between DLL injection and DLL hijacking.',
                        'answer': 'DLL injection forces a process to load a malicious DLL. DLL hijacking exploits the DLL search order to load malicious DLLs instead of legitimate ones.',
                        'category': 'advanced_techniques',
                        'difficulty': 'intermediate'
                    }
                ],
                'advanced': [
                    {
                        'question': 'How would you analyze a sample using advanced code obfuscation techniques?',
                        'answer': 'Use multiple analysis approaches: entropy analysis, unpacking tools, memory dumps, behavioral analysis, and potentially writing custom unpackers or using automated tools like YARA rules.',
                        'category': 'advanced_analysis',
                        'difficulty': 'advanced'
                    },
                    {
                        'question': 'Explain fileless malware and the challenges in detecting it.',
                        'answer': 'Fileless malware operates in memory without writing files to disk. Detection requires memory analysis, process monitoring, PowerShell logging, and behavioral analysis rather than file-based signatures.',
                        'category': 'advanced_techniques',
                        'difficulty': 'advanced'
                    },
                    {
                        'question': 'How would you develop YARA rules for a new malware family?',
                        'answer': 'Analyze multiple samples, identify unique strings/patterns, determine file offsets, create rules with appropriate conditions, test against known samples and benign files.',
                        'category': 'detection_development',
                        'difficulty': 'advanced'
                    },
                    {
                        'question': 'Describe techniques for analyzing encrypted C2 communications.',
                        'answer': 'Network traffic analysis, SSL/TLS inspection, memory analysis for encryption keys, behavioral pattern analysis, and potentially reverse engineering the encryption algorithm.',
                        'category': 'network_analysis',
                        'difficulty': 'advanced'
                    }
                ]
            },
            'incident_response': {
                'beginner': [
                    {
                        'question': 'What are the key phases of incident response?',
                        'answer': 'Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned (NIST framework).',
                        'category': 'ir_fundamentals',
                        'difficulty': 'beginner'
                    },
                    {
                        'question': 'What should be your first priority when malware is detected on a system?',
                        'answer': 'Containment - isolate the affected system to prevent lateral movement while preserving evidence for analysis.',
                        'category': 'ir_fundamentals',
                        'difficulty': 'beginner'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'How would you investigate a potential data exfiltration incident?',
                        'answer': 'Analyze network logs, examine file access patterns, check for unusual outbound traffic, investigate user account activity, and look for data staging areas.',
                        'category': 'investigation_techniques',
                        'difficulty': 'intermediate'
                    }
                ],
                'advanced': [
                    {
                        'question': 'Describe your approach to investigating an APT attack.',
                        'answer': 'Timeline analysis, IoC development, lateral movement tracking, persistence mechanism identification, attribution analysis, and comprehensive documentation for threat intelligence.',
                        'category': 'advanced_investigation',
                        'difficulty': 'advanced'
                    }
                ]
            },
            'threat_intelligence': {
                'beginner': [
                    {
                        'question': 'What is threat intelligence and why is it important?',
                        'answer': 'Threat intelligence is evidence-based knowledge about threats that helps organizations make informed security decisions and improve their defense posture.',
                        'category': 'ti_fundamentals',
                        'difficulty': 'beginner'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'How do you validate the reliability of threat intelligence?',
                        'answer': 'Verify sources, cross-reference with multiple feeds, check confidence levels, validate against known infrastructure, and track accuracy over time.',
                        'category': 'ti_analysis',
                        'difficulty': 'intermediate'
                    }
                ],
                'advanced': [
                    {
                        'question': 'Explain the diamond model of intrusion analysis.',
                        'answer': 'The diamond model connects adversary, infrastructure, capability, and victim as core features, helping analyze intrusion events and develop countermeasures.',
                        'category': 'ti_frameworks',
                        'difficulty': 'advanced'
                    }
                ]
            },
            'technical_skills': {
                'beginner': [
                    {
                        'question': 'What programming languages are most useful for malware analysis?',
                        'answer': 'Python for automation and analysis, Assembly for low-level understanding, C/C++ for malware development understanding, and PowerShell for Windows-based threats.',
                        'category': 'technical_fundamentals',
                        'difficulty': 'beginner'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'How would you automate the analysis of a large malware sample collection?',
                        'answer': 'Build analysis pipelines using tools like Cuckoo Sandbox, create custom scripts for feature extraction, implement machine learning for classification, and develop reporting systems.',
                        'category': 'automation',
                        'difficulty': 'intermediate'
                    }
                ],
                'advanced': [
                    {
                        'question': 'Explain how machine learning can be applied to malware detection.',
                        'answer': 'Feature extraction from PE files, behavioral analysis, network traffic analysis, ensemble methods, handling adversarial examples, and continuous model retraining.',
                        'category': 'ml_security',
                        'difficulty': 'advanced'
                    }
                ]
            }
        }
        
        # Scenario-based questions
        self.scenarios = [
            {
                'scenario': 'You receive an alert about a suspicious executable file that was downloaded by a user. The file has high entropy and unknown signature. Walk through your analysis process.',
                'expected_approach': [
                    'Isolate the file and system',
                    'Calculate file hashes and check threat intelligence',
                    'Perform static analysis (strings, PE analysis)',
                    'Run dynamic analysis in sandbox',
                    'Analyze network communications',
                    'Document findings and create IoCs'
                ],
                'difficulty': 'intermediate',
                'category': 'practical_analysis'
            },
            {
                'scenario': 'Multiple workstations in your organization show signs of compromise with similar indicators. How do you investigate this potential campaign?',
                'expected_approach': [
                    'Coordinate incident response team',
                    'Collect and preserve evidence from all systems',
                    'Perform timeline analysis across systems',
                    'Identify patient zero and attack vectors',
                    'Track lateral movement patterns',
                    'Develop comprehensive IoCs and countermeasures'
                ],
                'difficulty': 'advanced',
                'category': 'incident_investigation'
            }
        ]
    
    def get_random_question(self, 
                          topic: Optional[str] = None, 
                          difficulty: Optional[str] = None) -> Dict:
        """
        Get a random question optionally filtered by topic and difficulty
        
        Args:
            topic: Topic area (malware_analysis, incident_response, etc.)
            difficulty: Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            Dictionary containing question, answer, and metadata
        """
        available_questions = []
        
        # Collect questions based on filters
        for topic_name, difficulties in self.questions.items():
            if topic and topic != topic_name:
                continue
                
            for diff_name, questions in difficulties.items():
                if difficulty and difficulty != diff_name:
                    continue
                    
                for question in questions:
                    available_questions.append({
                        'topic': topic_name,
                        **question
                    })
        
        if not available_questions:
            return self._get_fallback_question()
            
        return random.choice(available_questions)
    
    def get_question_set(self, 
                        count: int = 5, 
                        topic: Optional[str] = None,
                        difficulty: Optional[str] = None,
                        include_scenarios: bool = False) -> List[Dict]:
        """
        Get a set of questions for an interview session
        
        Args:
            count: Number of questions to return
            topic: Topic filter
            difficulty: Difficulty filter
            include_scenarios: Whether to include scenario-based questions
            
        Returns:
            List of question dictionaries
        """
        questions = []
        used_questions = set()
        
        # Get regular questions
        max_attempts = count * 3  # Prevent infinite loops
        attempts = 0
        
        while len(questions) < count and attempts < max_attempts:
            question = self.get_random_question(topic, difficulty)
            question_key = question.get('question', '')
            
            if question_key not in used_questions:
                questions.append(question)
                used_questions.add(question_key)
            
            attempts += 1
        
        # Add scenarios if requested
        if include_scenarios and len(questions) < count:
            filtered_scenarios = self.scenarios
            if difficulty:
                filtered_scenarios = [s for s in self.scenarios if s['difficulty'] == difficulty]
            
            for scenario in random.sample(filtered_scenarios, 
                                        min(len(filtered_scenarios), count - len(questions))):
                questions.append({
                    'type': 'scenario',
                    'question': scenario['scenario'],
                    'expected_approach': scenario['expected_approach'],
                    'difficulty': scenario['difficulty'],
                    'category': scenario['category'],
                    'topic': 'practical_analysis'
                })
        
        return questions
    
    def get_available_topics(self) -> List[str]:
        """Get list of available topics"""
        return list(self.questions.keys())
    
    def get_available_difficulties(self) -> List[str]:
        """Get list of available difficulty levels"""
        return ['beginner', 'intermediate', 'advanced']
    
    def get_topic_stats(self) -> Dict[str, Dict[str, int]]:
        """Get statistics about questions per topic and difficulty"""
        stats = {}
        
        for topic, difficulties in self.questions.items():
            stats[topic] = {}
            total = 0
            
            for difficulty, questions in difficulties.items():
                count = len(questions)
                stats[topic][difficulty] = count
                total += count
            
            stats[topic]['total'] = total
        
        return stats
    
    def _get_fallback_question(self) -> Dict:
        """Return a fallback question when no matches found"""
        return {
            'question': 'Describe the key components of a comprehensive malware analysis framework.',
            'answer': 'A comprehensive framework should include static analysis tools, dynamic analysis environment, threat intelligence integration, automated analysis pipelines, reporting systems, and continuous learning capabilities.',
            'category': 'fundamentals',
            'difficulty': 'intermediate',
            'topic': 'malware_analysis'
        }
    
    def export_questions(self, filepath: str) -> bool:
        """
        Export all questions to a JSON file
        
        Args:
            filepath: Path to save the JSON file
            
        Returns:
            Success status
        """
        try:
            export_data = {
                'questions': self.questions,
                'scenarios': self.scenarios,
                'metadata': {
                    'total_questions': sum(len(q) for topic in self.questions.values() 
                                         for q in topic.values()),
                    'total_scenarios': len(self.scenarios),
                    'topics': self.get_available_topics(),
                    'difficulties': self.get_available_difficulties()
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Questions exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting questions: {e}")
            return False
    
    def import_questions(self, filepath: str) -> bool:
        """
        Import questions from a JSON file
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Success status
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'questions' in data:
                # Merge with existing questions
                for topic, difficulties in data['questions'].items():
                    if topic not in self.questions:
                        self.questions[topic] = {}
                    
                    for difficulty, questions in difficulties.items():
                        if difficulty not in self.questions[topic]:
                            self.questions[topic][difficulty] = []
                        
                        self.questions[topic][difficulty].extend(questions)
            
            if 'scenarios' in data:
                self.scenarios.extend(data['scenarios'])
            
            logger.info(f"Questions imported from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing questions: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize the generator
    generator = InterviewQuestionGenerator()
    
    # Test basic functionality
    print("=== Cybersecurity Interview Question Generator ===\n")
    
    # Get a random question
    print("Random Question:")
    question = generator.get_random_question()
    print(f"Q: {question['question']}")
    print(f"A: {question['answer']}")
    print(f"Topic: {question['topic']} | Difficulty: {question['difficulty']}\n")
    
    # Get a question set for malware analysis
    print("Malware Analysis Question Set:")
    questions = generator.get_question_set(count=3, topic='malware_analysis', include_scenarios=True)
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q['question']}")
        if q.get('type') == 'scenario':
            print(f"   Expected approach: {', '.join(q['expected_approach'][:3])}...")
        print()
    
    # Show statistics
    print("Question Statistics:")
    stats = generator.get_topic_stats()
    for topic, counts in stats.items():
        print(f"{topic}: {counts}")