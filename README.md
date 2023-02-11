# Text AI
Interact with Open AI's GPT-3 and DALL-E models via sms.



Instructions for building and saving the image and sending it to a remote host to load.

```
docker build -f dev/Dockerfile -t textai:xx.yy.zz app
docker image save --output textai.tar textai:xx.yy.zz
scp textai.tar root@$REMOTE_ADDRESS:/usr/src/app
docker image load -t textai.tar
```
