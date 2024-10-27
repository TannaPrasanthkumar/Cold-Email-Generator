# Cold Mail Generator 📧

A Streamlit-based application that automatically generates personalized cold emails for job applications by analyzing job postings and matching them with your portfolio.

## 🌟 Features

- **Automated Job Analysis**: Extracts key information from job postings using LLM
- **Portfolio Matching**: Matches your skills and projects with job requirements
- **Email Generation**: Creates professional, personalized cold emails
- **Interactive UI**: User-friendly interface with real-time progress tracking
- **Multi-format Output**: Copy or download generated emails

## 🛠️ Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- A Groq API key
- ChromaDB installed and configured
- Your portfolio data in CSV format
- pip (Python package installer)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/tannaprasanthkumar/cold-mail-generator.git
cd cold-mail-generator
```

2. Set up Python Virtual Environment:

On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Deactivate when you're done
deactivate
```

On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Deactivate when you're done
deactivate
```

3. Install required packages:
```bash
# Make sure your virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

## 📄 Requirements.txt

Create a `requirements.txt` file with these dependencies:
```txt
streamlit==1.31.0
langchain-groq==0.0.6
chromadb==0.4.22
pandas==2.2.0
python-dotenv==1.0.0
langchain-core==0.1.27
langchain-community==0.0.24
```

## 📄 Configuration

1. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

2. Prepare your portfolio data:
   - Create a CSV file named `portfolio.csv`
   - Required columns:
     - `Techstack`: List of technologies/skills
     - `Links`: URLs to relevant projects/work

## 🚀 Usage

1. Ensure your virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. Start the application:
```bash
streamlit run app.py
```

3. Access the web interface at `http://localhost:8501`

4. Enter a job posting URL and click "Generate Email"

## 📂 Project Structure

```
cold-mail-generator/
├── venv/              # Virtual environment directory
├── app.py             # Main Streamlit application
├── model.py           # LLM integration and prompt templates
├── portfolio.py       # Portfolio management and matching
├── utils.py           # Utility functions
├── portfolio.csv      # Your portfolio data
├── requirements.txt   # Project dependencies
├── .env              # Environment variables
└── README.md         # Project documentation
```

## 🗃️ Portfolio Format

Your `portfolio.csv` should follow this format:

```csv
Techstack,Links
"Python, Django, REST API","https://github.com/your-project1, https://github.com/your-project2"
"React, Node.js, MongoDB","https://github.com/your-project3"
```

## ⚙️ Components

- **Model Class**: Handles interaction with the Groq LLM for job analysis and email generation
- **Portfolio Class**: Manages portfolio data and skill matching using ChromaDB
- **Streamlit App**: Provides the user interface and orchestrates the workflow

## 📋 Development Environment Tips

1. **Managing Virtual Environment**:
   ```bash
   # Update pip in virtual environment
   python -m pip install --upgrade pip

   # Install a new package
   pip install package_name

   # Save current dependencies
   pip freeze > requirements.txt

   # Install from requirements.txt
   pip install -r requirements.txt
   ```

2. **Virtual Environment Best Practices**:
   - Always activate the virtual environment before running the app
   - Keep `requirements.txt` updated when adding new packages
   - Don't commit the `venv` folder to version control
   - Add `venv/` to your `.gitignore` file

3. **Common Virtual Environment Issues**:
   ```bash
   # If venv is corrupted, delete and recreate:
   deactivate
   rm -rf venv/  # On Windows: rmdir /s /q venv
   python -m venv venv
   ```

## 🔒 API Key Security

- Never commit your `.env` file to version control
- Keep your Groq API key confidential
- Use environment variables for sensitive data
- Add `.env` to your `.gitignore` file

## 🐛 Troubleshooting

Common issues and solutions:

1. **Virtual Environment Issues**
   - Error: "pip not found" or "streamlit not found"
     - Solution: Ensure virtual environment is activated
   - Error: "No module named 'package_name'"
     - Solution: Install missing package with `pip install package_name`

2. **ChromaDB Connection Error**
   - Ensure ChromaDB is properly installed
   - Check if the `chroma_store` directory exists and has proper permissions

3. **API Key Error**
   - Verify your Groq API key is correctly set in `.env`
   - Check if the `.env` file is in the correct location

4. **Portfolio Loading Error**
   - Ensure `portfolio.csv` exists and has the correct format
   - Check for proper CSV formatting and required columns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contact

For support or questions, contact:
- Email: your.email@example.com
- GitHub: [TannaPrasanthkumar](https://github.com/tannaprasanthkumar)

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for their LLM API
- [Streamlit](https://streamlit.io/) for the web framework
- [LangChain](https://www.langchain.com/) for LLM integration
- [ChromaDB](https://www.trychroma.com/) for vector storage