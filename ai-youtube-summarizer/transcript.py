import re
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_video_id(url: str) -> str | None:
    pattern = r'https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(url: str):
    video_id = get_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    transcripts = ytt_api.list(video_id)

    transcript = ""
    for t in transcripts:
        if t.language_code == 'en':
            if t.is_generated:
                if len(transcript) == 0:
                    transcript = t.fetch()
            else:
                transcript = t.fetch()
                break

    return transcript if transcript else None


def process(transcript) -> str:
    txt = ""
    for i in transcript:
        try:
            txt += f"Text: {i.text} Start: {i.start}\n"
        except KeyError:
            pass
    return txt


def chunk_transcript(processed_transcript: str, chunk_size: int = 200, chunk_overlap: int = 20) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_text(processed_transcript)
