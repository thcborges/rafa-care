FROM node:lts-alpine
ARG UNAME=app
ARG UID=1000
ARG GID=1000

# Create user
ENV HOME=/home/$UNAME
RUN deluser --remove-home node && adduser -g $GID -u $UID -D $UNAME
RUN chown -R $UNAME $HOME
USER $UNAME

RUN mkdir -p $HOME/app
WORKDIR $HOME/app

COPY ./rafa-care-front/package*.json  .

RUN npm install

COPY rafa-care-front .

EXPOSE 3000
CMD yarn dev -H 0.0.0.0