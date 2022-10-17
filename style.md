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





#### 抖动提醒

```css
@keyframes shake {
  10%, 90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%, 80% {
    transform: translate3d(2px, 0, 0);
  }

  30%, 50%, 70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%, 60% {
    transform: translate3d(4px, 0, 0);
  }
}

// 抖动
.apply-shake {
  animation: shake 0.82s cubic-bezier(.36, .07, .19, .97) both;
}
```

