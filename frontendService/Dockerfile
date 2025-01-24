FROM node:18

ARG BUILD_NO_CACHE
WORKDIR /app

COPY package*.json ./
RUN if [ "$BUILD_NO_CACHE" = "true" ]; then npm install --no-cache; else npm install; fi


COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
