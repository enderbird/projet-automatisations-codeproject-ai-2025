FROM node:20-slim

WORKDIR /app

COPY application/package*.json ./
RUN npm install

COPY application/ .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]