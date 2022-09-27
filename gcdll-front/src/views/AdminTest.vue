<template>
<div id="admin-test">
    <el-container v-if="page_width>768" style="justify-content: space-between;">
        
            <el-menu class="aside-nav" v-on:select="sidebar_select" 
            default-active="photo" :unique-opened="true"
            background-color="#545c64" text-color="#fff"
            :collapse="isCollapse"
            >
                <el-menu-item index="null" class="collapse-button" v-if="isCollapse==false" @click="isCollapse=true">
                    <i class="el-icon-d-arrow-left"></i>
                    <span slot="title">缩进</span>
                    
                </el-menu-item>
                <el-menu-item index="null" class="collapse-button" v-else @click="isCollapse=false">
                    <i class="el-icon-d-arrow-right"></i>
                </el-menu-item>
                <el-submenu index="photo">
                    <template slot="title">
                        <i class="el-icon-picture"></i>
                        <span>照片管理</span>
                    </template>
                    <el-menu-item-group>
                        <el-menu-item index="photo">
                            <i class="el-icon-s-open"></i>
                            <span slot="title">修复照片</span>
                        </el-menu-item>
                        <el-menu-item index="editphoto">
                            <i class="el-icon-edit"></i>
                            <span slot="title">照片信息</span>
                        </el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-submenu index="exhibit">
                    <template slot="title">
                        <i class="el-icon-files"></i>
                        <span>展览管理</span>
                    </template>
                    <el-menu-item-group>
                        <el-menu-item index="gallery">
                            <i class="el-icon-postcard"></i>
                            添加展览
                        </el-menu-item>
                        <el-menu-item index="editgellery">
                            <i class="el-icon-edit"></i>
                            <span slot="title">编辑展览</span>
                        </el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-menu-item index="user">
                    <i class="el-icon-user"></i>
                    <span slot="title">用户管理</span></el-menu-item>
                <el-menu-item index="dealcomment">
                    <i class="el-icon-s-order"></i>
                    <span slot="title">评论管理</span></el-menu-item>
                
                <el-submenu index="examin">
                    <template slot="title">
                        <i class="el-icon-view"></i>
                        <span>查看</span>
                    </template>
                    <el-menu-item-group>
                        <el-menu-item index="past">
                            <i class="el-icon-date"></i>
                            查看所有照片</el-menu-item>
                        <el-menu-item index="gallerylist">
                            <i class="el-icon-document-copy"></i>
                            查看所有展览</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                
            </el-menu>
      
        <el-main id="admin-main" :style="main_margin">
            <router-view/>
        </el-main>
    </el-container>
    <el-result v-else icon="warning" title="警告:屏幕范围过小" subTitle="请横屏或在电脑端进行操作">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="go_to_home">返回主页</el-button>
      </template>
    </el-result>
</div>
</template>
<script>
// import PhotoAdmin from "@/components/PhotoAdmin.vue"
// import UserAdmin from "@/components/UserAdmin.vue"
export default {
    name: "AdminTest",
    components: {
        // PhotoAdmin,
        // UserAdmin
    },
    props:{
        // 账户
        userstate:{
            type: Object,
            required: true
        },
        page_width:{
            type: Number,
            required: true
        }
    },
    data(){
        return{
            isCollapse:false
        }
    },
    methods: {
        go_to_home(){
            this.$router.push('/')
        },
        sidebar_select(key) {
            if(key=='null')
                return
            this.$router.replace({path: `/admin/${key}`})
        },
        
    },
    computed:{
        main_margin:function(){
            if(this.isCollapse)
            {
                return{
                    'margin-left':'100px'
                }
            }
            else
            {
                return{
                    'margin-left':'300px'
                }
            }
        }
    },
    created(){
        const my_this = this
        if(my_this.userstate.type!='admin')
            {
                my_this.$message.error('非管理员禁止访问')
                my_this.$router.push('/')
                return
            }
        var timer = setInterval(
            function(){
            if(my_this.userstate.type!='admin')
            {
                my_this.$message.error('非管理员禁止访问')
                my_this.$router.push('/')
                clearInterval(timer)
            }
        }, 2000)// 直接进行检查即可
    }
}
</script>
<style>
    .aside-nav:not(.el-menu--collapse) {
        width: 300px;
        min-height: 400px;
    }
    .aside-nav {
        position: fixed;
        left: 0px;
        height: 100%;
        background-color:#545c64;
        z-index:100;
    }
    #admin-main {
        margin-top: 0px;
        margin-left: 100px;
        transition: 0.5s;
        padding: 10px;
    }
    .el-menu-item {
        text-align: center;
    }
</style>