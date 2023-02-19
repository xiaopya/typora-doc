

百度文库爬虫  Baidu Wenku Spider

仅支持python3

## 郑重声明

请勿将该脚本用于下载付费文档或商业用途，否则后果自负！
本项目仅为方便查看在线文档和交流爬虫技术。

## 使用教程

目前该项目支持所有格式文档下载。

ppt仅能保存图片格式的pdf，建议下载后通过Acrobot等光学识别软件拷贝文字；

doc、pdf文件仅能保存为pdf，且可能看起来会有一些不同；

xls文件仅能保存为pdf，未来可能会支持保存为xls；

txt可保存为原始格式。

如果需要提取图片或查看原始数据，可以带参数`-t`保存临时文件。

原理为下载网页中显示的内容，而并非原始文档，只能尽力还原格式。

目前来看，大部分普通账户可能无法查看完整文档，但通过该项目却可以完整下载，猜测是仅仅在前端做了限制，不排除未来百度文库修复该漏洞。

### 安装


下载源码并安装依赖

```powershell
pip install -r requirements.txt
python main.py --help
```


### 进阶用法

#### -h, --help

显示帮助信息并退出。

#### -c COOKIES, --cookies COOKIES

传入cookie格式字符串，使请求带cookie。

#### -C COOKIES_FILENAME, --cookies_filename COOKIES_FILENAME

传入cookie文件，使请求带cookie。优先级低于前者。

#### -t, --temp

将临时文件保存到文件夹。

#### -o OUTPUT, --output OUTPUT

指定文件名（后缀名自动生成）

#### -p PAGENUMS, --pagenums PAGENUMS

指定下载和保存的页数，例如"2,6-8,10"代表下载页码"2,6,7,8,10"，从"1"开始。

#### -u USERAGENT, --useragent USERAGENT

指定请求时User-Agent。

#### -F FILENAME, --filename FILENAME

批量下载。传入文件名，文件中一行一个链接。

例如：
python main.py -C  I:\python\wks-main\cookies  https://wenku.baidu.com/view/291a3ff982d049649b6648d7c1c708a1284a0ad9.html