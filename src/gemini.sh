#!/bin/bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: ${GEMINI_API_KEY}' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Put your prompt here"
          }
        ]
      }
    ]
  }'
