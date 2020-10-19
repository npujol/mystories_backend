FROM node:lts-alpine
# WORKDIR ../frontend/mystories/
# RUN npm install --global yarn

# copy both 'package.json' and 'package-lock.json' (if available)
COPY frontend/mystories/package.json frontend/mystories/yarn.lock ./

# install project dependencies
RUN yarn install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY frontend/mystories/ .

# build app for production with minification
RUN yarn build

FROM nginx:1.19.0-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
COPY --from=0 ./dist /dist
