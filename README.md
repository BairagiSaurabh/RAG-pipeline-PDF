# RAG-pipeline-PDF

**Problem Statement** : To build a RAG pipeline to chat with your PDF using Langchain, OpenAI, Typsense DB (as storage and retriever) and Chainlit(to deploy app and have a chatbot like interface)

**Approach** :

- Using PDFPlumber to read the PDF file and extract text.
- Creating chunks of data with some overlap to have previous knowledge of earlier chunk.
- To create embeddings of the chunks of data I have used OpenAI Embedddings.
- Once we have the chunks of data and initialized the embeddings, we store them in the Typesense database by creating a collection of documents where the collection has the same name as the pdf file.
- When the user asks the query, through cosine similarity we get top 3 documents which then will be fed to the LLM model for answering the question asked.
- Finally, creating a chatbot like interface which can store previous chat history as well to interact with our model.

**How to run the model** : 

1. First clone the repository and make sure you see all libraries listed in the requirements.txt
2. Run this command to install all the requrired packages (pip install -r requirements.txt)
3. Create a .env file to store your OpenAI API key, Typsense API key and your typesense host.
4. For generating Typesense API key and other credentials kindly refer this documentation [Typsense Docs](https://typesense.org/)

- **Running the app.py file** : This file contains the module with all the methods embedded. It can used in the backend for testing and debugging purposes. Run this file with this command **(python app.py)**

- **Running the chainlit app** : We call our class here to do all processing and finally get an answer given an input PDF and query.  Run this file with this command **(chainlit run chainlit_app.py -w)**

[Demo Link](https://www.loom.com/share/6dd91ee3b28c455487ca81338ac109b1?sid=43620e81-1b74-4bf6-bf6e-039fbe110479)
