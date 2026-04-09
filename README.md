---
title: Email Triage Env
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---
Here is the clean, emoji-free version of your README ready to be copy-pasted:

Bilingual Email Triage Environment (English & Hinglish)
Built for the Meta x SST PyTorch Hackathon.

Overview
This is an OpenEnv reinforcement learning environment that simulates a customer support email triage system. To make this relevant to the Indian tech ecosystem and properly test modern LLMs, this environment features a Bilingual (English and Hinglish) synthetic dataset.

The Task
The agent receives an inbound customer email (Observation) and must act as a routing system, predicting the correct category (urgent, billing, spam, support, info) and priority (high, medium, low).

Reward Function
+1.0: Perfect routing (correct category AND correct priority).

+0.5: Partial success (correct category OR correct priority).

-1.0: Incorrect classification.

## Tasks

This environment consists of three sequential decision-making tasks:

1. Email Analysis
2. Category Classification
3. Priority Assignment and Resolution