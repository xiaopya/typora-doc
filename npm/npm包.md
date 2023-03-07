- 常用的npm包

------

### qs 序列化数据

```JavaScript
import qs from 'qs';
 
let obj = {	
    a: 'aaa',
    b: 'bbb',
    c: 'ccc',
  };
  
  console.log(qs.stringify(obj)); // a=aaa&b=bbb&c=ccc
 
  let arr = [1, 2];
  console.log(qs.stringify({ bb: arr })); // 'bb[0]=1&bb[1]=2'
 
  let url = 'age=18&name='xz';
  console.log(qs.parse(url)); // {age: 18, name: xz}
```

### rimraf  同rm -rf

```PowerShell
$ npm install rimraf -g // 全局安装

$ rimraf node_modules
```

### jsonwebtoken

```JavaScript
/* 
 * jsonwebtoken 封装 
 * 以下例子 用的是 koa2 框架
 */
const jwt = require('jsonwebtoken');

// code 唯一标识
class JWT {

    // code 标识 可以是任意字符 
    static obtain(body, time, code) {
        const { username, password } = body;
        const token = jwt.sign({
            username,
            password,
            iat: Date.now(),
            exp: Date.now() + time,
        }, code);
        return token;
    }

    static inspection(authorization, code) {
        /**
         * iat 发布时间
         * exp 到期时间
         */
        const { iat, exp } = jwt.verify(authorization, code);
        return {
            iat,
            exp
        }
    }
}
module.exports = {
    JWT
}



// 例子
const db = require('../utils/db');
const { JWT } = require('../utils/jwt');
const fs = require("fs");  // 引入fs模块

class userController {
    /**
     * 用户登录
     */
    static async Login(ctx) {
        const { username, password } = ctx.request.body;
        let sql = `select * from user where username=(?)`;
        let data = await new Promise((rev, rej) => {
            db.query(sql, [username], (err, data) => {
                if (err) rej(err);
                rev(data);
            })
        })
        if (!data.length) {
            // 如果data.length 为 [] 数据库不存在该数据 提示他 去注册 或者说没有该账号
            ctx.body = {
                msg: "该账号尚未注册",
                status: 'error',
                type: 'account',
            }
        } else {
            // 判断 数据库里存储的 密码 与传进来的密码 是否一样
            if (data[0].password === password) {
                // 生成token 令牌    5小时的 token 时间
                const token = JWT.obtain(ctx.request.body, 18000000, 'cyl');
                ctx.body = {
                    msg: '登录成功',
                    code: 200,
                    status: 'ok',
                    data: {
                        token,
                        username: data[0].username,
                    }
                }
            } else {
                ctx.body = {
                    msg: '账号或密码错误',
                    status: 'error',
                }
            }
        }
    }

    // token校验
    static async checkToken(ctx, next) {
        const { authorization } = ctx.request.headers;
        const time = new Date().getTime();
        const { exp } = JWT.inspection(authorization, 'cyl');
        if (time <= exp) {
            await next();
            ctx.body = {
                msg: 'token 还在有效期',
            }
        } else {
            ctx.body = {
                msg: 'token 过期 请重新登录',
                code: 200,
            }
            ctx.status = 401;
        }
    }
}

module.exports = {
    userController
}
```

### node mysql封装

```JavaScript
// 引入mysql
const mysql = require("mysql");

// 创建连接池
const pool = mysql.createPool({
    host: "localhost",  // 连接的服务器(代码托管到线上后，需改为内网IP，而非外网)
    port: 3306, // mysql服务运行的端口
    database: "admin_cms", // 选择某个数据库
    user: "root",   // 用户名
    password: "123456", // 用户密码
})


//对数据库进行增删改查操作的基础
const query = function (sql, options, callback) {
    pool.getConnection(function (err, conn) {
        if (err) callback(err, null, null);
        else {
            conn.query(sql, options, function (err, results) {
                //释放连接  
                conn.release();
                //事件驱动回调  
                callback(err, results);
            });
        }
    });
}

module.exports = {
    query
}
```

### require-directory 批量注册路由

```JavaScript
/**
 *  批量注册路由
 */
const requireDirectory = require('require-directory');
// 获取当前目录  （什么文件调用 取决于什么目录）
const currentDir = process.cwd();
// router 是路由文件夹名称
const path = `${currentDir}/router`

class Init {
    static init(app) {
        requireDirectory(module, path, {
            visit: visitor,
        })
        function visitor(obj) {
            // 配置根目录
            obj.prefix('/api');


            /**
             * 用中间件启动路由
             * router.routes() 启动路由
             * router.allowedMethods() 允许任何请求
             */
            app.use(obj.routes(), obj.allowedMethods());
        }
    }
}
module.exports = {
    Init
};

// 用法
// 在 node项目中 app.js 文件里 引入该文件 调用 Init.init(app)  把app当成参数传入进去

const Koa = require('koa2');
const app = new Koa();
const { Init } = require('./core/init');

// 批量注册路由
Init.init(app);

// 监听端口
app.listen(port, () => {
    console.log(`server is running at http://localhost:${port}`)
})
```