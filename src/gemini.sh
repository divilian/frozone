#!/bin/bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AIzaSyB0qlsLPrPGLvnRbF46j692AnXb2GkJ03A' \
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
