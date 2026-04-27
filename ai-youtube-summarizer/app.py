import gradio as gr
from transcript import get_transcript, process, chunk_transcript
from llm import get_llm, get_embedding_model
from vector_store import build_faiss_index
from chains import build_summary_chain, build_qa_chain, generate_summary, generate_answer

# Cached processed transcript across button clicks
processed_transcript = ""


def summarize_video(video_url: str) -> str:
    global processed_transcript

    if not video_url:
        return "Please provide a valid YouTube URL."

    raw = get_transcript(video_url)
    if not raw:
        return "No English transcript found for this video."

    processed_transcript = process(raw)

    llm = get_llm()
    chain = build_summary_chain(llm)
    return generate_summary(chain, processed_transcript)


def answer_question(video_url: str, user_question: str) -> str:
    global processed_transcript

    if not processed_transcript:
        if not video_url:
            return "Please provide a valid YouTube URL."
        raw = get_transcript(video_url)
        if not raw:
            return "No English transcript found for this video."
        processed_transcript = process(raw)

    if not user_question:
        return "Please enter a question."

    chunks = chunk_transcript(processed_transcript)
    embedding_model = get_embedding_model()
    faiss_index = build_faiss_index(chunks, embedding_model)

    llm = get_llm()
    chain = build_qa_chain(llm)
    return generate_answer(chain, faiss_index, user_question)


with gr.Blocks() as interface:
    gr.Markdown("<h2 style='text-align: center;'>YouTube Video Summarizer and Q&A</h2>")

    video_url = gr.Textbox(label="YouTube Video URL", placeholder="Enter the YouTube Video URL")

    summary_output = gr.Textbox(label="Video Summary", lines=5)
    question_input = gr.Textbox(label="Ask a Question About the Video", placeholder="Ask your question")
    answer_output = gr.Textbox(label="Answer to Your Question", lines=5)

    summarize_btn = gr.Button("Summarize Video")
    question_btn = gr.Button("Ask a Question")

    transcript_status = gr.Textbox(label="Transcript Status", interactive=False)

    summarize_btn.click(summarize_video, inputs=video_url, outputs=summary_output)
    question_btn.click(answer_question, inputs=[video_url, question_input], outputs=answer_output)

interface.launch(server_name="0.0.0.0", server_port=7860)
