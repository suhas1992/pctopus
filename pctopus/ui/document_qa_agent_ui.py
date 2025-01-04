import gradio as gr
from pctopus.agent.document_qa import DocumentQAAgent
from pctopus.llm.openai_llm import OpenAILLM
from pctopus.reader.document_reader import DocumentReader

doc_reader = DocumentReader()
supported_doc_formats = doc_reader.supported_formats()

def ask_doc_qa_agent(file_obj, question: str, model: str):
    """Process a document and answer questions using the specified OpenAI model.
    
    Args:
        file_obj: Gradio file object containing the uploaded document
        question: User's question about the document
        model: Name of the LLM model to use
        
    Returns:
        Answer to the question or error message
    """
    if file_obj is None:
        return "Error: Please upload a document first."
    
    if not question.strip():
        return "Error: Please enter a question."

    llm = OpenAILLM()
    doc_qa_agent = DocumentQAAgent(llm)

    try:
        response = doc_qa_agent.ask(
            document_path=file_obj.name,
            question=question,
            model=model
        )
        return response

    except Exception as e:
        return f"Error: {str(e)}"

def create_document_qa_gradio_app():
    """Create a Gradio interface for document Q&A system."""
    with gr.Blocks() as demo:
        gr.Markdown("# Document Q&A Agent")
        gr.Markdown("Upload a document and ask questions about its content.")
        
        with gr.Row():
            with gr.Column():
                file_input = gr.File(
                    label="Upload Document", 
                    file_types=supported_doc_formats)
                model_dropdown = gr.Dropdown(
                    choices=["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
                    value="gpt-3.5-turbo",
                    label="Select Model",
                    info="Choose the model for question answering"
                )
                question_input = gr.Textbox(
                    label="Your Question",
                    placeholder="Enter your question about the document here..."
                )
                submit_btn = gr.Button("Get Answer", variant="primary")
            
            with gr.Column():
                output = gr.Textbox(label="Answer")
    
        # Handle file submission
        submit_btn.click(
            ask_doc_qa_agent,
            inputs=[file_input, question_input, model_dropdown],
            outputs=output
        )

        return demo
    
    
if __name__ == "__main__":
    app = create_document_qa_gradio_app()
    app.launch()
