# Register Sponsor

While living in the Netherlands, I needed to find tech companies that sponsor 
work visas — but most don't include their industry in their registered name.
Built a tool to solve that.

## What it does

Scrapes the official Dutch visa sponsor registry, enriches each company with 
their commercial sector (translated from Dutch to English via a HuggingFace 
Transformer), and fetches their LinkedIn profile URL via Google API.

Users can filter by industry and reach each company's job listings in one click.

## The problem it solved

The public registry lists company names and registration numbers — nothing else.
Getting from "Acme BV" to "software company hiring engineers" required:

1. Cross-referencing the KVK (Dutch business registry) for sector data
2. Translating sector names from Dutch to English
3. Mapping each company to their LinkedIn presence

All automated with Python.

## Stack

Python · HuggingFace Transformers · Google API · SQLite

## Status

Core pipeline complete. LinkedIn URL fetching partially done — 
Google API daily quota limits the batch size.
