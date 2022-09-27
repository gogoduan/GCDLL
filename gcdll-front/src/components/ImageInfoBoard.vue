<template>
    <div id="image-info-board">
        <!-- 可选风格 type="border-card" -->
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="简介" name="introduction">
                <el-container>
                    <el-header height="30px">
                        <div class="title">
                            <b>
                                简介
                            </b>
                        </div>
                        
                    </el-header>
                    <el-main>    
                        {{  image_info.introduction    }}
                    </el-main>
                    <el-footer height="100px">
                        <el-row style="overflow-x:auto;white-space: nowrap;">
                            <el-tag type="info" style="border-radius:20px;"
                                v-for="tag,index in tag_list" :key="index">
                                {{tag.tag}}
                            </el-tag>
                        </el-row>
                    </el-footer>
                </el-container>
            </el-tab-pane>
            <el-tab-pane :label="'评论 '+image_info.comments" name="comment">
                <el-container>
                    <el-header height="30px">
                        <div class="title">
                            <b>
                                热门评论
                            </b>
                            <span style="font-size:80%">
                                共{{image_info.comments}}条
                            </span>
                            
                        </div>
                        <div class="title-button">
                            <el-button type="text" v-if="sort_order=='popularity'" @click="change_sort_order">
                                按时间
                            </el-button>
                            <el-button type="text" v-else  @click="change_sort_order">
                                按热度
                            </el-button>
                        </div>
                    </el-header>
                    <el-main :style="'height:'+(parent_height-230)+'px'">    
                        <div class="comment-list" v-infinite-scroll="image_comment_update" :infinite-scroll-disabled="scroll_disable" style="overflow: auto">
                            <!-- 头部加载条 -->
                            <div>
                                <div v-if="update_loading">
                                    <el-row :span="4">
                                        <i class="el-icon-loading" style="font-size:100%">
                                        </i>
                                    </el-row>
                                    <el-row :span="4">
                                        加载中...
                                    </el-row>
                                </div>
                                <div v-if="update_loading_error">
                                    <el-row :span="4">
                                        <i class="el-icon-warning" style="font-size:100%">
                                        </i>
                                    </el-row>
                                    <el-row :span="4">
                                        加载失败
                                    </el-row>
                                </div>
                            </div>
                            <!-- 评论内容 -->
                            <transition-group name="listgroup" tag="ul">
                                <div class="comment-item" v-for="comment in comment_list" :key="comment.id">
                                    <el-row>
                                        <el-col :span="3">
                                            <!-- <i class="el-icon-user" style="font-size:250%">
                                            </i> -->
                                            <el-avatar :src="comment.avatar">
                                            </el-avatar>
                                        </el-col>
                                        <el-col :span="21">
                                            <div class="comment-user">
                                            <el-row style="font-size:110%">
                                                {{  comment.user    }}
                                            </el-row>
                                            <el-row style="font-size:70%">
                                                {{  new Date(comment.timestamp).toLocaleDateString().replace(/\//g, "-")    }}
                                                {{  new Date(comment.timestamp).toLocaleTimeString()    }}
                                            </el-row>
                                        </div>
                                        <div class="comment-content">
                                            {{  comment.content  }}
                                        </div>
                                        <div class="comment-footer">
                                            <el-row>
                                                <el-col :span="4">
                                                    <el-button v-if="comment.liked==false" type="text" @click="like_operation(comment.id,comment.liked)" style="color:grey">
                                                        <a-icon type="like" />
                                                        点赞 {{comment.likes}}
                                                    </el-button>
                                                    <el-button v-else type="text" @click="like_operation(comment.id,comment.liked)"  style="color:grey">
                                                        <a-icon type="like" theme="filled" />
                                                        取消点赞 {{comment.likes}}
                                                    </el-button>
                                                </el-col>
                                                <el-col :span="10" style="height:20px">
                                                </el-col>
                                                
                                                <el-col :span="2" v-if="comment.user == user_state.username">
                                                    <el-button type="text" @click="delete_comment(comment.id)" style="color: grey">
                                                        <a-icon type="delete" />
                                                        删除
                                                    </el-button>
                                                </el-col>
                                                <el-col :span="2" v-else>
                                                    <el-button type="text" style="color: grey" @click="report_comment(comment.id)">
                                                        <a-icon type="info-circle" />
                                                        <span v-if="!comment.reported">
                                                            举报
                                                        </span>
                                                        <span v-else>
                                                            已举报
                                                        </span>
                                                    </el-button>
                                                </el-col>
                                            </el-row>
                                        </div>
                                        </el-col>
                                    </el-row>   
                                </div>
                            </transition-group>
                            <el-empty v-if="comment_list.length==0" description="暂时没有评论"></el-empty>
                            <!-- 尾部加载条 -->
                            <div>
                                <div v-if="loading">
                                    <el-row :span="4">
                                        <i class="el-icon-loading" style="font-size:100%">
                                        </i>
                                    </el-row>
                                    <el-row :span="4">
                                        加载中...
                                    </el-row>
            
                                </div>
                                <div v-else-if="loading_error">
                                    <el-row :span="4">
                                        <i class="el-icon-warning" style="font-size:100%">
                                        </i>
                                    </el-row>
                                    <el-row :span="4">
                                        加载失败
                                    </el-row>
                                </div>
                                <div v-else class="buffer">
                                    <el-row :span="8">
                                        <i class="el-icon-more" style="font-size:100%">
                                        </i>
                                    </el-row>
                                    
                                    <el-row v-if="update_all" :span="8">
                                        已经加载全部评论
                                        <el-button type="text" @click="insist_update">
                                            再刷新试试
                                        </el-button>
                                    </el-row>
                                    <el-row v-else :span="8">
                                        下滑查看更多评论
                                    </el-row>
                                </div>
                            </div>
                        </div>
                    </el-main>
                    <el-footer height="60px">
                        <el-col :span="4">
                        <el-avatar :src="user_state.avatar">
                        </el-avatar>
                        </el-col>
                        <el-col :span="16">
                        <div v-if="user_state.user_valid==true" class="input-comment">
                            <el-input type="textarea" resize="none" v-model="my_comment" placeholder="发一条友善的评论"></el-input>
                        </div>
                        <div v-else class="input-comment">
                            <el-input type="textarea" resize="none" placeholder="请登陆后评论" disabled></el-input>
                        </div>
                        </el-col>
                        <el-col :span="4">
                        <div class="input-comment-button">
                            <el-button round v-if="my_comment==''" disabled>发送</el-button>
                            <el-button round v-else @click="send_comment">发送</el-button>
                        </div>
                        </el-col>
                    </el-footer>
                </el-container>
            </el-tab-pane>
        </el-tabs>
        
    </div>
</template>

<script>
import {request_json} from '../utils/communication.js'

// 图片详情版面，评论版面
export default {
    name: "ImageInfoBoard",
    components: {
        
    },
    props: {
        // 账户
        user_state:{
            type: Object,
            required: true
        },
        id:{
            type: Number,
            default:()=> {
                return 0
            }
        },
        image_operation:{
            type:Function,
            require:true
        },
        need_update:{
            type:Function,
            require:true
        },
        // 1-照片 0-展览
        type:{
            type:Number,
            require:true
        },
        image_info:{
            type:Object,
            require:true,
        },
        initial_activename:{
            type:String,
            default:'comment',
        },
        tag_list:{
            type: Array,
            default(){return ['人像','已修复','人像','已修复','人像','已修复','人像','已修复']},
        },
    },
    data(){
        return {
            parent_height: 680,
            activeName: 'comment',
            // 从后端接收的
            comment_list: Array(0).fill({
				id: 10,
                user: "unknown",
				content: "Hello World!",
                likes: 0,
                liked: false,   // 是否已经点过赞
                timestamp: new Date().getTime()
            }),
            // input输入，准备发送给后端
            my_comment: "",
            // 参数
            sort_order: "popularity",  //排序依据
            // 正在加载评论
            loading: false,
            // 加载评论失败
            loading_error: false,
            // 正在加载评论
            update_loading: false,
            // 加载评论失败
            update_loading_error: false,
            // 后端全部评论已经被刷新完
            update_all: false,
            page: 0,
        }
    },
    methods:{
        get_box_height(){
            var object = document.getElementById("image-info-dialog")
            if(object!=null)
            {
                object = object.getElementsByClassName('el-dialog')[0]
                this.parent_height =  object.clientHeight
                console.log(object.clientHeight)
            }
        },
        // 评论发送
        send_comment: function(){
            this.$props.image_operation(2,this.my_comment)
            this.my_comment = ''
            const my_this = this
            // 发完2s后，自动刷新
            setTimeout(function(){
                my_this.sort_order = 'time'
                my_this.init_comment()
            },2000)
        },
        // 强制刷新
        insist_update: function(){
            this.update_all = false
            if(this.page > 0)
            {
                this.page = this.page - 1
            }
            else
            {
                this.page = 0
            }
            this.image_comment_update()
        },
        init_comment(){
            this.comment_list=[]
            this.page = 0
            this.update_all = false
            this.image_comment_update()
            this.need_update()
        },
        //获取评论
        image_comment_update: function(){
            if(isNaN(this.id))
                return
            var data = {
                type: String(this.type), //0-展览，1-照⽚ 
                id: String(this.id), 
                order: (this.sort_order=='time')?"1":"0", //排序⽅式，0-按热度，1-按时间最新 
                start: String(this.page), //需要评论范围，[start*10, (start+1)*10) }
            }
            var method = 'GET'
            var url = '/api/comment'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                // 如果所有评论已经加载
                if(object.length < 5)
                {
                    my_this.update_all = true
                    my_this.loading = false
                    my_this.update_loading = false
                }
                if(object.length == 0)
                {
                    my_this.update_all = true
                    my_this.loading = false
                    my_this.update_loading = false
                    return
                }
                for(var i=0;i<object.length;i+=1)
                {
                    var repeat = 0
                    for(var j=0;j<my_this.comment_list.length;j+=1)
                    {
                        if(object[i].id == my_this.comment_list[j].id)
                        {
                            repeat = 1
                            break
                        }
                    }
                    if(repeat==0)
                        my_this.comment_list.push(object[i])
                }
                for(let comment of my_this.comment_list) {
                    comment.timestamp *= (comment.timestamp < 1e12 ? 1000 : 1);
                }
                // my_this.comment_list = my_this.comment_list.concat(object)
                // console.log(my_this.comment_list)
                my_this.page += 1
                my_this.loading = false
                my_this.update_loading = false
            }
            // alert("正在向后端要评论")
            if(this.update_loading==false)
            {
                this.loading = true
            
                setTimeout(function(){
                    if(my_this.loading==false)
                        return
                    // alert('end')
                    my_this.loading = false
                    // alert(my_this.loading)
                    my_this.loading_error = true
                    setTimeout(function(){
                        my_this.loading_error = false
                        // my_this.update_all = true
                    },2000)
                },5000)
            }
            else{
                setTimeout(function(){
                    if(my_this.update_loading==false)
                        return
                    // alert('end')
                    my_this.update_loading = false
                    // alert(my_this.loading)
                    my_this.update_loading_error = true
                    setTimeout(function(){
                        my_this.update_loading_error = false
                        // alert(1)
                    },2000)
                },5000)
            
            }
            request_json(data,url,method,get_response)
            
        },
        // 改变评论排序方式
        change_sort_order: function(){
            if(this.sort_order=='popularity')
            {
                this.sort_order='time'
            }
            else{
                this.sort_order='popularity'
            }
            this.update_loading = true
            this.page = 0
            this.update_all = false
            this.comment_list = []
            this.image_comment_update()
        },

        // 给评论点赞
        send_like_to_comment:function(comment_id){
            var data = {
                id:String(comment_id),
                type:'like',
                object: String(1 - this.type),
            }
            var method = 'POST'
            var url = '/api/comment'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                for(let i =0;i<my_this.comment_list.length;i+=1)
                {
                    if(my_this.comment_list[i].id == comment_id)
                    {
                        my_this.comment_list[i].liked = true
                        my_this.comment_list[i].likes += 1
                    }
                }
            }
            request_json(data, url, method, get_response)
        },

        withdraw_like_to_comment:function(comment_id){
            var data = {
                id:String(comment_id),
                type:'unlike',
                object: String(1 - this.type),
            }
            console.log(data)
            var method = 'POST'
            var url = '/api/comment'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                for(let i =0;i<my_this.comment_list.length;i+=1)
                {
                    if(my_this.comment_list[i].id == comment_id)
                    {
                        my_this.comment_list[i].liked = false
                        my_this.comment_list[i].likes -= 1
                    }
                }
            }
            request_json(data, url, method, get_response)
        },

        like_operation:function(comment_id,comment_liked){
            if(comment_liked==false)
                this.send_like_to_comment(comment_id)
            else
                this.withdraw_like_to_comment(comment_id)
        },

        // 删除自己的评论
        delete_comment:function(comment_id){
            var data = {
                id:String(comment_id),
                object:String(1 - this.type),
                type:'delete',
            }
            var method = 'POST'
            var url = '/api/comment'
            const my_this = this
            var get_response = function(res) { 
                var object = res.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                my_this.$message('成功删除')
                my_this.init_comment()
            }
            // alert(this.id)
            request_json(data, url, method, get_response)
        },
        // 举报评论
        report_comment:function(comment_id){
            var index = -1
            for(let i=0;i<this.comment_list.length;i+=1){
                if(this.comment_list[i].id == comment_id){
                    index = i
                }
            }
            if(this.comment_list[index].reported){
                this.$message('您已举报，请等待管理员查看')
                return
            }
            var data = {
                id:String(comment_id),
                object:String(1 - this.type),
                type:'report',
            }
            var method = 'POST'
            var url = '/api/comment'
            const my_this = this
            var get_response = function(res) { 
                var object = res.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                my_this.$message({
                    type:'success',
                    message:'成功举报'
                    })
                my_this.comment_list[index].reported = true
                
            }
            // alert(this.id)
            request_json(data, url, method, get_response)
        },
        handleClick(){
            if(this.id!=0)
            {
                this.image_comment_update()
            }
        }
    },
    computed:{
        scroll_disable: function(){
            if(this.update_all)
            {
                return true
            }
            if (this.loading){
                return true
            }
            if (this.loading_error){
                return true
            }
            if (this.update_loading){
                return true
            }
            if (this.update_loading_error){
                return true
            }
            
            return false
        },
    },
    watch:{
        initial_activename:function(){
            this.activeName = this.initial_activename
        },
        id(){
            if(this.id!=0)
            {
                this.init_comment()
            }
        }
    },
    mounted:function(){
        this.init_comment()
        this.get_box_height()
        this.activeName = this.initial_activename
    }
}
</script>

<style scoped>
    .image-info-board {
        overflow: hidden;
        margin: 0px;
        min-width: 500px;
        height:100%;
    }

    .title {
        height: 30px;
        text-align: left;
        float: left;
        margin: 5px
    }

    .title-button {
        float: right;
        margin: 0;
    }

    .comment-item {
        width: 100%;
        min-height: 40px;
        border-bottom-style: solid;
        border-color: rgb(150, 150, 150);
        border-width: 1px;
        background-color: white;
        margin-bottom: 10px;
    }

    .comment-user {
        text-align: left;
        margin: 0px;
    }

    .comment-content {
        width: 90%;
        text-align: left;
        margin-left: 20px;
        overflow-y: scroll;
        overflow-wrap: break-word;
        white-space: pre-line;
    }

    .comment-footer {
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .comment-list {
        height: 100%;
    }

    .buffer {
        height: 100px;
        max-height: 150px;
        min-height: 20px; 
        text-align: center;
    }

    .el-header {
        padding: 0;
        margin: 0;
        position: static;
    }

    .el-main {
        padding: 0;
        /* overflow: hidden; */
        max-height: 400px;
    }

    .el-footer {
        height: 30%;
        margin-top: 10px;
    }

    .input-comment {
        width: 100%;
        float: left;
    }

    .input-comment-button {
        float: right;
        margin-top: 2%;
    }

    .comment-item /deep/ .el-avatar img{
        width:100%
    }

    .el-footer /deep/ .el-avatar img{
        width:100%
    }

    .listgroup-leave-to {
        opacity: 0;
        transform: translateX(50px);
    }
</style>