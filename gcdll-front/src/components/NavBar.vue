<template>
    <div id="outline" :style="'width:'+(page_width-30)+'px'">
        <div class="header-bar">
            <el-row>
                <el-col :span="4" style="padding-top: 10px" :xs="{span:6}">
                    <b id="title">
                        AI Repair
                    </b>
                </el-col>
                <el-col :span="6" :xs="{span:7}">
            <div class="jump-button">
                <el-tooltip content="返回上一级" placement="top" effect="dark">
                    <el-button type="text" @click="go_to_last_page">
                        <i class="el-icon-back big-icon">
                        </i>
                    </el-button>
                </el-tooltip>
                <el-tooltip content="主页" placement="top" effect="dark">
                    <el-button type="text" @click="go_to_home">
                        <a-icon type="home" class="big-icon" style="color: white"/>
                    </el-button>
                </el-tooltip>
                <el-tooltip content="管理主页" placement="top" effect="dark" v-if="state.type=='admin'">
                    <el-button type="text" @click="go_to_admin">
                        <i class="el-icon-setting big-icon">
                        </i>
                    </el-button>
                </el-tooltip>
            </div>
                </el-col>
                
                <el-col v-if="page_width > 768" :span="8" style="padding-top: 15px" :xs="{span:16}">
                    <search-bar v-if="$route.name!='search'" :change_scope="change_scope" :scope="scope">
                    </search-bar>
                    <div class="search-bar-placer" v-else>
                    </div>
                </el-col>
                <el-col v-else :span="2">
                    <el-tooltip content="搜索" placement="top" effect="dark">
                        <el-button type="text" @click="$router.push({name:'search'})">
                            <i class="el-icon-search big-icon">
                            </i>
                        </el-button>
                    </el-tooltip>
                </el-col>
                <el-col :span="6" style="padding-top: 15px" :xs="{span:8}">
            <div class="login-button" style="float:right">
                <el-button @click="open_drawer" v-if="state.user_valid" type="success">
                    <el-tooltip content="个人中心" placement="top" effect="dark">
                        <i class="el-icon-user">
                            <span >{{state.username}}</span>
                        </i>
                    </el-tooltip>
                </el-button>
                <el-button @click="open_login('login')" v-else type="success">
                    <i class="el-icon-user">
                    <span >登陆/注册</span>
                    </i>
                </el-button> 
            </div>
                </el-col>
            </el-row>
            
            
            
            
            
        </div>
        
    </div>
    
</template>

<script>
import SearchBar from './SearchBar.vue'
// import VALUE from '@/utils/const'
export default {
    name: "NavBar",
    components: {
        SearchBar
        // Login
    },
    props: {
        page_width:{
            type:Number,
            required:true,
        },
        state:{
            type: Object,
            required: true
        },
        // 提醒
        get_alert:{
            type: Function,
            required: true
        },
        // 侧边栏
        open_drawer:{
            type: Function,
            required: true
        },
        // 登陆框
        open_login:{
            type: Function,
            required: true
        }
    },
    data() {
        return {
            scope: 'photo',
        }
    },
    methods: {
        change_scope(new_scope){
            this.scope = new_scope
        },
        go_to_admin: function(){
            this.$router.push({path:'/admin/photo'})
        },

        go_to_home: function(){
            this.$router.push({path:'/'})
        },

        go_to_last_page: function(){
            this.$router.back(-1)
        },

        send: function() {
            console.log('search ' + this.keyword)
        },
    },
    computed:{
    }
}
</script>

<style>
    @media screen and (max-width: 1200px) {
        #outline{
            width:1200px;
            overflow-x: hidden;
        }
    }

    @media screen and (max-width: 768px) {
        #outline{
            width:100%;
            overflow-x: hidden;
        }
    }

    #outline {
        border-bottom-style: hidden; 
        border-width: 1px; 
        height: 100%;
    }
    #title {
        color: white;
        font-size: 200%;
    }
    .header-bar {
        min-height: 75px;
        width: 100%;
        margin:auto;
    }
    #outline .search-bar {
        align-self:flex-end;
        margin-bottom: 5px;
        float: right;
        margin-right: 20px;
    }
    .search-bar-placer{
        width: 40%;
        align-self:flex-end;
        margin-bottom: 5px;
        float: right;
        margin-right: 20px;
    }
    .login-button {
        align-self:flex-end;
        /* margin-right: 20px; */
        margin-bottom: 5px;
        /* z-index: 5; */
    }
    .jump-button {
        width: 50%;
        display: flex;
        align-self:flex-end;
        margin-right: 20px;
        margin-bottom: 5px;
        font-size:30px;
    }
    .big-icon{
        font-size: 40px;
        color: white
    }
    @media screen and (max-width: 768px) {
        .big-icon{
            font-size: 30px;
            color: white
        }
    }
</style>