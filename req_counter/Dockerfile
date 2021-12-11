FROM node:17-alpine

WORKDIR /app
COPY . /app/

RUN yarn install

CMD [ "yarn", "run", "server", "0.0.0.0", "8000"]