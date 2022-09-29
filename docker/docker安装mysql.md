查看mysql可用版本

```shell
docker search mysql
```

![image-20220929214307857](https://raw.githubusercontent.com/start-point/typora/master/Typora202209292143986.png)



安装mysql镜像

```shell
docker pull mysql
```

![image-20220929214449967](https://raw.githubusercontent.com/start-point/typora/master/Typora202209292144013.png)

查看镜像（是否安装成功）

```shel
docker images
```

![image-20220929214543783](https://raw.githubusercontent.com/start-point/typora/master/Typora202209292145811.png)



运行mysql

> --name mysql-3306 是取别名后面启动mysql 关闭都可以用这个名字，也可以用自动生成的id

```shell
docker run -itd --name mysql-3306 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

![image-20220929214746690](C:\Users\48676\AppData\Roaming\Typora\typora-user-images\image-20220929214746690.png)



查看是否运行成功

```shell
docker ps
```

![image-20220929214835032](https://raw.githubusercontent.com/start-point/typora/master/Typora202209292148061.png)





进入mysql容器

```shell
#进入mysql容器
docker exec -it mysql-3306 bash

#进入mysql  然后输入刚刚的密码 123456
mysql -u root -p   
```

![image-20220929215142521](https://raw.githubusercontent.com/start-point/typora/master/Typora202209292151557.png)
