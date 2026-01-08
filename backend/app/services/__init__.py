import google.generativeai as genai
from app.config import get_settings
from typing import List, Dict
import json

settings = get_settings()


class LLMService:
    """Google Gemini LLM Service for generating interview questions"""

    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    def generate_interview_questions(
        self, resume_content: str, job_description: str
    ) -> List[Dict[str, str]]:
        """
        Generate 10-15 interview questions based on resume and job description
        """
        prompt = f"""You are an expert technical interviewer. Based on the following resume and job description,
generate 10-15 relevant interview questions along with reference answers.

Resume:
{resume_content}

Job Description:
{job_description}

Please provide the output as a JSON array with objects containing 'question' and 'answer' keys.
The questions should cover:
1. Technical skills mentioned in the resume
2. Experience related to the job requirements
3. Behavioral questions relevant to the role
4. Scenario-based questions matching the job description

Format your response ONLY as a valid JSON array, nothing else. Do not include any markdown code blocks or explanations.
Just return the raw JSON array.

Example format:
[
  {{"question": "Tell me about...", "answer": "A good answer would..."}},
  {{"question": "Describe your experience with...", "answer": "The candidate should..."}}
]
"""

        try:
            # Generate content with Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )

            # Extract text from response
            response_text = response.text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            # Parse JSON
            result = json.loads(response_text)

            # Handle different response formats
            if isinstance(result, dict):
                if "questions" in result:
                    return result["questions"]
                elif "questions_answers" in result:
                    return result["questions_answers"]
                else:
                    return list(result.values())[0] if result else []
            elif isinstance(result, list):
                return result

            return []

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from Gemini response: {str(e)}")
            print(f"Response was: {response_text[:200]}...")
            return []
        except Exception as e:
            print(f"Error generating questions with Gemini: {str(e)}")
            return []


def get_llm_service():
    """Get the LLM service instance"""
    return LLMService()
