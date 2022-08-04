# base image를 ubuntu 18.04로 설정합니다.
FROM ubuntu:18.04

# apt-get update 명령을 실행합니다.
RUN apt-get update

# DOCKER CONTAINER가 시작될 때 "Hello FastCampus"를 출력합니다.
CMD ["echo", "Hello FastCampus"]
