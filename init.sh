#!/bin/bash
echo '开始下载anaconda，版本Anaconda3-2020.07-Linux-x86_64 ...'
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh

echo '安装anaconda环境 ...'

bash Anaconda3-2020.07-Linux-x86_64.sh
echo 'export PATH=$PATH:/root/anaconda3/bin'>>/root/.bashrc

source /root/.bashrc

echo 'conda 安装完毕，执行依赖环境初始化操作...'

conda env create --file dubhe_visual.yaml

echo 'conda dubhe_visual虚拟环境初始化成功，进入环境并执行数据初始化操作...'

source activate dubhe_visual

cd backend/
python manage.py migrate

echo '数据库初始化成功，启动服务请执行：source start_server.sh'

