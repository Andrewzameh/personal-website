import json
import queue
import sys
from typing import Any, Dict, List
import threading

from langchain.schema import LLMResult

from flask import Blueprint, render_template, request, Response
from flask import Flask, render_template

from langchain.document_loaders import TextLoader, UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import OpenAI

from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import SpacyTextSplitter
from langchain.text_splitter import NLTKTextSplitter

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.retrievers import KNNRetriever

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredFileLoader
from os import path

chain = Blueprint("chain", __name__)

q = queue.Queue()
stop_item = "###finish###"
new_token_event = threading.Event()


class StreamingStdOutCallbackHandlerYield(StreamingStdOutCallbackHandler):
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        with q.mutex:
            q.queue.clear()

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        sys.stdout.write(token)
        sys.stdout.flush()
        q.put(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        q.put(stop_item)


class StreamingOutputThread(threading.Thread):
    def __init__(self, question, retriever, chain_type_kwargs):
        super().__init__()
        self.question = question
        self.retriever = retriever
        self.chain_type_kwargs = chain_type_kwargs

    def run(self):
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.retriever,
            # return_source_documents=True,
            chain_type_kwargs=self.chain_type_kwargs,
        )
        for token in qa_chain(self.question):
            q.put(token)
            q.put(stop_item)


# Prmpt Handling - give a long detailed answer as per the context only,
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:{context}

User: I need a full answer as per the context above only for this question, {question}
Assistant:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Models
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = OpenAI(
    model="text-embedding-ada-002",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandlerYield()],
    max_tokens=1000,
    stop="USER",
    temperature=0,
)  # select your faux openai model name


@chain.route("/QA", methods=["GET", "POST"])
def QABot():
    return render_template("QA.html")


@chain.route("/QARes", methods=["GET", "POST"])
def QA_response():
    q.queue.clear()
    userInput = request.args.get("question")
    print("userInput: %s" % (userInput))
    mode = request.args.get("mode")

    # Documents
    # loader = TextLoader('C:/Users/andrew.sameh/OneDrive - Valsoft Aspire/Repos/GPT-FT/text-generation-webui-main/state_of_the_union.txt',encoding='utf-8')
    # loader = TextLoader('C:/Users/andrew.sameh/OneDrive - Valsoft Aspire/Repos/GPT-FT/text-generation-webui-main/text.txt',encoding='utf-8')
    # loader = UnstructuredPDFLoader('C:/Users/andrew.sameh/Downloads/Documents/SSA User Guide.pdf',encoding='utf-8')
    # loader = DirectoryLoader(docPath, glob="./*.pdf", loader_cls=UnstructuredPDFLoader)
    # loader = UnstructuredEPubLoader("/content/Running Lean_ Iterate from Plan A to a Plan That Works (Lean Series) - Maurya, Ash.epub") #, mode="elements"

    # newDB = True
    newDB = False

    if newDB:
        faissIndex = "db-InnQuest-new"
        persist_directory = "db-InnQuest-new"
        docPath = path.join(path.dirname(path.realpath(__file__)), "..", "Documents")
        text_loader_kwargs = {"autodetect_encoding": True}
        # loader = DirectoryLoader(docPath, glob="./*.*", loader_cls=UnstructuredFileLoader,use_multithreading=True)
        loader = DirectoryLoader(
            docPath,
            glob="./*.txt",
            loader_cls=TextLoader,
            use_multithreading=True,
            loader_kwargs=text_loader_kwargs,
        )
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            # separators="/n/n/n",
            chunk_size=1000,
            chunk_overlap=200,
            # length_function=len,
            # add_start_index=True,
        )
        # text_splitter = NLTKTextSplitter(separator="/n/n/n",chunk_size=1000)
        dataSplitted = text_splitter.split_documents(data)
        # Chroma
        vectordb = Chroma.from_documents(
            documents=dataSplitted,
            embedding=embedding,
            persist_directory=persist_directory,
        )
        vectordb.persist()
        # FAISS
        # vectordb = FAISS.from_documents(documents=dataSplitted,
        #                                  embedding=embedding)
        # vectordb.save_local(faissIndex)
        
    else:
        if mode == "ssa":
            persist_directory = "db-SSA"
        elif mode == "speech":
            persist_directory = "db-Stat"
        elif mode == "lightspeed":
            persist_directory = "db-LightSpeed"
        elif mode == "innquest":
            # persist_directory = 'db-InnQuest'
            # persist_directory = 'db-InnQuest-old'
            persist_directory = "db-InnQuest-new"
            # faissIndex = 'db-InnQuest-FAISS'

        vectordb = Chroma(
            persist_directory=persist_directory, embedding_function=embedding
        )
        # vectordb = FAISS.load_local(faissIndex, embedding)

    # retriever
    # retriever = vectordb.as_retriever(search_kwargs={"k": 4},search_type="mmr")
    retriever = vectordb.as_retriever(search_kwargs={"k": 3, "include_metadata": False})
    # retriever = vectordb.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5})
    # retriever = vectordb.as_retriever(search_kwargs={"k": 2},)
    docs = retriever.get_relevant_documents(userInput)
    print("docs: %s" % (docs))

    chain_type_kwargs = {"prompt": PROMPT}

    # threading.Thread(target= qa_chain, args=(userInput))
    streaming_thread = StreamingOutputThread(userInput, retriever, chain_type_kwargs)
    streaming_thread.start()

    def generate_output():
        comp = ""
        while True:
            token = q.get()
            if token == stop_item:
                response_dict = {"streaming_completed": True}
                yield f"data: {json.dumps(response_dict)}\n\n"
                break
            comp += token
            htmlAnswer = comp.replace("\n", "<br>")
            compDict = {"content": htmlAnswer}
            yield f"data: {json.dumps(compDict)}\n\n"

    # qa_chain(userInput)
    print("mode: %s" % (mode))
    return Response(generate_output(), mimetype="text/event-stream")
