# Language Agnostic Chatbot

## Project Overview

The Language Agnostic Chatbot is an AI-powered multilingual communication platform designed to enable users to interact seamlessly in different languages without manually selecting a preferred language. The system automatically detects the input language, translates and processes the request using Natural Language Processing (NLP), and generates accurate responses in the user’s language.

The platform integrates language detection, translation services, chatbot response generation, conversation history tracking, and analytics into a centralized system. It is designed to improve communication accessibility and support users from diverse linguistic backgrounds.

The solution is suitable for educational platforms, customer support systems, business communication platforms, and multilingual digital services.

---

## Objective

To develop an intelligent chatbot system that supports multilingual interaction through automatic language detection and AI-based response generation.

The system aims to:

* Enable communication across multiple languages.
* Automatically detect user language.
* Generate real-time responses.
* Store and manage conversation history.
* Improve accessibility and user experience.
* Support NLP-based query understanding.
* Provide centralized chatbot management.
* Build historical conversation data for analytics.

---

## Problem Statement

Many chatbot systems require users to manually select their preferred language and often struggle to provide accurate multilingual responses.

This creates:

* Communication barriers.
* Limited multilingual support.
* Poor user experience.
* Inconsistent response quality.
* Difficulty in handling multiple language inputs.
* Lack of conversation tracking.

This project solves these challenges by providing an AI-powered Language Agnostic Chatbot capable of understanding and responding across multiple languages.

---

## User & Module Identification

The Language Agnostic Chatbot platform allows users to interact through a chatbot interface while administrators manage language configurations and analytics.

---

## Modules List

* User Management Module
* Language Detection Module
* Translation Management Module
* Chat Processing Module
* NLP Processing Module
* Response Generation Module
* Conversation History Module
* Authentication & Access Control Module

---

## Database Requirement Analysis

The Language Agnostic Chatbot requires a centralized database to manage users, conversations, language processing, translations, chatbot responses, and historical chat records.

---

## Table List

| Table Name           | Description                  |
| -------------------- | ---------------------------- |
| Users                | Stores user information      |
| Chats                | Stores chat conversations    |
| Languages            | Stores supported languages   |
| Translations         | Stores translated messages   |
| NLP_Processing       | Stores NLP analysis          |
| Responses            | Stores chatbot responses     |
| Conversation_History | Stores previous chat records |
| Audit_Logs           | Stores system activity logs  |

---

%% ═══════════════════════════════════════════════════
%% CORE USERS & CHAT SESSIONS
%% ═══════════════════════════════════════════════════

USERS {
    uuid        id              PK
    varchar     name
    varchar     email           UK
    varchar     phone           UK
    enum        role
    boolean     is_active
    timestamptz created_at
}

CHAT_SESSIONS {
    uuid        id              PK
    uuid        user_id         FK
    varchar     detected_lang
    varchar     preferred_lang
    timestamptz started_at
    timestamptz ended_at
}

MESSAGES {
    uuid        id              PK
    uuid        session_id      FK
    uuid        sender_id       FK
    text        original_text
    text        translated_text
    varchar     language
    enum        message_type    %% user / bot
    timestamptz created_at
}

%% ═══════════════════════════════════════════════════
%% LANGUAGE PROCESSING LAYER
%% ═══════════════════════════════════════════════════

LANGUAGE_DETECTION {
    uuid        id              PK
    uuid        message_id      FK
    varchar     detected_lang
    float       confidence_score
    timestamptz created_at
}

TRANSLATIONS {
    uuid        id              PK
    uuid        message_id      FK
    varchar     source_lang
    varchar     target_lang
    text        translated_text
    varchar     engine_used
    timestamptz created_at
}

INTENTS {
    uuid        id              PK
    varchar     name
    text        description
}

MESSAGE_INTENTS {
    uuid        id              PK
    uuid        message_id      FK
    uuid        intent_id       FK
    float       confidence_score
}

%% ═══════════════════════════════════════════════════
%% NLP & RESPONSE GENERATION
%% ═══════════════════════════════════════════════════

NLP_ANALYSIS {
    uuid        id              PK
    uuid        message_id      FK
    text        entities_json
    text        sentiment
    text        keywords
    timestamptz created_at
}

BOT_RESPONSES {
    uuid        id              PK
    uuid        session_id      FK
    uuid        message_id      FK
    text        response_text
    varchar     response_lang
    enum        response_type   %% text / image / mixed
    timestamptz created_at
}

AI_MODELS {
    uuid        id              PK
    varchar     name
    varchar     version
    text        description
    boolean     is_active
}

RESPONSE_MODEL_USAGE {
    uuid        id              PK
    uuid        response_id     FK
    uuid        model_id        FK
    float       latency_ms
    float       confidence
}

%% ═══════════════════════════════════════════════════
%% FEEDBACK & IMPROVEMENT
%% ═══════════════════════════════════════════════════

FEEDBACK {
    uuid        id              PK
    uuid        message_id      FK
    uuid        user_id         FK
    int         rating
    text        comments
    timestamptz created_at
}

CONVERSATION_SUMMARY {
    uuid        id              PK
    uuid        session_id      FK
    text        summary_text
    varchar     summary_lang
    timestamptz created_at
}

%% ═══════════════════════════════════════════════════
%% RELATIONSHIPS
%% ═══════════════════════════════════════════════════

USERS           ||--o{ CHAT_SESSIONS         : starts
CHAT_SESSIONS   ||--o{ MESSAGES              : contains
USERS           ||--o{ MESSAGES              : sends

MESSAGES        ||--o{ LANGUAGE_DETECTION    : analyzed_by
MESSAGES        ||--o{ TRANSLATIONS          : translated_to
MESSAGES        ||--o{ MESSAGE_INTENTS       : has
INTENTS         ||--o{ MESSAGE_INTENTS       : classifies

MESSAGES        ||--o{ NLP_ANALYSIS          : processed_by
CHAT_SESSIONS   ||--o{ BOT_RESPONSES         : generates
MESSAGES        ||--o{ BOT_RESPONSES         : replies_to

AI_MODELS       ||--o{ RESPONSE_MODEL_USAGE  : powers
BOT_RESPONSES   ||--o{ RESPONSE_MODEL_USAGE  : generated_with

USERS           ||--o{ FEEDBACK              : gives
MESSAGES        ||--o{ FEEDBACK              : receives

CHAT_SESSIONS   ||--o{ CONVERSATION_SUMMARY  : summarized_as

