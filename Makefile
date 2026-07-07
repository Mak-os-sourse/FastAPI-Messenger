docker:
	sudo systemctl start docker
	sudo docker-compose up -d
	sudo docker-compose -f docker-compose-test.yml up -d