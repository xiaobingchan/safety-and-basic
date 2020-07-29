FROM mhart/alpine-node
LABEL maintainer = "lmjben <yinhengliben@gmail.com>"

RUN rm -rf /apps
RUN mkdir /app
WORKDIR /app

COPY . /app
RUN npm install
RUN npm run build
RUN mv ./dist/* ./

EXPOSE 8082

CMD BUILD_ENV=docker node app.js
