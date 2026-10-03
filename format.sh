#!/bin/bash
black src tests web
autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r src tests web
