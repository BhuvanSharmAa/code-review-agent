# Multi-Agent Code Review System

An automated code review pipeline built with LangGraph, using parallel specialist agents for security, quality, and logic analysis.

## Architecture
- **Ingestion agent** — parses code diffs, detects language
- **Security agent** (Mistral-7B) — finds vulnerabilities, hardcoded secrets, injection risks
- **Quality agent** (Zephyr-7B) — checks style, complexity, naming
- **Logic agent** (Mistral-7B) — catches edge cases, null risks, wrong conditionals
- **Aggregator** — scores findings, feeds RAG store
- **Refinement agent** (CodeLlama-7B) — suggests fixes using past context via FAISS RAG

## LangGraph Patterns Used
- Sequential → ingestion
- Parallel → security + quality + logic via Send() API
- Conditional → route to refinement or final report
- Iterative → refinement loop capped at 3 iterations

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # add your tokens
python main.py --mode local
```

## Run on a real GitHub PR
```bash
python main.py --mode pr --owner <owner> --repo <repo> --pr <number>
```

## Tech Stack
LangGraph · LangSmith · FAISS · HuggingFace Inference API · GitHub Actions
