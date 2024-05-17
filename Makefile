

dockerfile:
    docker build -t 32healthtest .

run-docker: dockerfile
    docker run -d --name 332healthcontainer -p 80:80 32heathtest
