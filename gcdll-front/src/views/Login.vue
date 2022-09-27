<template>
    <el-dialog class="login"
        :title="title[state]"
        :visible.sync="visible"
        :width="(page_width<768)?'90%':'400px'"
        :before-close="handleClose">
            <div id="login" v-if="state==0">
                <el-input v-model="loginInfo.account" placeholder="用户名">
                        <template #prepend>
                            用户名
                        </template>
                </el-input>  
                <el-input v-model="loginInfo.password" placeholder="密码" show-password>
                    <template #prepend>
                        密码
                    </template>
                </el-input> 
            </div>
            <div id="register" v-else-if="state==1">
                <div id="input">
                    <el-input value v-model="registerInfo.account" placeholder="用户名">
                        <template #prepend>
                            <el-badge is-dot class="item">用户名</el-badge>
                        </template>
                    </el-input>
                    <span v-if="registerInfo.account==''">
                        *用户名不能为空
                    </span>
                    <el-input v-model="registerInfo.password" placeholder="密码" show-password>
                        <template #prepend>
                            <el-badge is-dot class="item">密码</el-badge>
                        </template>
                    </el-input>
                    <span v-if="registerInfo.password==''">
                        *密码不能为空
                    </span>
                    <el-input v-model="registerInfo.check_password" placeholder="再次输入密码" show-password>
                        <template #prepend>
                            <el-badge is-dot class="item">确认密码</el-badge>
                        </template>
                    </el-input>  
                    <span v-if="registerInfo.password!=registerInfo.check_password">
                        *两次密码不一致
                    </span>              
                </div>
            </div>
            <div id="change-password" v-else>
                <div id="input">
                    <el-input value :placeholder="user_state.username" disabled>
                        <template #prepend>
                            用户名
                        </template>
                    </el-input>
                    <el-input v-model="loginInfo.password" placeholder="密码" show-password>
                        <template #prepend>
                            密码
                        </template>
                    </el-input> 
                    <el-input v-model="registerInfo.password" placeholder="新密码" show-password>
                        <template #prepend>
                            <el-badge is-dot class="item">新密码</el-badge>
                        </template>
                    </el-input>
                    <span v-if="registerInfo.password==''">
                        *密码不能为空
                    </span>
                    <el-input v-model="registerInfo.check_password" placeholder="再次输入新密码" show-password>
                        <template #prepend>
                            <el-badge is-dot class="item">确认新密码</el-badge>
                        </template>
                    </el-input>
                    <span v-if="registerInfo.password!=registerInfo.check_password">
                        *两次密码不一致
                    </span>              
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <div v-if="state==0">
                    <el-button id="login-button" type="primary" v-on:click="login">登   录</el-button>
                    <el-button id="change-state-button" v-on:click="change_state"> 新用户注册 </el-button>
                </div>
                <div v-else-if="state==1">
                    <el-button id="login-button" type="primary" v-on:click="register">注册</el-button>
                    <el-button id="change-state-button" v-on:click="change_state"> 老用户登陆 </el-button>
                </div>
                <div v-else>
                    <el-button id="login-button" type="primary" v-on:click="change_password">修改</el-button>
                </div>
            </span>
    </el-dialog>
</template>

<script>
import {request_json} from '../utils/communication.js'

export default {
    name: "Login",
    components: {
        // NavBar,
    },
    props:
    {
        page_width:{
            type:Number,
            required:true,
        },
        user_state:{
            type: Object,
            required: true
        },
        visible:{
            type: Boolean,
            required: false,
        },
        login_type:{
            type: String,
            required: true
        },
        get_alert:{
            type: Function,
            required: true
        },
        set_account:{
            type: Function,
            required: true
        },
        close_login:{
            type: Function,
            required: true
        }
    },
    data() {
        return {
            title:[
                '游客/管理员登录',
                '注册',
                '更改密码',
            ],
            id: "",
            name: "",
            loginInfo: {
                account: "",
                password: "",
            },
            registerInfo: {
                account: "",
                password: "",
                check_password: "",
            },
            state: 0,   //0-登陆，1-注册
        }
    },
    methods: {
        handleClose(){
            this.close_login()
        },
        // 登陆、注册切换：清空了变量
        change_state: function() {
            this.registerInfo.account=""
            this.registerInfo.password=""
            this.registerInfo.check_password=""
            this.loginInfo.account=""
            this.loginInfo.password=""
            this.state = 1-this.state
        },

        // TODO: 添加判断id是否为用户/管理员

        // 处理登陆信息，并向后端发送数据
        login: function() {
            if(this.loginInfo.account=='')
            {
                this.$message('用户名不能为空')
                return
            }
            if(this.loginInfo.password=='')
            {
                this.$message('密码不能为空')
                return
            }
            console.log('sending login info...')
            var data = {
                login: true,    
                user: this.loginInfo.account,
                password: this.loginInfo.password,
            }
            var method = 'POST'
            var url = '/api/login'

            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data

                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                my_this.id = object.id
                my_this.name = object.name
                my_this.loginInfo.account = ''
                my_this.$props.set_account(my_this.name, object.type, my_this.id, 1, object.avatar)
                my_this.$props.close_login() 
                my_this.get_alert('success','成功登陆')
            }
            var get_error = function (err) { 
                my_this.$alert(err)
            }
            request_json(data,url,method, get_response, get_error,10000)
            
        },

        // 处理注册信息，并向后端发送数据
        register: function() {
            if(this.registerInfo.account=='')
            {
                this.$message('用户名不能为空')
                return
            }
            if(this.registerInfo.password=='')
            {
                this.$message('密码不能为空')
                return
            }
            if(this.registerInfo.password != this.registerInfo.check_password)
            {
                this.$message('两次密码不一致')
                return
            }
            console.log('sending register info...')
            var data = {
                register: true,    
                user: this.registerInfo.account,
                password: this.registerInfo.password,
            }
            var method = 'POST'
            var url = '/api/login'
            
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                my_this.id = object.id
                my_this.name = object.name
                my_this.loginInfo.account = ''
                my_this.$props.set_account(my_this.name, object.type, my_this.id, 1, object.avatar)
                my_this.$props.close_login() 
                my_this.get_alert('success','成功注册')
                }
            var get_error = function (err) { 
                my_this.$alert(err)
            }
            request_json(data,url,method, get_response, get_error)
            
        },

        // 更改密码
        change_password: function(){
            if(this.loginInfo.password=='')
            {
                this.$message('旧密码不能为空')
                return
            }
            if(this.registerInfo.password=='')
            {
                this.$message('新密码不能为空')
                return
            }
            var data = {
                change_password: true,    
                id: this.user_state.user_id,
                old_password: this.loginInfo.password,
                new_password: this.registerInfo.password,
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
                my_this.get_alert('success','密码修改成功')
            }
            my_this.$props.close_login() 
            request_json(data,url,method,get_response)
        },

        clear(){
            this.loginInfo.account=""
            this.loginInfo.password=""
            this.registerInfo.account=""
            this.registerInfo.password=""
            this.registerInfo.check_password=""
            this.state = 0
            this.login_type = 'login'
        }
    },
    watch:{
        login_type(){
            if(this.login_type=='password')
                this.state = 2
            else
                this.state = 0
        },
        visible(){
            if(this.visible==false){
                this.clear()
            }
        }
    },
    created: function(){
        this.clear()
        if(this.login_type=='password')
        {
            this.state = 2
        }
    }
}
</script>

<style>
    #out {
        padding-left: 10%;
        padding-right: 10%;
    }
    #login-main {
        display: flex; 
        flex-direction:row; 
        justify-content: center;
    }
    #name{
        font-family: "Microsoft Yahei";
        font-size: 30px;
        color:black;
        text-shadow: 5px 5px 5px #888888;
    }
    .login .el-input {
        margin: 5px 0;
    }
    #login-button {
        margin: 10px;
    }
    #login,#register,#change-password{
        max-width: 400px;
        min-width: 300px;
        align-self: center;
        padding: 5px;
        background-color: white;
        /* border: 2px solid; */
        border-radius: 5px;
    }
    #input span{
        font-size: 70%;
        color: rgb(255, 0, 0);
    }
    .el-icon-close:hover {
        color:deepskyblue;
    }
</style>