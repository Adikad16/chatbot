# main.py

import os
import json
import datetime

import streamlit as st
import google.generativeai as genai

from google.cloud import discoveryengine_v1 as discoveryengine
from google.cloud import storage
from google.api_core.client_options import ClientOptions


# ================================
# Configuration & Environment Setup
# ================================

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "chatbot.json"

PROJECT_ID = "mini-project-454908"
LOCATION = "global"
DATA_STORE_ID = "mini-proj-atgeir_1743403050571"
ENGINE_ID = "mini-proj-atgeir_1743403000829"
GENAI_API_KEY = "AIzaSyBzNKFDGFaAq5n3shmKLN3eunoaV1Iiybw"

GREETINGS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
GOODBYES = ["bye", "goodbye", "exit", "quit"]


# ================================
# Client Creation Functions
# ================================

def create_conversation_client():
    """
    Creates and returns a ConversationalSearchServiceClient for interacting with 
    the Google Cloud Discovery Engine's conversational search service.

    Returns:
        discoveryengine.ConversationalSearchServiceClient
    """
    options = ClientOptions(api_endpoint="global-discoveryengine.googleapis.com")
    return discoveryengine.ConversationalSearchServiceClient(client_options=options)


def create_search_client():
    """
    Creates and returns a SearchServiceClient for interacting with 
    the Google Cloud Discovery Engine's search service.

    Returns:
        discoveryengine.SearchServiceClient
    """
    options = ClientOptions(api_endpoint="global-discoveryengine.googleapis.com")
    return discoveryengine.SearchServiceClient(client_options=options)


# ================================
# Document Interaction Functions
# ================================

def search_data_store(query, search_client):
    """
    Performs a semantic and keyword-based search over the documents indexed in 
    the Discovery Engine data store using the provided query.

    Args:
        query (str): User query
        search_client (SearchServiceClient): Discovery Engine search client

    Returns:
        discoveryengine.SearchResponse
    """
    serving_config = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/engines/{ENGINE_ID}/servingConfigs/default_config"

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=query,
        page_size=10,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(return_snippet=True),
            summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                summary_result_count=5,
                include_citations=True,
                ignore_adversarial_query=True,
                ignore_non_summary_seeking_query=True,
                model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
                    preamble="Answer the user's question based on the provided documents."
                ),
                model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(version="stable"),
            )
        ),
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO,
        ),
    )

    return search_client.search(request)


def converse_with_documents(query, conversation_id=None, conv_client=None):
    """
    Sends a user query to the Conversational Search API and returns a response.

    Args:
        query (str): User query
        conversation_id (str, optional): Ongoing conversation ID
        conv_client (ConversationalSearchServiceClient, optional): Client instance

    Returns:
        Tuple[ConverseConversationResponse, str]
    """
    if conv_client is None:
        conv_client = create_conversation_client()

    serving_config = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/engines/{ENGINE_ID}/servingConfigs/default_config"

    if not conversation_id:
        conv_request = discoveryengine.CreateConversationRequest(
            parent=f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/engines/{ENGINE_ID}",
            conversation=discoveryengine.Conversation()
        )
        conversation = conv_client.create_conversation(conv_request)
        conversation_id = conversation.name

    request = discoveryengine.ConverseConversationRequest(
        name=conversation_id,
        query=query,
        serving_config=serving_config,
    )

    response = conv_client.converse_conversation(request)
    return response, conversation_id


# ================================
# Gemini Summarization
# ================================

def summarize_chat(messages):
    """
    Summarizes a chat conversation using the Gemini model.

    Args:
        messages (list): List of chat messages

    Returns:
        str: Summary of the conversation
    """
    if not messages:
        return "No conversation history available to summarize."

    conversation_text = "\n".join(
        f"User: {msg['content']}" if msg["role"] == "user" else f"Assistant: {msg['content']}"
        for msg in messages
    )

    trimmed_text = conversation_text[:3000]

    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash-001")

    response = model.generate_content(f"Summarize the following conversation:\n\n{trimmed_text}")
    return response.text.strip() if response.text else "Summarization failed."


# ================================
# Query Processing
# ================================

def process_query(query):
    """
    Processes a user query and returns a formatted response.

    Args:
        query (str): User query

    Returns:
        str: Final assistant response
    """
    search_client = create_search_client()
    conv_client = create_conversation_client()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    })

    query_lower = query.lower()

    if any(greet in query_lower for greet in GREETINGS) and len(query.split()) <= 2:
        answer = "Hello! How can I assist you today?"
        st.session_state.messages.append({"role": "assistant", "content": answer})
        return answer

    if any(farewell in query_lower for farewell in GOODBYES):
        answer = "Goodbye! Have a great day!"
        st.session_state.messages.append({"role": "assistant", "content": answer})
        return answer

    try:
        response, st.session_state.conversation_id = converse_with_documents(
            query, st.session_state.get("conversation_id"), conv_client
        )
        answer = response.reply.reply.text
        sources = "Sources: " + ", ".join(
            [doc.document_id for doc in response.search_results[:3]]
        ) if response.search_results else ""
    except Exception:
        response = search_data_store(query, search_client)
        fr = list(response.results)
        print(fr, "***********", fr)
        if len(fr) != 0:
            answer, sources = get_answer_and_sources(response, fr)
        else:
            answer = "I couldn't find an answer to your question. Please try a different one."
            sources = "No relevant documents found."

    full_response = f"{answer}\n\nSources: {sources}"
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return full_response

def get_answer_and_sources(response, fr):
    first_result = fr[0]

    document = first_result.document
    jsn = json.loads(discoveryengine.Document.to_json(document))
    gcs_url = jsn["derivedStructData"]["link"]

    lst = gcs_url.split("/")
    file_name = lst[-1]
    bucket_name = lst[2]
    blob_name = "/".join(lst[3:])

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    expiration = datetime.timedelta(minutes=60)
    signed_url = blob.generate_signed_url(expiration=expiration, method="GET")

    pdf_link = f"[📄 {file_name}]({signed_url})"

    if hasattr(response, 'summary') and response.summary.summary_text:
        answer = response.summary.summary_text
    else:
        snippets = [
                result.document.derived_struct_data.fields["snippets"].list_value.values[0]
                .struct_value.fields["snippet"].string_value
                for result in response.results
                if "snippets" in result.document.derived_struct_data.fields
            ]
        answer = "Here's what I found:\n\n" + "\n\n".join(snippets) if snippets else \
                "I couldn't find specific information about that in the documents."

    sources = pdf_link
    return answer,sources
