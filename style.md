- *常用的style样式

------

### 超出的内容出现省略号

```JavaScript
.div{
  display: -webkit-box;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2; // 行数
  -webkit-box-orient: vertical;
}
```