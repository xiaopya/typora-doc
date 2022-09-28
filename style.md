- *常用的style样式

------

### 超出的内容出现省略号

```css
.div{
  display: -webkit-box;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2; // 行数
  -webkit-box-orient: vertical;
}
```

#### 毛玻璃效果

```css
.div{
    backdrop-filter: blur(5px);
}
```



#### 页面平滑滚动

```css
.html{
    scroll-behavior: smooth;
}
```

