import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()


def _get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set")
    return TavilyClient(api_key=api_key)


def _get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")
    return Groq(api_key=api_key)


def get_realtime_info(query: str, *, max_results: int = 3) -> str:
    """
    Fetches up-to-date information about any topic using Tavily Search API
    and summarizes it using Groq.
    """
    tavily_client = _get_tavily_client()
    resp = tavily_client.search(query=query, max_results=max_results, topic="general")

    if resp and resp.get("results"):
        summaries = []
        for r in resp["results"]:
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            url = r.get("url", "")
            summaries.append(f"**{title}**\n\n{snippet}\n\n🔗 {url}")
        source_info = "\n\n---\n\n".join(summaries)
    else:
        source_info = f"No recent updates found on '{query}'."

    model = os.getenv("GROQ_MODEL_INFO", "llama-3.1-8b-instant")
    prompt = f"""
You are a professional researcher and content creator with expertise in multiple fields.
Using the following real-time information, write an accurate, engaging, and human-like summary
for the topic: '{query}'.

Requirements:
- Keep it factual, insightful, and concise (around 200 words).
- Maintain a smooth, natural tone.
- Highlight key takeaways or trends.
- Avoid greetings or self-references.

Source information:
{source_info}

Output only the refined, human-readable content.
"""

    client = _get_groq_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
    )
    content = response.choices[0].message.content if response and response.choices else None
    return content.strip() if content else source_info


def generate_video_transcription(info_text: str) -> str:
    prompt = f"""
You are a creative scriptwriter.
Turn this real-time information into an engaging short video script (for YouTube Shorts or Instagram Reels).
Use a conversational tone with a strong hook and a clear call to action at the end.
Keep it around 100–120 words.

{info_text}
"""
    model = os.getenv("GROQ_MODEL_SCRIPT", "llama-3.1-8b-instant")
    client = _get_groq_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=220,
    )
    content = response.choices[0].message.content if response and response.choices else None
    return content.strip() if content else "⚠️ Could not generate video script."

