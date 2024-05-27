from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma


class VectorStore():

    embedder = OpenAIEmbeddings()
    store=None


    def __init__(self ) -> None:
        self.store = Chroma(
            embedding_function=self.embedder,   
            persist_directory="vectors",
        )
    
    
    def repopulate(self, documents) -> None:
        self.store = Chroma.from_documents(
            documents, 
            embedding=self.embedder,
            persist_directory="vectors"
        )
    

class Chunker():

    sizing = 2000
    overlapping = 15


    def load(self, path):
        loader = None
        file = None

        if path.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            print("Unknown file type: ", path)

        if loader is not None:
            file = loader.load()
            print("Loaded file: ", path)

        return file
    

    def chunk(self, path):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.sizing,
            chunk_overlap=round(self.sizing * self.overlapping / 100),
            length_function=len,
            is_separator_regex=False,
        )

        return splitter.split_documents(self.load(path))

