# 前端z-index

同一级的元素
设置了z-index：z-index越大，层级越高，越靠前
未设置z-index：DOM树中越靠后的元素层级越高，越靠前

不同级的元素
父元素设置了z-index：子元素始终在父元素上边，即使子元素的z-index小于父元素的z-index
父元素没有设置z-index：子元素设置负的z-index可位于父元素的下边，其余全位于父元素的上边

## 游客端
* （按由高到低顺序）
* 提醒条el-alert 1000001 
* 侧边栏el-drawer 10000
* Login窗口 3001
* Login窗口的cover 3000
* 其他element-ui自带的popup结构 2000+
    * 加载中标识loading
    * 提示信息tooltip
* 弹出评论区 ExhibitPage.exhibit-comment 2002/ cover 2001
* 导航栏NavBar 2001
