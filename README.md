First run Elastic search and Kibana using Docker-compose file:
`docker-compose up -d`

You can check the docker status by using:
`docker-compose ps`

To install requirements please run:
`pip install -r requirements.txt`

search keywords (Since the task is for search only, documenting it alone):
CURL request = `curl --location --request POST 'http://127.0.0.1:5000/search?keyword=$KEYWORD'`
