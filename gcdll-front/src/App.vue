<template>
  <div id="app" style="height:100%;">
    <!-- 侧边栏 -->
    <el-drawer v-if="state.user_valid==true"
            :visible.sync="drawer"
            title="个人中心"
            direction="rtl" 
            z-index="10000"
            :size="(width>768)?'30%':'50%'"
        >
            <el-menu
                class="el-menu-vertical"
            >
                <el-menu-item index="1" @click="open_center">
                    <i class="el-icon-user" ></i>
                    查看账号信息
                </el-menu-item>
                <el-menu-item index="3" @click="change_password">
                    <i class="el-icon-setting" ></i>
                    更改密码
                </el-menu-item>
                <el-menu-item index="4" @click="log_out">
                    <i class="el-icon-circle-close" ></i>
                    注销
                </el-menu-item>
                
            </el-menu>
    </el-drawer>
    <!-- 提醒窗口 -->
    <el-alert v-if="alert_visible" :title="alert_content" :type="alert_type" effect="dark" center show-icon/>
    <!-- 弹窗 -->
    <el-dialog
    title="用户详情"
    :visible.sync="center_dialog_visible"
    :width="(width>768)?'50%':'90%'">
        <user-center :state="state" :update="check_log_in" :visible="center_dialog_visible">
        </user-center>
    </el-dialog>
    <el-dialog
    title="我的动态"
    :visible.sync="comment_dialog_visible"
    :width="(width>768)?'50%':'90%'">
        <user-comment-center :state="state">
        </user-comment-center>
    </el-dialog>
    <el-container>
      <el-header id="header" :height="get_header_height()">
        <NavBar :page_width="width" :state="state" :open_login="open_login" :get_alert="get_alert" :open_drawer="open_drawer"/>
      </el-header>
      <el-main id="main" v-if="!url_error">
            <keep-alive include="SearchResultPage,AdminTest,UserHome" v-if="state_checked">
                <router-view :userstate="state" :openlogin="open_login" 
                :page_width="width" :url_error_report="url_error_report">
                </router-view>
            </keep-alive>
      </el-main>
      <el-main id="main" v-else>
          <el-empty description="404，您访问的页面不存在"></el-empty>
      </el-main>
    </el-container>
    <Login 
        :visible="login_visible" :page_width="width"
        :user_state="state" :set_account="set_account" :close_login="close_login"
        :get_alert="get_alert" :login_type="login_type">
    </Login>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import $ from 'jquery'
import Login from '@/views/Login.vue'
import NavBar from './components/NavBar.vue'
import UserCenter from './components/UserCenter.vue'
import UserCommentCenter from './components/UserCommentCenter.vue'
// import AdminTest from "./views/AdminTest.vue"
import {request_json} from './utils/communication'
import VALUE from './utils/const'
export default {
  name: 'App',
  components: {
    NavBar,
    Login,
    UserCenter,
    UserCommentCenter,
  },
  data(){
    return{
        url_error: false,
        // 窗口宽度
        width: null,

      // 侧边栏
      drawer: false,

      // 登陆框激活
      login_visible: false,
      login_type: 'login',

      // 提醒窗口
      alert_visible: false,
      alert_type: 'success',
      alert_content: '成功',

      center_dialog_visible: false,
      comment_dialog_visible: false,
    
        state_checked:false,
      // 登陆状态
      state:{
            type: 'user',
            user_id: 0,
            username:  "",
            avatar: "",
			user_valid:false
        },
    }
  },
  methods:{
        //===============响应式布局==========
        get_header_height(){
            if(this.width < VALUE.PHONE_WIDTH)
            {
                return "75px"
            }
            else
            {
                return "75px"
            }
        },

        url_error_report(){
            this.url_error = true
        },


        open_center:function(){
            this.center_dialog_visible = true
        },
        open_comment_center:function(){
            this.comment_dialog_visible = true
        },
        open_drawer: function(){
            this.drawer = true
        },

        open_login: function(type){
            this.login_visible = true
            this.login_type = type
        },

        // 更改密码
        change_password: function(){
            this.drawer = false
            this.open_login('password')
        },

        check_log_in(forbid_message = false){
            console.log('checking login info...')
            var data = 1
            var method = 'GET'
            var url = '/api/login'

            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                my_this.state_checked=true
                if(object.status!=undefined)
                    {
                        console.log(object)
                        my_this.$message.error(object.detail);
                        return
                    }
                my_this.set_account(object.name, object.type, object.id, 1, object.avatar)
                if(forbid_message==false)
                {
                    my_this.get_alert('success','已登陆')
                }
            }
            var get_error = function (err) { 
                my_this.$alert(err)
            }
            request_json(data,url,method, get_response, get_error,10000)
        },

        // 注销
        log_out: function(){
            this.drawer = false
            var data = {
                log_out: true,
                id: this.state.user_id
            }
            var method = 'POST'
            var url = '/api/login'
            const my_this = this
            var get_response = function (res) {
                var object = res.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                my_this.set_account('',0,0,0,null)
                my_this.get_alert('success','成功注销')
            }
            request_json(data,url,method,get_response)
        },
      
        // 允许子组件创建一个alert
        get_alert: function(type, content=''){
            this.$message(
                {
                    type: type,
                    message: content
                }
            )
            // this.alert_content = content
            // if(type == 'success')
            // {
            //     this.alert_visible = true
            //     this.alert_type = type
            // }
            // else if(type == 'error')
            // {
            //     this.alert_visible = true
            //     this.alert_type = type
            // }
        },

        // 设置账号
        set_account: function(username, type, id, valid, avatar){
            if(valid)
            {
                this.$set(this.state,'user_id',id)
                this.$set(this.state,'username',username)
                this.$set(this.state,'avatar',avatar)
                this.$set(this.state,'type',type)
                this.$set(this.state,'user_valid',true)
                console.log(this.state)
            }
            else{
                this.$set(this.state,'user_id',id)
                this.$set(this.state,'username',username)
                this.$set(this.state,'avatar',avatar)
                this.$set(this.state,'type',type)
                this.$set(this.state,'user_valid',false)
            }
        },

        // 关闭Login窗口
        close_login: function(){
            this.login_visible = false
        },
  },
  watch: {
        // 实现自动3秒后消失
        alert_visible: function(){
            if (this.alert_visible==true)
            {
                var my_this = this
                setTimeout(function () {
                    my_this.alert_visible = false
                }, 3000);
            }
        },
        $route(){
            if(this.$route.name==undefined){
                this.url_error = true
            }
            else{
                this.url_error = false
            }
        }
        
    },
    computed: {
        
    },
    created() 
    {
        const my_this=this
        var f = function(){
            var docEl = document.documentElement;
            my_this.width = docEl.getBoundingClientRect().width;
        }
        f()
        setInterval(f,2000)
        // this.check_log_in()
    },
    mounted(){
        // this.$message('检查登陆状态中')
        this.check_log_in()
    },
    store:{

    }
}
</script>

<style scoped>
    #app {
      font-family: Avenir, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: #2c3e50;
      background-color: rgb(240, 240, 240);
    }

    *:focus{
        outline:none;
    }

    @media screen and (max-width: 1200px) and (min-width: 768px) {
        #app{
            width:1200px;
            overflow-x: hidden;
        }
    }

    @media screen and (max-width: 768px) {
        #app{
            font-size: 10px;
            width:100%;
            overflow-x: hidden;
        }
    }

    .el-alert {
            position: fixed;
            left: 40%;
            margin: 50px;
            width: 300px;
            z-index: 1000001;
        }

    #header {
      position: fixed;
      width: 100%;
      z-index: 2001;
      background-color: rgb(70, 70, 70);
    }
    #main {
      margin-top: 75px; /* TODO：需要根据header的高度进行调整 */
      padding: 0;
      overflow-x: hidden;
      background-color: rgb(240, 240, 240);
    }
    .el-menu-item {
        text-align: left;
    }
    .cover {
        width: 3000px;
        height: 2000px;
        z-index: 3000;
        position: fixed;
        top: 0;
        left: 0;
        opacity: 0.6;
        background-color: gray;
        filter: alpha(opacity=40);
    }
    .login {
        top: 100px;
        left: 0;
        width: 100%;
        height: 100%;
        position: fixed; 
        z-index:3001;
    }
</style>

