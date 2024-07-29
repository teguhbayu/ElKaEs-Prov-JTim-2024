#!/bin/bash
sudo -u ec2-user -i <<'EOF'
sudo yum update -y 
sudo yum install git nodejs -y
git clone https://github.com/handipradana/dash.git
cd /home/ec2-user/dash
npm i
echo 'PORT = 5000' > .env
echo 'API_URL = ""' >> .env
npm run prod
EOF