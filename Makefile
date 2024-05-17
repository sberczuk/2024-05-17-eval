

dockerfile:requirements
	docker build -t claims_processor .


run-docker:
	docker run -d --name claim_process_container  -p 80:80 claims_processor


requirements:
	pip3 freeze > requirements.txt

