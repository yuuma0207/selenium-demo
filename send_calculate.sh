#!/bin/bash
curl -X POST http://127.0.0.1:5123/calculate -H "Content-Type: application/json" -d '{"numbers": [1,2,3,4,5]}'