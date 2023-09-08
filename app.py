import streamlit as st

from functions import load_pdf_data, load_txt_data, process_document, process_query

def main():
    st.title("Chat With Your Documents")

    file = st.file_uploader("Upload a file", type=["txt", "pdf"])


    if file is not None:
        if file.type == "text/plain":
            doc = "text"
            data = load_txt_data(file)
            index = process_document(file.type)

        elif file.type == "application/pdf":
            doc = "text"
            data = load_pdf_data(file)
            index = process_document(file.type)

        # do something with the data


        question = st.text_input("Once uploaded, you can chat with your document. Enter your question here:")
        submit_button = st.button('Submit')

        if submit_button:
            if doc == "text":
                qa_chain = process_query(index)
                response = qa_chain({"query": question})["result"]

            if response:
                st.markdown(response)


if __name__ == "__main__":
    main()