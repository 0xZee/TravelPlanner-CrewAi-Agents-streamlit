from crewai_tools import tool
from langchain_community.tools import DuckDuckGoSearchResults 
import json

# TOOLS

class SearchTool():
  
  @tool("search web tool")
  def search_web_tool(query):
    """
    Useful to search the internet about a query and return up-to-date relevant results.
    """
    #search_tool = DuckDuckGoSearchResults(backend="news", num_results=5 , verbose=True)
    search_tool = DuckDuckGoSearchResults(num_results=10 , verbose=True)
    return search_tool.run(query)
