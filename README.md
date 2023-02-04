# sms-2-openai
Interact with Open AI's GPT-3 and DALL-E models via sms.



Instructions for building and saving the image and sending it to a remote host to load.

```
docker build -f dev/Dockerfile -t sms2openai:xx.yy.zz app
docker image save --output sms2openai.tar sms2openai:xx.yy.zz
scp sms2openai.tar root@$REMOTE_ADDRESS:/usr/src/app
```
