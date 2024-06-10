# Customer Support Email Automation

I used Langchain/Langgraph to build a customer support email automation system for an AI agency. It consists of multiple AI agents working together to achieve the following steps:

- **Check for new emails in the agency GMAIL inbox.**
- **Categorize email into 'customer_complaint', 'product_enquiry', 'customer_feedback', 'unrelated'.**
- **Synthesize queries to extract relevant information from RAG to answer customer.**
- **Write a draft email to respond to the client.**
- **Email verifier: Check the quality and correct formatting of the email, and ensure its relevancy.**

## System Flowchart

This is the detailed flow of the system:

[![](https://mermaid.ink/img/pako:eNp1ks9uwjAMxl8lyqlI8AI9TBqUP5edthMUVVHilog26RwXxCjvPreFrWhaLkn8_T47cXKV2huQscxLf9YHhSQ-ktQJHq-7QLzfi9nsRcyj0iuTOThnUClbhskAzTu1haqmSyu2O3BmPxZq9BpCaMVipxVB4dF-wZDhzi0enGk0CYSSMdOKJNLeBUIOZqiK7LOBQJZDk7HNeRJ_rKvojJYgM6hyGmrdTUl_lWWEQGjhBFmOvurS3_Vlr__vX_X6OjoB2vySFeAAu5pP0Lo_WeBOtGITdfOTvHlq2NiC0NflC4zJ3w6mTk5lBcjJDD_YtaNSSQeoIJUxL43CYypTd2NONeTfL07LmHsIU4m-KQ4yzlUZeNfUhs-dWFWgqn6iYCx5fBv-Q_8tprJWbuv9g7l9A0wuuN4?type=png)](https://mermaid.live/edit#pako:eNp1ks9uwjAMxl8lyqlI8AI9TBqUP5edthMUVVHilog26RwXxCjvPreFrWhaLkn8_T47cXKV2huQscxLf9YHhSQ-ktQJHq-7QLzfi9nsRcyj0iuTOThnUClbhskAzTu1haqmSyu2O3BmPxZq9BpCaMVipxVB4dF-wZDhzi0enGk0CYSSMdOKJNLeBUIOZqiK7LOBQJZDk7HNeRJ_rKvojJYgM6hyGmrdTUl_lWWEQGjhBFmOvurS3_Vlr__vX_X6OjoB2vySFeAAu5pP0Lo_WeBOtGITdfOTvHlq2NiC0NflC4zJ3w6mTk5lBcjJDD_YtaNSSQeoIJUxL43CYypTd2NONeTfL07LmHsIU4m-KQ4yzlUZeNfUhs-dWFWgqn6iYCx5fBv-Q_8tprJWbuv9g7l9A0wuuN4)

## How to Run

### Prerequisites

- Python 3.7+
- Groq api key
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

   Create a `.env` file in the root directory of the project and add your GMAIL address, as we are using llama3-70b with Groq you must also get an API key to access it:

   ```env
   MY_EMAIL=your_email@gmail.com
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Ensure Gmail API is enabled:**

   Follow [this guide](https://developers.google.com/gmail/api/quickstart/python) to enable Gmail API and obtain your credentials.

### Running the Application

1. **Start the workflow:**

   ```sh
   python main.py
   ```

   The application will start checking for new emails, categorizing them, synthesizing queries, drafting responses, and verifying email quality.

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
