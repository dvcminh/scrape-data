from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "model": "ollama/mistral",
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",
    },
    "verbose": True,
}
smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the products with their descriptions",
    source="https://tiki.vn/dien-thoai-may-tinh-bang/c1789",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)
