all the attached diagrams considered as conceptual diagrams for our project, .....

# Requirements, Risks, Assumptions, & Constraints

## Requirements

### Business Requirements
* Provide AI-powered Spanish language learning assistance for students, teachers, and self-learners.
* Ensure the AI supports different learning levels (beginner, intermediate, advanced).
* Offer interactive learning experiences, including conversational AI, grammar correction, speak to learn, and vocabulary expansion.
* Ensure alignment with Spanish language curricula (Common European Framework of Reference - CEFR).

### Functional Requirements
* Cloud based solution utilising managed serveices and serverless where possible, the reasons is the company is small and no team to manage the infrastructure, also the owner looking to utilise scalability offered by serverless on cloud. of-course the budget is one of the limitations on this project (no CapEx)
* Conversational AI Tutor: Engage users in real-time Spanish conversations to improve fluency.
* Grammar & Spell Checker: AI should correct grammar mistakes and explain errors to learners.
* Pronunciation Feedback: Provide AI-powered speech recognition for pronunciation assessment.
* Reading Comprehension Aid: Summarize Spanish texts and explain difficult words/phrases.
* Adaptive Learning: AI should adjust difficulty levels based on user progress. (not sure if easy to be done, will try)
* Multimodal Support: Accept text and voice inputs, and provide text, audio, and image-based responses.

### Non-functional Requirements
* Performance: Response time < 7 seconds for text-based queries, < 10 seconds for voice-based analysis.
* Scalability: Must support hunderds of users, especially in peak learning hours.
* Usability: Intuitive UI/UX for students, parents, and educators.
* Content Filtering: Ensure AI-generated responses are safe, culturally appropriate, and educationally relevant.

### Tooling
* Gen AI models will be used for content creation, spelling checks, etc
* ML algorithims can be used for voice-text converting (if required), (maybe OCR for writing and spelling check)

### Risks
* AI Accuracy Issues: The model may generate incorrect grammar explanations or misleading answers.
* Bias in Language Learning: AI may favor one Spanish dialect over others (e.g., Castilian vs. Latin American Spanish).
* Data Privacy Concerns: AI interactions must be anonymized and secured, especially for minors.
* Teacher Resistance: Educators may be hesitant to adopt AI-powered learning tools.

### Assumptions
* Students and teachers will actively use AI for Spanish language learning.
* Internet access is available for most users, but offline mode may be required in some regions.
* Schools and universities will integrate AI learning tools into their curricula.

### Constraints
* Budget: Limited funding for model fine-tuning and infrastructure.
* Infrastructure: Choice of cloud provider (AWS, GCP, Azure) affects cost and performance.
* Latency: AI-generated responses must be fast for an effective learning experience.
* AI model controls: we want to make sure that the responces is related to the selected languge, avoide users to exploitation of the model for out of context questions.

## Data Strategy

### Data Sources
Public Spanish Datasets: Wikipedia (Spanish), Common Crawl, OpenSubtitles, CC100-ES, and Spanish news articles.

### Privacy Measures
* Anonymization: Remove personally identifiable information (PII) from datasets.
* Data Minimization: Collect only necessary user data for personalization.
* Encryption:
    *  At Rest: AES-256 encryption for stored user data.
    * In Transit: TLS 1.2/1.3 for securing API communication.
* Access Controls: Role-based access for teachers, students, and administrators. (will be added in the future)

## Model Selection and Development

* Will use SaaS AI model accessed via API (most likely Chatgpt or Anthropic Claude)
* The input will be text and output text
* Most of AI models supports Spanish language, based on testing will check if multiple models required.
* We do not think there will be Fine-tuning for the model
* will use open-source tools for model evaluation such as Ragas