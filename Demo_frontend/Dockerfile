FROM node:16

WORKDIR Demo_frontend

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

ENTRYPOINT npm run start
