# Chatbot RAG-BASED avec Streamlit

Ce projet est une interface de chatbot utilisant Streamlit, connectée à un backend via un webhook n8n.

## Prérequis
- Python 3.8+
- pip

## Installation

1. Clonez ce dépôt ou copiez les fichiers sur votre machine.
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement de l'application

Dans le dossier du projet, lancez :

```bash
streamlit run app.py
```

L'application sera accessible dans votre navigateur à l'adresse indiquée par Streamlit (par défaut http://localhost:8501).

## Configuration
- Le chatbot communique avec un webhook n8n à l'adresse : `http://localhost:5678/webhook/chatbot-app`
- Modifiez `WEBHOOK_URL` dans `app.py` si besoin.

## Fonctionnalités
- Interface conversationnelle moderne
- Historique de session
- Statistiques de conversation
- Réinitialisation de session

## Dépendances principales
- streamlit
- requests
- streamlit-extras

## Auteur
- Inspiré par des exemples de chatbots RAG et Streamlit. 