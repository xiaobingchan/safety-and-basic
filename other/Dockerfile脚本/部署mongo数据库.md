docker pull mongo

mkdir -p /docker/mongo_data

docker run -p 27017:27017 -v /docker/mongo_data:/data/db --name docker_mongodb -d mongo

