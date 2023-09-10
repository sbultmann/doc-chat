import streamlit as st

from functions import load_pdf_data, load_txt_data, process_document, process_query
from config import embeddings

import chromadb
from langchain.vectorstores import Chroma

# Missing stuff clear upload box after upload --> use st.form
# Set collection field to newly created
# Use open source model for embedding

def main(client):
    options = [x.name for x in client.list_collections()]
    st.title("Chat With Your Documents")
    st.header("Step 1: Choose or create a collection:")
    new_collection = st.text_input("Create new collection:")
    option = st.selectbox(
        'Choose existing collection',
        options
        )
    

    st.header("Step 2: Add a new document to the collection:")
    file = st.file_uploader("Upload a file", type=["txt", "pdf"])


    if file is not None:
        if file.type == "text/plain":
            doc = "text"
            data = load_txt_data(file)
            splits = process_document(file.type)
            if new_collection:
                print("new collection chosen ...")
                index = Chroma(
                        client=client,
                        collection_name=new_collection,
                        embedding_function=embeddings,
                    )
                index.add_documents(splits)
            elif option:
                print(f"old collection chosen ... NAME:{option}")
                index = Chroma(
                    client=client,
                    collection_name=option,
                    embedding_function=embeddings,
                )
                index.add_documents(splits)
            print(f'Added {len(splits)} to vector DB. Count: {index._collection.count()}')

        elif file.type == "application/pdf":
            doc = "text"
            data = load_pdf_data(file)
            splits = process_document(file.type, index)
            if new_collection:
                print("new collection chosen ...")
                index = Chroma(
                        splits,
                        client=client,
                        collection_name=new_collection,
                        embedding_function=embeddings,
                    )
            elif option:
                print("old collection chosen ...")
                index = Chroma(
                    splits,
                    client=client,
                    collection_name=option,
                    embedding_function=embeddings,
                )
            index.add(splits)
            print(f'Added {len(splits)} to vector DB. Count: {index._collection.count()}')

        # do something with the data

        st.header("Step 3: Chat with your documents:")
        question = st.text_input("Enter your question here:")
        submit_button = st.button('Submit')

        if submit_button:
            if doc == "text":
                qa_chain = process_query(index)
                response = qa_chain({"query": question})["result"]

            if response:
                st.markdown(response)


if __name__ == "__main__":
    client = chromadb.PersistentClient(path='./chroma/chromadb')
    main(client)