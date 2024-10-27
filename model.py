from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import os

load_dotenv()

class Model:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv('GROQ_API_KEY'),
            model_name="llama-3.1-70b-versatile"
        )
    
    def extract_jobs(self, cleaned_text):
        prompt_template = ChatPromptTemplate.from_template(
            """
            ### Context:
            You are analyzing job postings from a company's career page. The following text contains job listing information that needs to be structured.

            ### Source Data:
            {page_data}

            ### Task:
            Extract all job postings from the provided text and structure them according to the specified format.

            ### Requirements:
            1. Extract each complete job posting
            2. For each posting, identify and structure the following information:
            - Role/Position title
            - Required years of experience (if specified)
            - Required skills and qualifications
            - Full job description
            
            ### Output Format:
            Return a JSON array where each object represents a job posting with the following schema:
            {{
                "role": string,                    // Job title/position name
                "experience": string | null,       // Required experience (null if not specified)
                "skills": string[],               // Array of required skills
                "description": string             // Complete job description
            }}

            ### Rules:
            - Maintain the exact structure specified in the schema
            - Include all identified job postings
            - Use null for missing required experience
            - Convert skills into an array format
            - Preserve the original text in descriptions
            - Return only valid JSON without any additional text or explanations

            ### JSON Output:
            """
        )
        
        chain = prompt_template | self.llm
        response = chain.invoke({"page_data": cleaned_text})
        
        try:
            parser = JsonOutputParser()
            output = parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        
        return output if isinstance(output, list) else [output]
    
    def write_mail(self, job, links):
        # Process links to extract just the URLs into a comma-separated string
        processed_links = ", ".join([link.get("links", "") for link in links]) if links else "No relevant projects available"
        
        prompt_email = ChatPromptTemplate.from_template(
            """
            ### JOB POSTING DETAILS:
            {job_description}

            ### CONTEXT:
            You are Prasanth Kumar, a final year B.Tech Computer Science and Engineering student at [University Name]. 
            You are passionate about technology and software development, with strong academic performance 
            and practical experience through projects and internships.

            ### BACKGROUND:
            - Currently pursuing B.Tech in Computer Science and Engineering
            - Strong foundation in programming languages and software development
            - Completed relevant coursework in [specific areas matching job requirements]
            - Active participation in technical clubs and hackathons
            - Experience with academic projects and internships

            ### INSTRUCTION:
            Write a professional job application email to the HR department for the position described above. The email should:
            1. Begin with a proper formal greeting
            2. Express genuine interest in the position
            3. Highlight relevant academic achievements and technical skills
            4. Mention any relevant projects or internships: {link_list}
            5. Demonstrate knowledge about the company and why you're a good fit
            6. Include your eagerness to learn and contribute
            7. Request for an opportunity to interview
            8. End with a professional closing

            ### TONE AND STYLE:
            - Professional yet enthusiastic
            - Confident but not arrogant
            - Show genuine interest and motivation
            - Maintain formal email etiquette
            - Keep paragraphs concise and focused
            - Highlight your potential as a fresh graduate

            Note: Do not use curly braces in the email content. Use parentheses or square brackets if needed.

            ### EMAIL (NO PREAMBLE):
            """
        )
        
        chain_email = prompt_email | self.llm
        
        response = chain_email.invoke({
            "job_description": str(job),
            "link_list": processed_links
        })
        
        # Escape any remaining curly braces in the response
        return response.content.replace("{", "{{").replace("}", "}}")