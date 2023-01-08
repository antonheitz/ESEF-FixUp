#!/bin/bash

case "$1" in
    "dev")
        echo "Running in dev mode..."
        python3 main.py
        ;;
    # build
    "build")
        echo "building images..."
        docker-compose build
        echo "build complete"
        ;;
    # start
    "start")
        echo "starting containers..."
        docker-compose --compatibility up -d
        ;;
    # start
    "start-dev")
        echo "starting containers [dev]..."
        docker-compose --compatibility up 
        ;;
    # stop
    "stop")
        echo "stopping containers..."
        docker-compose --compatibility stop
        ;;
    # cleanup
    "cleanup")
        echo "removing containers..."
        docker-compose --compatibility down 
        ;;
    *)
        echo "Please provide a valid command: build | start | stop "
        ;;
esac