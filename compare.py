import os
import matplotlib.pyplot as plt
from apify_client import ApifyClient

KEYWORDS = ["chatgpt", "gemini", "claude", "copilot", "perplexity", "midjourney",
            "stable diffusion", "llama", "mistral", "deepseek", "grok", "notebooklm"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("satin_armeria/google-trends-advanced-comparator").call(
    run_input={"keywords": KEYWORDS, "geo": "", "timeframe": "today 12-m"})
rows = client.dataset(run["defaultDatasetId"]).list_items().items
summary = client.key_value_store(run["defaultKeyValueStoreId"]).get_record("OUTPUT")["value"]
print("self-check:", summary["validation"]["selfCheck"].get("meanAbsErrorPoints"), "points")

for kw in KEYWORDS:
    pts = [r for r in rows if r["keyword"] == kw]
    plt.plot([p["date"] for p in pts], [p["value"] for p in pts], label=kw)
plt.xticks([]); plt.ylabel("Interest (common 0-100 scale)"); plt.legend(ncol=3, fontsize=8)
plt.savefig("comparison.png", dpi=120)
