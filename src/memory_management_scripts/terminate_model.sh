#!/bin/bash
pid="$(ps aux | grep sma_llm.main.my_main | grep -v grep | awk '{print $2}')"
kill "$pid"
