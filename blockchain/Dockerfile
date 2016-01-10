FROM debian:jessie

RUN apt-get update && apt-get install -y curl nodejs
RUN curl -sL https://deb.nodesource.com/setup_5.x | bash -
RUN apt-get install -y nodejs
#RUN curl https://npmjs.org/install.sh | bash -
RUN npm install -g blockchain-wallet-service
CMD ["blockchain-wallet-service", "start", "-b", "0.0.0.0"]
EXPOSE 3000
