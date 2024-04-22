import os
from dotenv import load_dotenv
import typesense
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import Typesense
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import chainlit
import warnings
warnings.filterwarnings("ignore")

load_dotenv()


class PDF_chat():
    def __init__(self,pdf_path,query):
        self.OpenAI_API_KEY = os.getenv('OpenAI_API_KEY')
        self.pdf_path = pdf_path
        self.query = query
        store_name = self.pdf_path.split(".")[0].strip()  # extract pdf name from the file to create new collection with that name
        self.schema_name = store_name
        print(self.schema_name)


    def load_and_split_documents(self):
        """
        This function loads the pdf, extracts the text and creates chunks of data to be fed to the Typsense database

        """
        loader = PDFPlumberLoader(self.pdf_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)


    def init_typesense_search(self,docs, embeddings):
        """
        Here, we are setup our typesense configurations

        """
        return Typesense.from_documents(
            docs,
            embeddings,
            typesense_client_params={
                'host': 'your_hostname',
                'port': 'your_port',
                'protocol': 'https',
                "typesense_api_key": 'your_typesense_api_key',
                "typesense_collection_name": self.schema_name,
            }
        )

    def get_llm_answer(self,chain, retriever):
        """
        This function first fetches the relevant documents based on the query asked and we select top 3 documents
        These top documents are fed to the LLM model to answer our query, finally the model returns a string which has the answer to our query
        """
        retrieved_docs = retriever.get_relevant_documents(self.query)[:3]
        #print(retrieved_docs)
        with get_openai_callback() as cb:
            response = chain.run(input_documents=retrieved_docs, question=self.query)
            print(cb)
        return response
    
    def main(self):
        """
        This function is called to run all our methods and this finally returns the desired result

        """
        docs = self.load_and_split_documents()
        embeddings = OpenAIEmbeddings(openai_api_key=self.OpenAI_API_KEY)
        docsearch = self.init_typesense_search(docs, embeddings)
        retriever = docsearch.as_retriever()

        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        answer = self.get_llm_answer(chain, retriever)
        return answer

# pdf_path = 'fepw101.pdf'
# query = "What is the moral of the story"

# chat = PDF_chat(pdf_path,query)
# result = chat.main()
# print(result)
