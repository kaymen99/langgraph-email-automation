<!--
Title: Customer Support Email Automation System | Langchain/Langgraph Integration
Description: Automate customer support emails with our system built using Langchain/Langgraph. Features include email categorization, query synthesis, draft email creation, and email verification.
Keywords: Customer support automation, email automation, Langchain, Langgraph, AI email agents, Gmail API, Python email automation, email categorization, email verification, AI agents, AI tools
Author: kaymen99
-->

# Customer Support Email Automation with AI Agents and RAG

**A Langgraph system for streamlining client interactions, ensuring every customer receives a quick and accurate response. 🌟**

## Introduction

In today's fast-paced environment, customers demand quick, accurate, and personalized responses—expectations that can overwhelm traditional support teams. Managing large volumes of emails, categorizing them, crafting appropriate replies, and ensuring quality consumes significant time and resources, often leading to delays or errors, which can harm customer satisfaction.

**Customer Support Email Automation** is an AI solution designed to enhance customer communication for businesses. Leveraging a Langgraph-driven workflow, multiple AI agents collaborate to efficiently manage, categorize, and respond to customer emails. The system also implements RAG (Retrieval-Augmented Generation) technology to deliver accurate responses to any business or product-related questions.

## Features

### Email Inbox Management with AI Agents

- Continuously monitors the agency's Gmail inbox
- Categorizes emails into 'customer complaint,' 'product inquiry,' 'customer feedback,' or 'unrelated'
- Automatically handles irrelevant emails to maintain efficiency

### AI Response Generation

- Quickly drafts emails for customer complaints and feedback using Langgraph
- Utilizes RAG techniques to answer product/service related questions accurately
- Creates personalized email content tailored to each customer's needs

### Quality Assurance with AI

- Automatically checks email quality, formatting, and relevance
- Ensures every response meets high standards before reaching the client

## How It Works

1. **Email Monitoring**: The system constantly checks for new emails in the agency's Gmail inbox using the Gmail API.
2. **Email Categorization**: AI agents sort each email into predefined categories.
3. **Response Generation**: 
   - For complaints or feedback: The system quickly drafts a tailored email response.
   - For service/product questions: The system uses RAG to retrieve accurate information from agency documents and generates a response.
4. **Quality Assurance**: Each draft email undergoes AI quality and formatting checks.
5. **Sending**: Approved emails are sent to the client promptly, ensuring timely communication.

## System Flowchart

This is the detailed flow of the system:

[![](https://mermaid.ink/img/pako:eNqllEuP2jAQx7-KZa6AgAB5HFrxFlJBXbarIsIeTDwBi2CntrPAEr57TRIoW_Wwojk585_fvJLxCQeCAvZwGIl9sCFSox_9JUfm6fgTwZkWEo0mnfE3NOYrcXgtNFSpfEHd01jlZjTYxfr49Zyr3YuaTgWawt4ohEUqRQt_wCn6LkUASr3eOw5FYpQXTrjagwR6Q3p-j2hYC8neITcWXC_jXriEyDjQFHXv7b1EabEDiXpiF0eEcY1ME0MAuiLBNkV9_6dk2uidNXD9IaQpjyaBRgP-K2HymKKB_3zkegPqUsJTApKBQqEJN-uMCnKQzWLuj0CjTtYCCqXY3XnMM49_pu1n0tA3iUU4A0L_0odZWZ04luINUjTyn4HTD7PIPaamO4Vm8MYUE9z0mIujQjzonMkmlUtKHyMwHzJkUeSVQjcsKy3FFryS4zjFubJnVG-8RnwoByIS0ivVarV7vFvgq9Uf3LKsz-K9a_bV6hG8f80ePoQP_i_78DY69xF8VOBu-BA-v2Z_DF8UOKX08zguY7NW5j-i5sI4XcItsdmNHSyxZ46UyO0SL_nZ-JFEC7M5Afa0TKCMpUjWG-yFJFLmLYmp2ds-I2tJdjdrTDj2TviAvUbLrjYtt2G1XLdVr7XtZhkfjbnqNJyW4zZt17LdpuO0z2X8LoQJUau6rbbt2la7btmWW6s3s3iLTMxLAHq5zCb5dRcIHrI1Pv8GXQeX4g?type=png)](https://mermaid.live/edit#pako:eNqllEuP2jAQx7-KZa6AgAB5HFrxFlJBXbarIsIeTDwBi2CntrPAEr57TRIoW_Wwojk585_fvJLxCQeCAvZwGIl9sCFSox_9JUfm6fgTwZkWEo0mnfE3NOYrcXgtNFSpfEHd01jlZjTYxfr49Zyr3YuaTgWawt4ohEUqRQt_wCn6LkUASr3eOw5FYpQXTrjagwR6Q3p-j2hYC8neITcWXC_jXriEyDjQFHXv7b1EabEDiXpiF0eEcY1ME0MAuiLBNkV9_6dk2uidNXD9IaQpjyaBRgP-K2HymKKB_3zkegPqUsJTApKBQqEJN-uMCnKQzWLuj0CjTtYCCqXY3XnMM49_pu1n0tA3iUU4A0L_0odZWZ04luINUjTyn4HTD7PIPaamO4Vm8MYUE9z0mIujQjzonMkmlUtKHyMwHzJkUeSVQjcsKy3FFryS4zjFubJnVG-8RnwoByIS0ivVarV7vFvgq9Uf3LKsz-K9a_bV6hG8f80ePoQP_i_78DY69xF8VOBu-BA-v2Z_DF8UOKX08zguY7NW5j-i5sI4XcItsdmNHSyxZ46UyO0SL_nZ-JFEC7M5Afa0TKCMpUjWG-yFJFLmLYmp2ds-I2tJdjdrTDj2TviAvUbLrjYtt2G1XLdVr7XtZhkfjbnqNJyW4zZt17LdpuO0z2X8LoQJUau6rbbt2la7btmWW6s3s3iLTMxLAHq5zCb5dRcIHrI1Pv8GXQeX4g)

## Tech Stack

* Langchain & Langgraph: for developing AI agents workflow.
* Langserve: simplify API development & deployment (using FastAPI).
* Groq and Gemini APIs: for LLMs access.
* Google Gmail API

## How to Run

### Prerequisites

- Python 3.7+
- Groq api key
- Google Gemini api key (for embeddings)
- Gmail API credentials
- Necessary Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kaymen99/langgraph-email-automation.git
   cd langgraph-email-automation
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add your GMAIL address, we are using the Groq llama-3.1-70b model and the Google gemini embedding model so you must also get API keys to access them:

   ```env
   MY_EMAIL=your_email@gmail.com
   GROQ_API_KEY=your_groq_api_key
   GOOGLE_API_KEY=your_gemini_api_key
   ```

5. **Ensure Gmail API is enabled:**

   Follow [this guide](https://developers.google.com/gmail/api/quickstart/python) to enable Gmail API and obtain your credentials.

### Running the Application

1. **Start the workflow:**

   ```sh
   python main.py
   ```

   The application will start checking for new emails, categorizing them, synthesizing queries, drafting responses, and verifying email quality.

2. **Deploy as API:** you can deploy the workflow as an API using Langserve and FastAPI by running the command below:

   ```sh
   python deploy_api.py
   ```

   The workflow api will be running on `localhost:8000`, you can consult the API docs on `/docs` and you can use the langsergve playground (on the route `/playground`) to test it out.


### Customization

You can customize the behavior of each agent by modifying the corresponding methods in the `Nodes` class or the agents prompt `prompts` located in the `src` directory.

You can also add your own agency data into the `data` folder, then you must create your own vector store by running (update first the data path):

```sh
python create_index.py
```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

### Contact

If you have any questions or suggestions, feel free to contact me at `aymenMir1001@gmail.com`.
