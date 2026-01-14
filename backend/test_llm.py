#!/usr/bin/env python3
"""
Test script to verify Google Gemini LLM service is working
"""
import sys
import os

# Add the app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app.services import LLMService
from app.config import get_settings
import json

def test_llm_service():
    """Test the LLM service with sample resume and job description"""

    print("=" * 60)
    print("Testing Google Gemini LLM Service")
    print("=" * 60)

    # Check API key
    settings = get_settings()
    print(f"\n✓ Gemini API Key: {'*' * 20}{settings.gemini_api_key[-8:]}")
    print(f"✓ Gemini Model: {settings.gemini_model}")

    # Sample data
    sample_resume = """
    John Doe
    Senior Software Engineer

    EXPERIENCE:
    - 5 years of Python development
    - Expertise in FastAPI and Django frameworks
    - Experience with PostgreSQL and MongoDB
    - Built microservices architecture using Docker and Kubernetes
    - Strong background in AWS cloud services

    SKILLS:
    - Python, JavaScript, TypeScript
    - React, Node.js
    - PostgreSQL, Redis
    - Docker, Kubernetes, AWS
    - REST APIs, GraphQL
    """

    sample_job_description = """
    We are looking for a Senior Backend Engineer with strong Python skills.

    Requirements:
    - 5+ years of Python experience
    - Experience with FastAPI or Django
    - Knowledge of PostgreSQL
    - Experience with cloud platforms (AWS/GCP)
    - Strong API design skills
    - Experience with microservices architecture
    """

    print("\n" + "=" * 60)
    print("Sample Resume:")
    print("=" * 60)
    print(sample_resume[:200] + "...")

    print("\n" + "=" * 60)
    print("Sample Job Description:")
    print("=" * 60)
    print(sample_job_description[:200] + "...")

    # Initialize LLM service
    print("\n" + "=" * 60)
    print("Initializing LLM Service...")
    print("=" * 60)

    try:
        llm_service = LLMService()
        print("✓ LLM Service initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize LLM Service: {str(e)}")
        return False

    # Generate questions
    print("\n" + "=" * 60)
    print("Generating Interview Questions...")
    print("=" * 60)
    print("⏳ This may take 10-30 seconds...\n")

    try:
        questions = llm_service.generate_interview_questions(
            sample_resume,
            sample_job_description
        )

        if not questions:
            print("✗ No questions generated")
            return False

        print(f"✓ Generated {len(questions)} questions!\n")

        # Display questions
        print("=" * 60)
        print("Generated Questions:")
        print("=" * 60)

        for i, qa in enumerate(questions, 1):
            print(f"\n{i}. QUESTION:")
            print(f"   {qa.get('question', 'N/A')}")
            print(f"\n   REFERENCE ANSWER:")
            answer = qa.get('answer', 'N/A')
            # Truncate long answers
            if len(answer) > 150:
                answer = answer[:150] + "..."
            print(f"   {answer}")
            print("-" * 60)

        # Show full JSON structure
        print("\n" + "=" * 60)
        print("JSON Structure (first question):")
        print("=" * 60)
        print(json.dumps(questions[0], indent=2))

        print("\n" + "=" * 60)
        print("✓ LLM Service Test PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"✗ Error generating questions: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_llm_service()
    sys.exit(0 if success else 1)
