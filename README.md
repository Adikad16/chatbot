---
title: README - Atgeir Intranet Chatbot
---

# 📌 Project Overview {#project-overview}

This repository contains a chatbot built using Google Cloud\'s Vertex AI
Agent Builder. It utilizes a custom data store and supports
document-based Q&A interactions through a Streamlit-based UI.

# ✨ Features {#features}

\- Multi-turn conversational chat powered by Vertex AI Agent Builder

\- Summarization of chat history using Gemini Pro

\- GCS-based document search with signed URLs for PDF access

\- Interactive UI built using Streamlit with animated chatbot visuals

\- Integrated fallback mechanism with custom document retrieval

# 📁 Folder Structure {#folder-structure}

• \`main.py\` - Core logic to handle queries, search, summarization, and
interaction with Agent Builder.  
• \`ui.py\` - Frontend powered by Streamlit to interact with users.  
• \`chatbot.json\` - GCP service account key (not included for security
reasons).

# ⚙️ Setup {#setup}

1\. Clone this repository.

2\. Install required dependencies:

pip install -r requirements.txt

3\. Place your GCP service account key as \`chatbot.json\`.

4\. Run the application using Streamlit:

streamlit run ui.py

# 🔧 Configuration {#configuration}

Set the following in \`main.py\`:

\- \`PROJECT_ID = \"mini-project-454908\"\`  
- \`LOCATION = \"global\"\`  
- \`DATA_STORE_ID = \"mini-proj-atgeir_1743403050571\"\`  
- \`ENGINE_ID = \"mini-proj-atgeir_1743403000829\"\`

# 🙌 Credits {#credits}

Built with ❤️ using Google Cloud, Vertex AI, and Streamlit.
