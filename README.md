# Chatbot
Follow the steps below to set up and run the project:

Step 1: Create a Conda Environment

Open the Anaconda Prompt.
Run the following command to create a new Conda environment:

conda create --name <env_name> python=3.x

Activate the environment:
conda activate <env_name>

Step 2: Install Dependencies

Run the following commands to install the required packages:

pip install langchain
pip install pinecone-client
pip install langchain_cohere
pip install huggingface-hub
pip install ctransformers==0.2.5
pip install sentence-transformers==2.2.2
pip install flask
pip install streamlit
pip install faiss

Step 3: Configure API Keys

Collect API keys for Pinecone and Cohere LLM.
Paste the API keys in the appropriate places in your project files.

Step 4: Open Anaconda Prompt
Open the Anaconda Prompt on your system.

Step 5: Navigate to the Project Directory

Activate the created environment:
conda activate <env_name>

Navigate to your project folder by pasting the path:
cd <path_to_project>

Step 6: Run the Project
Run the following command to start the application:
python app.py
