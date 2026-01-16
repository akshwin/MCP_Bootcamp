from mcp.server.fastmcp import FastMCP
from storyforge_core import get_realtime_info, generate_video_transcription

mcp = FastMCP("this is for real time news ")

@mcp.tool()
async def fetch_new_mcp(query):
    return get_realtime_info(query=query)


@mcp.tool()
async def gen_vid_trans_mcp(query):
    news = get_realtime_info(query=query)
    return generate_video_transcription(news)


if __name__ == "__main__":
    mcp.run(transport = "stdio")