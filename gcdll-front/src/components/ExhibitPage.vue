<template>
    <div id="exhibit-page">
            <el-row class="main">
                <el-row style="min-height: 300px;max-height: 500px">
                <el-col :span="8" class="cover-container" :xs="{span:24}">
                    <el-skeleton v-if="exhibit_info.img_src==undefined" style="height:100%">
                        <template slot="template">
                            <el-skeleton-item variant="image" style="width: 100%; height: 100%; padding:20px" />
                        </template>
                    </el-skeleton>
                    <img v-else v-bind:src="exhibit_info.img_src" alt="封面">
                </el-col>
                <el-col :span="11" class="introduction-container" :xs="{span:24}">
                    <h2>
                        {{  exhibit_info.name   }}
                    </h2>
                    <p>
                        {{  exhibit_info.introduction    }}
                    </p>
                    <el-row>
                        <el-tag v-for="tag in exhibit_info.tag_list" :key="tag.tag"
                        type="info" effect="dark">
                            {{tag.tag}}
                        </el-tag>
                    </el-row>
                </el-col>
                <el-col :span="4" class="info-container" :xs="{span:24}">
                    <el-col :span="24" :xs="{span:8}">
                        <el-row>
                            <el-button type="success" circle size="medium" @click="comment_visible=true; initial_activename = 'comment'">
                                <i class="el-icon-edit-outline">
                                </i>
                            </el-button>
                        </el-row>
                        <el-row style="font-size:80%">
                            查看评论
                        </el-row>
                    </el-col>
                    <el-col :span="24" :xs="{span:8}">
                        <el-row>
                            <el-button type="success" circle size="medium" @click="comment_visible=true; initial_activename='introduction'">
                                <i class="el-icon-info">
                                </i>
                            </el-button>
                        </el-row>
                        <el-row style="font-size:80%">
                            展览信息
                        </el-row>
                    </el-col>
                    <el-col :span="24" v-if="liked==false" :xs="{span:8}" >
                        <el-row>
                            <el-button type="text" circle size="medium" @click="send_like();">
                                <a-icon type="like" />
                            </el-button>
                        </el-row>

                        <el-row style="font-size:80%">
                            点赞 {{exhibit_info.likes}}
                        </el-row>
                    </el-col>
                    <el-col :span="24" v-else :xs="{span:8}">
                        <el-row>
                            <el-button type="text" circle size="medium" @click="withdraw_like">
                                <a-icon type="like" theme="filled" />
                            </el-button>
                        </el-row>

                        <el-row style="font-size:80%">
                            取消点赞 {{exhibit_info.likes}}
                        </el-row>
                    </el-col>
                </el-col>
                </el-row>

                <el-row style="width:100%" v-if="search_mode==false">
                    <input class="fake-search" @focus="search_mode=true"
                        placeholder="在此搜索...">
                </el-row>
                
            </el-row>
            <el-row class="main" v-if="search_mode==false">
                <exhibit-board :exhibit_style="exhibit_style" :user_state="userstate" :image_list="image_list" :state="my_state" :column="(page_width<768)?2:4">
                </exhibit-board>
                <el-empty v-if="image_list.length==0" description="暂时没有照片"></el-empty>
            </el-row>
            <el-row class="main" v-else>
                <el-card>
                    <div slot="header" class="clearfix">
                        <b class="title" style="font-size:150%">展览内搜索</b>
                        <el-tooltip content="关闭搜索" style="font-size:100%; float:right;">
                            <el-button type="text" @click="search_mode=false">
                                <i class="el-icon-close">
                                </i>
                            </el-button>
                        </el-tooltip>
                    </div>
                <search-page :display_type="'block'" :is_filter="true" 
                :range="'photo'" :exhibit_id="id" :type="0"
                :auto_focus="true">
                </search-page>
                </el-card>
            </el-row>
        <el-dialog id="image-info-dialog" :visible.sync="comment_visible" top="40px" width="600px" lock-scroll :fullscreen="page_width<768">
            <div class="dialog-block">
                <image-info-board :user_state="userstate" :type="0" :id="exhibit_info.id" 
                    :image_operation="exhibit_operation" :need_update="exhibit_update"
                    :image_info="exhibit_info" :tag_list="exhibit_info.tag_list"
                    :initial_activename="initial_activename">
                </image-info-board>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import SearchPage from './SearchPage.vue'
import ExhibitBoard from './ExhibitBoard.vue'
import ImageInfoBoard from './ImageInfoBoard.vue'
import {request_json} from '@/utils/communication.js'

// 展览页面
export default {
    name: "ExhibitPage",
    components: {
        // ExhibitBlock,
        ExhibitBoard,
        ImageInfoBoard,
        SearchPage
    },
    props: {
        page_width:{
            type:Number,
            required:true,
        },
        // 展览id，从router来
        id: {
            type:String,
            require:true
        },
        // 账户
        userstate:{
            type: Object,
            required: true
        },
        // 打开登陆页
        openlogin:{
            type:Function,
            require:true
        },
        url_error_report:{
            type:Function,
            require:true
        },
    },
    data(){
        return {
            exhibit_style: 'swipe',
            search_mode: false,

            // 已点赞
            liked: false,

            //评论区可见
            comment_visible: false,
            initial_activename: 'comment',

            //展览信息
            exhibit_info: {},
            // 展览中照片集
            image_list: [],
        }
    },
    computed:{
        my_state(){
            if(this.exhibit_style=='rank' || this.exhibit_style=='cross')
                return 'auto_photo'
            return 'photo'
        }
    },
    methods:{
        //从后端要信息
        exhibit_update: function(){
            var data = {id: String(this.id)}
            var method = 'GET'
            var url = '/api/exhibit'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    my_this.url_error_report()
                    return
                }
                my_this.image_list = object.img_list
                my_this.exhibit_info = object.exhibit_info
                my_this.exhibit_style = object.exhibit_info.style
            }
            request_json(data,url,method,get_response)
            
        },

        //给展览点赞
        exhibit_operation: function(type, content){
            if(this.userstate.user_valid == false)
            {
                this.openlogin()
                return
            }
            var data = {
                    id:String(this.id),
                    type:String(type),
                    content:content,
                }
            var method = 'POST'
            var url = '/api/exhibit'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    return
                }
                var message = ""
                if(type==1)
                  message = "点赞"
                else if(type==3)
                  message = "取消点赞"
                else
                  message = "发送评论"
                my_this.$message({
                  type:'success',
                  message: "成功"+message,
                })
                my_this.exhibit_update()
            }
            request_json(data,url,method,get_response)
        },

        // 关闭评论区
        close_comment:function(){
            this.comment_visible = false
        },

        // 点赞
        send_like: function(){
            if(this.userstate.user_valid == false)
            {
                this.openlogin()
                return
            }
            this.liked = true
            this.$set(this.exhibit_info,'likes',this.exhibit_info.likes+1)
            this.exhibit_operation(1,'')
        },

        // 取消点赞
        withdraw_like: function(){
            this.liked = false
            this.$set(this.exhibit_info,'likes',this.exhibit_info.likes-1)
            this.exhibit_operation(3,'')
        },

        get_background(url){
            return {
                'background': "url("+url+")",
                'background-position': '50%',
                'background-repeat': 'no-repeat',
                'background-size': 'fill'
            }
        },
    },
    created: function(){
        this.exhibit_update()
    },
    watch:{
        exhibit_info(){
            this.liked = this.exhibit_info.liked
        }
    }
}
</script>

<style scoped>
    .main{
        padding:10px;
        width:100%;
        margin-bottom:20px;
    }

    .cover-container {
        height: 250px;
        margin: 10px;
        border-style: inset;
        border-color:rgb(210, 210, 210);
        border-width: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
        float: left;
    }

    .cover-container img {
        padding-bottom: 0px;
        height: 100%;
        width: 100%;
        object-fit: cover;
        margin: auto;
        display: inline-block;
    }

    .border {
        width: 1px;
        height: 100%;
        margin-left: 20px;
        margin-right: 20px;
        background-color: #888888;
        float: left;
    }

    .introduction-container {
        height: 100%;
        float: left;
        text-align: left;
        padding-left: 10px;
    }

    .info-container {
        /* width: 100px; */
        /* height: 100%; */
        float: right;
        /* padding: 10px; */
    }

    .info-container .el-button {
        margin: 10px;
    }

    .el-icon-edit-outline, .el-icon-star-off, .el-icon-star-on, .el-icon-info {
        font-size: 250%
    }

    .el-main {
        height: auto;
        overflow: hidden;
    }

    .dialog-block {
        height: 500px;
    }

    .fake-search {
        border-radius:40px;
        border-width: 2px;
        border-style: solid;
        height: 40px;
        width:70%;
        max-width: 500px;
        text-align: center;
    }

    .fake-search:hover{
        opacity: 0.8;
    }

    .modal{
        margin:auto;
        position:relative;
        width:100%;
    }

    .modal-header{
        position:absolute;
        z-index:2;
        right:100px;
        top:20px;
    }

    .anticon {   
        font-size:250%; 
        color:rgb(255, 77, 0);
    }
</style>