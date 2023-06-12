#!/bin/bash
apt install ffmpeg -y && gunicorn app:app && python3 bot.py
