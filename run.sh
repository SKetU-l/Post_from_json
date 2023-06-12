#!/bin/bash
exec gunicorn app:app && nohup python3 bot.py
