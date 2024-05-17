

dockerfile:
    docker build -t claim_process  .

run-docker: dockerfile
    docker run -d --name claim_process_container  -p 80:80 claim_process


requirements: requirements.txt
    pip3 freeze > requirements.txt
