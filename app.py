import streamlit as st

from functions import load_pdf_data, load_txt_data, process_document, process_query
from config import embeddings

import chromadb
from langchain.vectorstores import Chroma

# Missing stuff clear upload box after upload --> use st.form
# Set collection field to newly created
# Use open source model for embedding
# add field to show sources

def main(client):
    st.title("Chat With Your Documents")
    st.header("Step 1 (optional):")
    st.subheader("Create a new collection")
    with st.form('select_collection'):
        new_collection = st.text_input("Create new collection:")
        submitted = st.form_submit_button("Submit")
        if submitted:
            collection_name = "_".join(new_collection.split(" "))
            index = Chroma(
                    client=client,
                    collection_name=collection_name,
                    embedding_function=embeddings,
                )    
    
    st.header("Step 2 (optional):")
    st.subheader("Add a new document to the collection")
    with st.form("upload_document"):
        uploaded_files = st.file_uploader("Upload a file", type=["txt", "pdf"], accept_multiple_files=True)
        options = [x.name for x in client.list_collections()]
        collection_name = st.selectbox(
        'Choose collection',
        options
        )
        processed = st.form_submit_button("Process document")
        if processed:
            for file in uploaded_files:
                if file.type == "text/plain":
                    doc = "text"
                    data = load_txt_data(file)
                    splits = process_document(file.type)
                    index = Chroma(
                            client=client,
                            collection_name=collection_name,
                            embedding_function=embeddings,
                        )
                    index.add_documents(splits)
                    print(f'Added {len(splits)} to vector DB. Count: {index._collection.count()}')

                elif file.type == "application/pdf":
                    doc = "text"
                    data = load_pdf_data(file)
                    splits = process_document(file.type)
                    index = Chroma(
                            client=client,
                            collection_name=collection_name,
                            embedding_function=embeddings,
                        )
                    index.add_documents(splits)
                    print(f'Added {len(splits)} to vector DB. Count: {index._collection.count()}')


    

        # do something with the data

    st.header("Step 3:")
    st.subheader("Chat with your documents")
    with st.form("question"):
        options = [x.name for x in client.list_collections()]
        collection_name = st.selectbox(
        'Choose collection',
        options
        )
        question = st.text_input("Enter your question here:")
        submit_button = st.form_submit_button('Submit')

        if submit_button:
                index = Chroma(
                        client=client,
                        collection_name=collection_name,
                        embedding_function=embeddings,
                    )
                qa_chain = process_query(index)
                response = qa_chain({"query": question})
                st.markdown("## Response:")
                st.markdown(response["result"])
                st.markdown("## Sources:")
                for source in response["source_documents"]:
                    print(source.page_content)


if __name__ == "__main__":
    client = chromadb.PersistentClient(path='./chroma/chromadb')
    main(client)