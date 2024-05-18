from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain

def _pdf_to_chunks(pdf):
        # read pdf and it returns memory address
        pdf_reader = PdfReader(pdf)

        # extrat text from each page separately
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split the long text into small chunks.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=200,
            length_function=len)

        chunks = text_splitter.split_text(text=text)
        return chunks
    
    
def _llm_qa(chunks, prompt):

        # Using OpenAI for embedding
        embeddings = GPT4AllEmbeddings()


        # Facebook AI Similarity Serach library help us to convert text data to numerical vector
        vectorstores = FAISS.from_texts(chunks, embedding=embeddings)

        # compares the query and chunks, enabling the selection of the top 'K' most similar chunks based on their similarity scores.
        docs = vectorstores.similarity_search(query=prompt, k=3)

        # creates an OpenAI object, using the ChatGPT 3.5 Turbo model
        llm = Ollama(model="llama3", temperature=0.5)

        # question-answering (QA) pipeline, making use of the load_qa_chain function
        chain = load_qa_chain(llm=llm, chain_type='stuff')

        response = chain.run(input_documents=docs, question=prompt)
        return response
    
def _prompt(query_with_chunks):

        query = f''' You are an expert resume evaluator. You provide 4 insights: 1. brief summary 2. weakneses 3. strengths 4. grade from 0 to 10 (2 decimals)

                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query
    
class Analyzer:
    
    def analyze(pdf):
        
        pdf_chunks = _pdf_to_chunks(pdf)

        prompt = _prompt(query_with_chunks=pdf_chunks)

        analysis = _llm_qa(chunks=pdf_chunks, prompt=prompt)
        
        return analysis
        
    






   