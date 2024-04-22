import chainlit as cl
from app import PDF_chat

@cl.on_chat_start
async def on_chat_start():

    files = None

    # Wait for the user to upload a PDF file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a PDF file to begin!",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]
    pdf_path = file.name
    cl.user_session.set("pdf_file", pdf_path)
    print("file upload done")
    print("File path:",pdf_path)

    @cl.on_message
    async def main(message:str):
        message = message.content
        print("Query : ",message)
        cb = cl.AsyncLangchainCallbackHandler(
            stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
        )
        cb.answer_reached = True

        pdf_file = cl.user_session.get("pdf_file")
        chat = PDF_chat(pdf_file,message)
        result = chat.main()
        await cl.Message(content=result).send()