#! /bin/bash

kill_containers() {
        for c in `docker ps --quiet | cut -w -f 1`
        do
                docker container kill $c
        done
}

kill_images() {
        for image in `docker image ls --quiet | cut -w -f 1`
        do
                docker image rm -f $image
        done
}

die_docker_die() {
        kill_containers
        kill_images
        docker system prune --all --force --volumes
}

alias 'ddd!'="die_docker_die"