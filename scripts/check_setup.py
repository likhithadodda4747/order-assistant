import os
from dotenv import load_dotenv
import psycopg, voyageai, anthropic

load_dotenv()

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    print("DB ok, chunks rows:", conn.execute("SELECT count(*) FROM chunks").fetchone()[0])

vec = voyageai.Client().embed(["hello"], model="voyage-3.5", input_type="document").embeddings[0]
print("Voyage ok, vector length:", len(vec))

msg = anthropic.Anthropic().messages.create(
    model="claude-haiku-4-5-20251001", max_tokens=20,
    messages=[{"role": "user", "content": "Say ok"}])
print("Claude ok:", msg.content[0].text)