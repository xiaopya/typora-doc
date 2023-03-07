#### 搭建react脚手架

- 初始化生成`package.json`文件：

```powershell
npm init -y
```

- 安装需要的依赖包：

```powershell
# react react-dom在写react组件时需要引用
npm i react react-dom -D

# webpack webpack-cli做webpack配置时使用
npm i webpack webpack-cli -D

# 安装开发服务器，在开发模式下启动本地服务
npm i webpack-dev-server -D

# babel-loader用于转译js文件 
# @babel/core是babel的核心库，必须安装
# @babel-preset-env是一个只能预设，用于编译js高级语法
npm i babel-loader @babel/core @babel/preset-env -D

# 为了编译react中的语法
npm i @babel/preset-react -D

# 开发模式下，我们需要在html模板里查看组件样式
# 它会把html文件打包，自动引入css样式和js代码
npm i html-webpack-plugin -D

# 生产模式下，需要把css文件独立打包
npm i mini-css-extract-plugin -D

# 压缩css代码
npm i css-minimizer-webpack-plugin -D

# style-loader会把css样式插入到html中
# css-loader会把import引入的css文件编译成css代码
npm i style-loader css-loader -D

```

- 搭建脚手架，这里需要把开发和生产环境分开
- 开发环境
  - `webpack.dev.js`

```js
const path = require("path");
const htmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    mode: "development",
    entry: "./src/index.js",
    module: {
        rules: [
            // 处理css
            {
                test: /\.css$/,
                use:["style-loader","css-loader"]
            },
            // 处理js和jsx
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: "babel-loader"
            }
        ]
    },
    plugins: [
        new htmlWebpackPlugin({
            // 开发模式下打包html时候，以index.html为模板
            template: path.resolve(__dirname,"public/index.html")
        })
    ],
    // 配置开发模式的source-map，便于调试代码，定位bug
    devtool: "cheap-module-source-map",
    // 配置开发服务器
    devServer: {
        port: 3001,
        open: true
    },
    resolve: {
        // 自动补充扩展名，引入的时候就可以省略文件后缀
        extensions: [".js",".jsx",".json"]
    },
    // externals 用来定义哪些通过import引入的包不要被打包到boundle中
    // 也就是说，我们在写组件时引入的react和react-dom，不要打包
    externals: {
        react:{
            root: "React",
            commonjs2: "react",
            commonjs: "react",
            amd: "react",
        },
        "react-dom":{
            root: "ReactDom",
            commonjs2: "react-dom",
            commonjs: "react-dom",
            amd: "react-dom"
        }
    }
}
```

- 生产环境
  - `webpack.prod.js`

```js
const path = require("path");
const miniCssExtractPlugin = require("mini-css-extract-plugin");
const cssMinimizerPlugin = require("css-minimizer-webpack-plugin");


module.exports = {
    mode: "production",
    entry: "./src/index.js",
    output: {
        // 打包到lib目录下
        path: path.resolve(__dirname,'lib'),
        filename: "index.js",
        // 每次打包时，都自动清楚原有的打包文件
        clean: true,
        // 发布到npm库的相关信息
        // name是发布到npm时的库名，别人安装就是安装它
        // type是暴露库的形式，umd就表示别人可以在所有模块定义下引入这个库
        // 比如CommonJs AMD 和全局变量的形式
        // export用来指定哪一个导出应该被暴露为一个库
        // default就是我们默认导出的库
        library: {
            name: 'xpy-markdown',
            type: 'umd',
            export: 'default'
        },

    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    miniCssExtractPlugin.loader,
                    'css-loader'
                ]
            },
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            }
        ]
    },
    plugins: [
        new miniCssExtractPlugin({
            // 因为我们在文件中引入就是publicTest.css
            // 所以在打包后，也用这个名字，以免引入失败
            filename: 'publicTest.css'
        })
    ],
    resolve: {
        // 支持.js .jsx .json文件引入时隐藏后缀
        extensions: ['.js', '.jsx', '.json']
    },
    // 压缩和优化的相关配置都写在optimization里
    optimization: {
        minimizer: [
            new cssMinimizerPlugin()
        ]
    },
    externals: {
        react: {
            root: 'React',
            commonjs2: 'react',
            commonjs: 'react',
            amd: 'react',
        },
        'react-dom': {
            root: 'ReactDOM',
            commonjs2: 'react-dom',
            commonjs: 'react-dom',
            amd: 'react-dom',
        }
    }
}
```

#### 配置`babel`

- 兼容使用`@babel/preset-env`
- 编译jsx语法 `@babel/preset-react`

```js
module.exports = {
  presets: [
    "@babel/preset-env",
    "@babel/preset-react"
  ]
}
```

#### 配置`package.json`

+ 文档参考：`https://juejin.cn/post/7145001740696289317`



```json
{
  "name": "xpy-markdown",
  "version": "1.0.0",
  "description": "...",
  "main": "lib/index.js", // 模块的出口文件
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "webpack serve --config webpack.dev.js", // 开发模式下启动 npm start
    "build": "webpack --config webpack.prod.js", // 生产模式下启动，打包项目 npm run build
    "pub": "npm run build && npm publish" // 在已经登陆npm后，执行npm run pub就会直接打包并发布到npm
  },
  "repository": {
    "type": "git",
    "url": "https://gitee.com/guozia007/pulish-react-test01.git"
  },
  "keywords": [
    "react",
    "react component",
    "practive"
  ],
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  },
  "files": [
    "lib"
  ],
  "author": "xiaopy",
  "license": "ISC",
  "devDependencies": {
    "@babel/core": "^7.21.0",
    "@babel/preset-env": "^7.20.2",
    "@babel/preset-react": "^7.18.6",
    "babel-loader": "^9.1.2",
    "css-loader": "^6.7.3",
    "css-minimizer-webpack-plugin": "^4.2.2",
    "html-webpack-plugin": "^5.5.0",
    "mini-css-extract-plugin": "^2.7.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "style-loader": "^3.3.1",
    "webpack": "^5.75.0",
    "webpack-cli": "^5.0.1",
    "webpack-dev-server": "^4.11.1"
  },
  "peerDependencies": {
    "react": ">=16.9.0",
    "react-dom": ">=16.9.0"
  },
  "browserslist": [
    "> 0.25%",
    "last 2 versions",
    "not dead"
  ]
}

```

#### 配置`.npmignore`

- 过滤上传的文件

```tex
node_modules
.DS_Store
*.log
```

好了