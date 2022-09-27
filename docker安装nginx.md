### 安装 Docker Engine-Community

#### 1. 使用 Docker 仓库进行安装

> 在新主机上首次安装 Docker Engine-Community 之前，需要设置 Docker 仓库。之后，您可以从仓库安装和更新 Docker

- 设置仓库

> 安装所需的软件包。yum-utils 提供了 yum-config-manager ，并且 device mapper 存储驱动程序需要 device-mapper-persistent-data 和 lvm2。

```PowerShell
sudo yum install -y yum-utils  device-mapper-persistent-data  lvm2
```

- 使用以下命令来设置稳定的仓库。

```PowerShell
 sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

#### 2. 安装 Docker Engine-Community

> 安装最新版本的 Docker Engine-Community 和 containerd，或者转到下一步安装特定版本 如果提示你是否接受密钥  选择是

```PowerShell
sudo yum install docker-ce docker-ce-cli containerd.io
```

#### 3. 启动docker

```PowerShell
sudo systemctl start docker
```

#### 4. 通过运行 hello-world 映像来验证是否正确安装了 Docker Engine-Community 。

```PowerShell
sudo docker run hello-worldv
```

### 安装nginx

#### **1. 查看官方仓库镜像**

```PowerShell
docker search nginx
```

![01](https://raw.githubusercontent.com/start-point/typora/master/Typora01.png)



#### 2. 拉取镜像

```PowerShell
docker pull nginx
```

![image](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage.png)



#### 3. 查看镜像

```PowerShell
docker images
```

![image-20220927225223720](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225223720.png)



#### 4. 启动nginx镜像

> 这里的 —name nginx 可要可不要 这是给nginx命名

```PowerShell
docker run -d -p 8080:80 --name nginx-8080 nginx
```

![image-20220927225235759](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225235759.png)

#### 5. 访问网页端口

> 公安网服务器ip加上8080 访问就可以得到

如果到这一步 六浏览器没有打开以下内容，就是你的服务器没有开放8080端口

我这里是阿里云 在安全组开发8080 端口即可

![image-20220927225250876](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225250876.png)

#### 6. nginx关闭/启动

```PowerShell
#关闭
docker stop nginx-8080    # 按照我的方法在上面给nginx命名了
docker stop id            # 这里是没有命名nginx 需要用docker ps 查看已经启动的镜像 拿到nginx的id 来关闭nginx

#启动
docker restart nginx-8080 # 这里也一样 没有命名 就需要去拿 nginx 的id
```

### **安装git 并拉取代码**

#### 安装

```PowerShell
yum install -y git

# 检查是否出现版本号  出现则安装成功
git version
```

#### git配置

```PowerShell
# 配置一个用于提交代码的用户，输入命令
git config --global user.name "Your Name"

#配置一个用户邮箱，输入命令
git config --global user.email "email@example.com"

#生成公钥和私钥，输入命令后一路回车即可
ssh-keygen -t rsa -C "youremail@example.com"

#查看公钥和私钥
cat /root/.ssh/id_rsa.pub
```

![image-20220927225305381](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225305381.png)

#### 一下就是密钥，复制它

![image-20220927225315877](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225315877.png)

#### 打开github

![image-20220927225327507](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225327507.png)

![image-20220927225343849](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225343849.png)

![image-20220927225358487](https://raw.githubusercontent.com/start-point/typora/master/Typoraimage-20220927225358487.png)

#### 然后就可以在服务器 拉取代码了

```PowerShell
git clone 项目地址
```

### CentOS安装nvm

- 可以通过[curl](https://so.csdn.net/so/search?q=curl&spm=1001.2101.3001.7020)或者wget进行安装，命令如下

```PowerShell
#curl

curl -o- [https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh](https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh) | bash

#wget

wget -qO- [https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh](https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh) | bash
```

安装完后，如果是用xshell连远程主机的话，先重连一次，不然会发现提示找不到nvm命令

可能出现依旧提示找不到nvm命令，那么请使用source命令，如下

```PowerShell
source ~/.bashrc

#如果是zsh的话

source ~/.zshrc
```

到这里执行 nvm 看看是否安装成功

安装yarn

```PowerShell
npm install yarn -g
```

### 项目打包，部署上线

#### 正常git拉取项目下来，执行以下命令

```PowerShell
git clone ...  # 拉取远程仓库项目

yarn           # 安装项目包

yarn build     # 打包项目 会生成一个dist文件
```

#### 先把docker容器停掉

```PowerShell
docker ps    # 查看在运行的 nginx  依次停止


# 一定要在项目根目录下面执行命令  $PWD代表当前路径
docker run -d -p 8080:80 -v $PWD/dist:/usr/share/nginx/html nginx


docker ps    # 查看nginx是否启动
```

这时候再去访问项目ip 就可以成功访问到了

### 脚本简化部署命令

> 这时候在每次写代码都会去执行 关闭容器 pull代码 执行启动命令会很麻烦 在项目的根目录下创建一个 文件名 [start.sh](http://start.sh)

```PowerShell
# start.sh     启动命令 sh start.sh

git pull

yarn --registry=https://registry.npm.taobao.org/ && yarn build

#删除容器
docker rm -f xiaopy &> /dev/null

#启动容器
docker run -d --restart=on-failure:5\
    -p 8080:80 \
    -v $PWD/dist:/usr/share/nginx/html \
    --name xiaopy nginx
```