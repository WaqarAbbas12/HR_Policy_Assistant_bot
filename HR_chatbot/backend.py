from flask import Flask, request, jsonify
from connection import connectDB, create_collection
from chunks import extract_text_from_pdf, ChunkData, CreateDataObjects
import weaviate.classes.config as wc
import weaviate.classes as wvc
import os
import tempfile
import atexit

app = Flask(__name__)


client = connectDB()


atexit.register(lambda: client.close())

collection_name = "Document"

if collection_name not in client.collections.list_all():
    create_collection(client)

collection = client.collections.get(collection_name)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "No selected file"}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            file.save(temp.name)
            text = extract_text_from_pdf(temp.name)
            chunks = ChunkData(text)
            CreateDataObjects(chunks, collection)
        return jsonify({"message": "PDF processed and data stored successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query is missing."}), 400

        print(f"[INFO] Received query: {query}")

        # Step 1: Semantic Search
        response = collection.query.near_text(
            query=query,
            limit=1,
            return_metadata=wvc.query.MetadataQuery(score=True, explain_score=True),
        )

        print("[DEBUG] Query response:", response)

        if not response.objects:
            return (
                jsonify(
                    {
                        "response": "I'm sorry, I couldn't find relevant information.",
                        "detail": "No similar chunks were found for the given query.",
                    }
                ),
                200,
            )

        top_result = response.objects[0]
        context = top_result.properties.get("body", "")
        score = top_result.metadata.score or 0.0

        if not context:
            return (
                jsonify(
                    {
                        "error": "'body' field missing in Weaviate response object.",
                        "raw_response": str(top_result),
                    }
                ),
                500,
            )

        gen_response = collection.generate.near_text(
            query=query,
            limit=1,
            return_metadata=wvc.query.MetadataQuery(score=True),
            single_prompt=f"""You are a helpful HR assistant. Use the context below, retrieved from the company's 
HR policy document, to answer the question clearly and accurately. 
If the context does not contain enough information to answer, reply with: 
"I'm sorry, I couldn't find relevant information in the uploaded document."

Context:
{context}

Question:
{query}

Answer:""",
        )

        print("[DEBUG] Generation response:", gen_response)

        if gen_response.objects:
            answer = gen_response.objects[0].generated
            return (
                jsonify(
                    {
                        "response": answer,
                        "context": context,
                        "score": score,
                        "query": query,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "response": "I'm sorry, I couldn't find relevant information.",
                        "detail": "No generated response returned by the LLM.",
                        "context": context,
                        "score": score,
                    }
                ),
                200,
            )

    except Exception as e:
        print("[ERROR] Exception in /chat route:", e)
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500


@app.route("/end_chat", methods=["POST"])
def end_chat():
    try:
        if collection_name in client.collections.list_all():
            client.collections.delete(collection_name)
            print(f"Collection '{collection_name}' deleted successfully.")
            return jsonify(
                {"message": f"Collection '{collection_name}' deleted successfully."}
            )
        else:
            return (
                jsonify({"message": f"Collection '{collection_name}' does not exist."}),
                404,
            )
    except Exception as e:
        print(f"Error deleting collection: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
