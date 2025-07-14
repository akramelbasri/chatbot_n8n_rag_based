# Bonne pratique : importer d'abord les modules standards, puis les modules externes, puis les modules locaux
import streamlit as st
import requests
import uuid
import time
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime

# Constants
WEBHOOK_URL = "http://localhost:5678/webhook/chatbot-app"

# Configuration de la page
st.set_page_config(
    page_title="Chatbot RAG-BASED",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration des styles CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    .user-message {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .assistant-message {
        background-color: #F1F1F1;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #2E86AB;
        padding: 10px 20px;
    }
    
    .stButton > button {
        border-radius: 20px;
        background-color: #2E86AB;
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #1A5276;
    }
    
    /* Styles pour les messages de chat */
    .chat-message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 18px 18px 5px 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        margin-left: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .chat-message-assistant {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 18px 18px 18px 5px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        margin-right: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_session_id():
    return str(uuid.uuid4())

def send_message_to_n8n_rag_based(session_id, message):
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["output"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion: {str(e)}"
    except Exception as e:
        return f"Erreur inattendue: {str(e)}"

def create_unique_key(role, index, session_id):
    """Crée une clé unique pour chaque élément Streamlit"""
    return f"{role}_message_{index}_{session_id}"

def add_timestamp_to_message(role, content):
    """Ajoute un timestamp au message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    return {
        "role": role,
        "content": content,
        "timestamp": timestamp
    }

def clear_conversation():
    """Efface l'historique de la conversation"""
    st.session_state.messages = []
    st.session_state.session_id = generate_session_id()
    st.rerun()

def main():
    # Initialisation
    load_css()
    
    # Header avec style
    st.markdown('<h1 class="main-header">🤖 Conversational Chatbot RAG-BASED</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Posez vos questions et obtenez des réponses intelligentes</p>', unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Sidebar avec informations
    with st.sidebar:
        st.header("🛠️ Configuration")
        
        # Afficher l'ID de session
        st.text(f"Session ID: {st.session_state.session_id[:8]}...")
        
        # Bouton pour effacer la conversation
        if st.button("🗑️ Effacer la conversation", type="secondary"):
            clear_conversation()
        
        # Statistiques
        st.header("📊 Statistiques")
        st.metric("Messages totaux", len(st.session_state.messages))
        user_messages = len([m for m in st.session_state.messages if m.get("role") == "user"])
        st.metric("Vos messages", user_messages)
        st.metric("Réponses assistant", len(st.session_state.messages) - user_messages)
        
        # Statut de connexion
        st.header("🔗 Connexion")
        st.info(f"Webhook: {WEBHOOK_URL}")

    # Zone de chat
    st.header("💬 Conversation")
    
    # Conteneur pour les messages avec style
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.messages:
            # Display chat messages avec styles
            for i, message in enumerate(st.session_state.messages):
                unique_key = create_unique_key(message["role"], i, st.session_state.session_id)
                
                if message["role"] == "user":
                    with stylable_container(
                        key=unique_key,
                        css_styles="""
                        {
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            border-radius: 18px 18px 5px 18px;
                            padding: 12px 16px;
                            margin: 8px 0;
                            max-width: 70%;
                            margin-left: auto;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        """
                    ):
                        st.markdown(f"**Vous:** {message['content']}")
                        if "timestamp" in message:
                            st.caption(f"_{message['timestamp']}_")
                
                else:
                    with stylable_container(
                        key=unique_key,
                        css_styles="""
                        {
                            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            color: white;
                            border-radius: 18px 18px 18px 5px;
                            padding: 12px 16px;
                            margin: 8px 0;
                            max-width: 70%;
                            margin-right: auto;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        """
                    ):
                        st.markdown(f"**Assistant:** {message['content']}")
                        if "timestamp" in message:
                            st.caption(f"_{message['timestamp']}_")
        else:
            st.info("👋 Salut ! Commencez la conversation en tapant votre message ci-dessous.")

    # Zone d'input avec style
    st.header("✍️ Votre message")
    
    # User input
    user_input = st.chat_input("Tapez votre message ici...")

    if user_input:
        # Add user message to chat history avec timestamp
        user_message = add_timestamp_to_message("user", user_input)
        st.session_state.messages.append(user_message)
        
        # Afficher le message utilisateur immédiatement
        with stylable_container(
            key=f"temp_user_message_{len(st.session_state.messages)}",
            css_styles="""
            {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 18px 18px 5px 18px;
                padding: 12px 16px;
                margin: 8px 0;
                max-width: 70%;
                margin-left: auto;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            """
        ):
            st.markdown(f"**Vous:** {user_input}")
            st.caption(f"_{user_message['timestamp']}_")

        # Afficher un spinner pendant le traitement
        with st.spinner("🤖 Génération de la réponse..."):
            # Get LLM response
            llm_response = send_message_to_n8n_rag_based(st.session_state.session_id, user_input)

        # Add LLM response to chat history avec timestamp
        assistant_message = add_timestamp_to_message("assistant", llm_response)
        st.session_state.messages.append(assistant_message)
        
        # Afficher la réponse de l'assistant
        with stylable_container(
            key=f"temp_assistant_message_{len(st.session_state.messages)}",
            css_styles="""
            {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                border-radius: 18px 18px 18px 5px;
                padding: 12px 16px;
                margin: 8px 0;
                max-width: 70%;
                margin-right: auto;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            """
        ):
            st.markdown(f"**Assistant:** {llm_response}")
            st.caption(f"_{assistant_message['timestamp']}_")
        
        # Rerun pour afficher tous les messages avec les bonnes clés
        st.rerun()

if __name__ == "__main__":
    main()

