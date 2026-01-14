"""
Mock data for testing
"""
from typing import List, Dict

# Mock resume content
MOCK_RESUME_CONTENT = """
JOHN DOE
Senior Software Engineer
Email: john.doe@example.com | Phone: (555) 123-4567

PROFESSIONAL SUMMARY
Results-driven Senior Software Engineer with 7+ years of experience in full-stack development,
specializing in Python, FastAPI, React, and cloud technologies. Proven track record of delivering
scalable applications and leading development teams.

TECHNICAL SKILLS
- Backend: Python, FastAPI, Django, Flask, Node.js
- Frontend: React, TypeScript, JavaScript, HTML5, CSS3
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Cloud: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes
- Tools: Git, CI/CD, Jenkins, GitHub Actions

PROFESSIONAL EXPERIENCE

Senior Software Engineer | Tech Corp Inc. | 2020 - Present
- Led development of microservices architecture using FastAPI and PostgreSQL
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored junior developers and conducted code reviews
- Designed and built RESTful APIs serving 1M+ requests daily

Software Engineer | StartupXYZ | 2018 - 2020
- Developed full-stack web applications using React and Django
- Optimized database queries improving application performance by 40%
- Collaborated with cross-functional teams in Agile environment

Junior Developer | DevShop | 2016 - 2018
- Built responsive web interfaces using React and modern CSS
- Participated in daily standups and sprint planning
- Fixed bugs and implemented new features based on user feedback

EDUCATION
Bachelor of Science in Computer Science
State University | 2012 - 2016

CERTIFICATIONS
- AWS Certified Solutions Architect
- Python Professional Certification
"""

# Mock job descriptions
MOCK_JOB_DESCRIPTION_BACKEND = """
Senior Backend Engineer

We are looking for an experienced Senior Backend Engineer to join our growing team.

Requirements:
- 5+ years of experience in backend development
- Strong proficiency in Python and FastAPI or Django
- Experience with PostgreSQL and database optimization
- Knowledge of Docker and containerization
- Experience with AWS or other cloud platforms
- Strong understanding of RESTful API design
- Experience with microservices architecture
- Excellent problem-solving skills

Responsibilities:
- Design and implement scalable backend services
- Write clean, maintainable code with proper testing
- Collaborate with frontend developers and designers
- Optimize application performance and database queries
- Participate in code reviews and technical discussions
- Mentor junior team members

Nice to have:
- Experience with React or other frontend frameworks
- Knowledge of Redis and caching strategies
- Experience with CI/CD pipelines
- Familiarity with GraphQL
"""

MOCK_JOB_DESCRIPTION_FULLSTACK = """
Full Stack Developer

Join our team as a Full Stack Developer working on cutting-edge web applications.

Requirements:
- 3+ years of full-stack development experience
- Proficiency in React and modern JavaScript
- Backend experience with Python (FastAPI/Django) or Node.js
- Experience with PostgreSQL or MySQL
- Understanding of RESTful APIs
- Git version control

Responsibilities:
- Build responsive user interfaces with React
- Develop and maintain backend APIs
- Write unit and integration tests
- Deploy applications to cloud platforms
- Work in Agile environment with cross-functional teams

Nice to have:
- TypeScript experience
- AWS or cloud platform knowledge
- Docker experience
- UI/UX design skills
"""

# Mock LLM responses
MOCK_INTERVIEW_QUESTIONS: List[Dict[str, str]] = [
    {
        "question": "Can you describe your experience with FastAPI and how you've used it in production?",
        "answer": "A strong candidate should discuss specific projects where they used FastAPI, mention its async capabilities, type hints, automatic API documentation, and performance benefits. They should be able to explain dependency injection, middleware, and how they structured their applications."
    },
    {
        "question": "How do you handle database optimization in PostgreSQL?",
        "answer": "The candidate should mention indexing strategies, query optimization using EXPLAIN ANALYZE, connection pooling, avoiding N+1 queries, using CTEs and window functions appropriately, and monitoring query performance. They might also discuss denormalization strategies when necessary."
    },
    {
        "question": "Describe your approach to implementing microservices architecture.",
        "answer": "Look for understanding of service boundaries, inter-service communication (REST, gRPC, message queues), API gateways, service discovery, distributed tracing, handling eventual consistency, circuit breakers, and deployment strategies. They should mention real examples from their experience."
    },
    {
        "question": "Tell me about a time when you had to optimize an application's performance. What was your approach?",
        "answer": "The candidate should describe a specific situation, the performance issues they identified, the profiling tools they used, the optimizations they implemented (code-level, database, caching, etc.), and the measurable results achieved. This tests both technical skills and problem-solving ability."
    },
    {
        "question": "How do you approach mentoring junior developers?",
        "answer": "Look for practical examples of code reviews, pair programming, knowledge sharing sessions, setting clear expectations, providing constructive feedback, and helping juniors grow their skills. This assesses leadership and communication abilities."
    },
    {
        "question": "Explain how you would design a RESTful API for a social media platform.",
        "answer": "The candidate should discuss resource identification, HTTP methods, status codes, versioning strategies, authentication/authorization, pagination, rate limiting, error handling, and API documentation. They should demonstrate understanding of REST principles."
    },
    {
        "question": "What's your experience with Docker and containerization?",
        "answer": "Should cover Docker basics, writing Dockerfiles, multi-stage builds, docker-compose for local development, container orchestration basics, security best practices, and how they've used containers in their projects."
    },
    {
        "question": "How do you ensure code quality in your projects?",
        "answer": "Look for mentions of code reviews, linting, type checking, unit tests, integration tests, CI/CD pipelines, code coverage tools, following style guides, and maintaining documentation. Real examples strengthen the answer."
    },
    {
        "question": "Describe a challenging technical problem you solved recently.",
        "answer": "The candidate should clearly articulate the problem, the constraints they faced, their analysis process, the solution they implemented, alternatives they considered, and the outcome. This tests problem-solving skills and technical depth."
    },
    {
        "question": "How do you stay updated with new technologies and best practices?",
        "answer": "Good answers include reading technical blogs, attending conferences/meetups, contributing to open source, personal projects, online courses, podcasts, and participating in developer communities. Shows commitment to continuous learning."
    },
    {
        "question": "What's your experience with AWS services?",
        "answer": "The candidate should discuss specific AWS services they've used (EC2, S3, Lambda, RDS, etc.), how they architected solutions, cost optimization strategies, security considerations, and real project examples. Certification is a plus but practical experience is key."
    },
    {
        "question": "How do you handle errors and exceptions in your applications?",
        "answer": "Should cover try-catch blocks, custom exception classes, logging strategies, error monitoring tools, user-friendly error messages, retry mechanisms, circuit breakers, and how they debug production issues."
    },
    {
        "question": "Describe your experience working in an Agile environment.",
        "answer": "Look for understanding of Agile principles, experience with sprints, standups, retrospectives, sprint planning, user stories, estimation, and collaboration with cross-functional teams. Real examples of how Agile improved their workflow are valuable."
    },
    {
        "question": "How would you implement authentication and authorization in a FastAPI application?",
        "answer": "Should discuss JWT tokens, OAuth2, password hashing (bcrypt), dependency injection for auth, protecting routes, role-based access control, refresh tokens, and security best practices. Code examples or library mentions (like python-jose, passlib) strengthen the answer."
    },
    {
        "question": "What's your approach to writing tests for backend applications?",
        "answer": "The candidate should cover unit tests, integration tests, test fixtures, mocking external dependencies, test coverage, TDD practices, using pytest or unittest, testing async code, and CI integration. Real examples of how testing caught bugs early are valuable."
    }
]

# Mock file content (base64 encoded)
MOCK_PDF_CONTENT = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 4 0 R
>>
>>
/MediaBox [0 0 612 792]
/Contents 5 0 R
>>
endobj
4 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj
5 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test Resume) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000274 00000 n
0000000361 00000 n
trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
456
%%EOF
"""

# Mock user data
MOCK_USERS = [
    {
        "email": "john@example.com",
        "username": "johndoe",
        "full_name": "John Doe",
        "password": "SecurePass123!"
    },
    {
        "email": "jane@example.com",
        "username": "janesmith",
        "full_name": "Jane Smith",
        "password": "AnotherPass456!"
    }
]

# Mock session data
MOCK_SESSION_DATA = {
    "job_description": MOCK_JOB_DESCRIPTION_BACKEND,
    "resume_content": MOCK_RESUME_CONTENT,
    "resume_filename": "john_doe_resume.pdf"
}

# Mock answer submission
MOCK_USER_ANSWERS = [
    {
        "question_id": 1,
        "answer": "I have extensive experience with FastAPI, having used it in production for the last 3 years. At Tech Corp, I built microservices handling 1M+ requests daily. I particularly appreciate its async capabilities, automatic OpenAPI documentation, and the type hints system which catches errors early.",
        "expected_score": 9.0
    },
    {
        "question_id": 2,
        "answer": "For PostgreSQL optimization, I focus on proper indexing, using EXPLAIN ANALYZE to identify slow queries, implementing connection pooling, and avoiding N+1 queries through eager loading. I also monitor query performance and use caching for frequently accessed data.",
        "expected_score": 8.5
    },
    {
        "question_id": 3,
        "answer": "I've implemented microservices using FastAPI with service-to-service communication via REST APIs and message queues. I ensure proper service boundaries, use API gateways for routing, implement circuit breakers for resilience, and use Docker for consistent deployments.",
        "expected_score": 8.0
    }
]
