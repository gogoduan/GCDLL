<template>
    <div id="image-pic-board">
        <el-row style="height: 90px">
            <el-col :span="10">
                    <el-row style="padding-left:30px; margin-top: 20px; font-size:150%; text-align:left">
                        <b>
                            {{  image_info.name     }}
                        </b>
                    </el-row>
                    <el-row style="color: gray; padding-left:30px; margin-top: 5px; font-size:80%; text-align:left">
                        {{    datetime    }}
                    </el-row>
            </el-col>
            <el-col :span="8">
                <div class="button-section">
                    <el-col :span="12" v-if="$route.name == 'image'">
                        <el-row>
                            <el-button type="text" @click="go_to_route">
                                <i class="el-icon-s-operation">
                                </i>
                            </el-button>
                        </el-row>
                        <el-row>
                            <span style="font-size: 80%">
                                修复详情
                            </span>
                        </el-row>
                    </el-col>
                    <el-col :span="12" v-else>
                        <el-row>
                            <el-button type="text" @click="go_to_route">
                                <i class="el-icon-picture">
                                </i>
                            </el-button>
                        </el-row>
                        <el-row>
                            <span style="font-size: 80%">
                                照片详情
                            </span>
                        </el-row>
                    </el-col>
                    <el-col :span="12" v-if="$route.name == 'image'">
                        <el-row :span="24">
                            <el-button v-if="liked==false" type="text" @click="send_like">
                                <a-icon type="like" />
                            </el-button>
                            <el-button v-else type="text" @click="withdraw_like">
                                <a-icon type="like" theme="filled" />
                            </el-button>
                        </el-row>
                        <el-row>
                            <span style="font-size: 80%">
                                点赞{{image_info.likes}}
                            </span>
                        </el-row>
                    </el-col>              
                </div>
            </el-col>
            <el-col :span="6">
                <el-row style="height: 80px">
                    <el-col :span="10" style="margin-top:20px;">
                    <el-avatar :size="50" icon="el-icon-user-solid">
                    </el-avatar>
                    </el-col>
                    <el-col :span="14" style="margin-top:20px;">
                        <el-row>
                        <b>
                            上传人
                        </b>
                        </el-row>
                        <el-row>
                        <b>
                            {{image_info.publisher_name}}
                        </b>
                        </el-row>
                    </el-col>
                </el-row>
                </el-col>
                    
        </el-row>
        <el-row class="main-container">
            <el-skeleton class="img_container" style="width: 90%;margin:auto"
             v-if="image_info.img_src==undefined" animated>
                <template slot="template">
                    <el-skeleton-item
                        variant="image"
                        style="width: 100%; height: 400px;"
                        />
                </template>
            </el-skeleton>
                <div v-else class="img-container">
                    <div id="after-repair" :style="after_style">
                        <div class="cover-wrap">
                            <div id="before-repair" :style="before_style">
                            </div>
                        </div>
                        <div class="center-line">
                            <div class="circle">
                            </div>
                            <el-tooltip id="tooltip" class="item" effect="dark" content="拖动试试" placement="right" :disabled="Boolean(show_tooltip)">
                                
                                    <i class="el-icon-rank">
                                    </i>
                                
                            </el-tooltip>
                            
                        </div>
                        <div id="before-sign">
                            <el-tag type="info" effect="dark" style="margin:0">修复后</el-tag>
                        </div>
                        <div id="after-sign">
                            <el-tag type="info" effect="dark" style="margin:0">修复前</el-tag>
                        </div>
                    </div>
                </div>
        </el-row>
            
    </div>
</template>

<script>
import $ from 'jquery'

// 图片版面
export default {
    name: "ImagePicBoard",
    components: {
        
    },
    props: {
        // 账户
        user_state:{
            type: Object,
            required: true
        },
        image_operation:{
            type:Function,
            require:true
        },
        image_info: {
            type: Object,
            default:() => {
                
            },
        },
        openlogin:{
            type:Function,
            require:true
        },
    },
    data(){
        return {
            show_tooltip: false,
            liked: false,
        }
    },
    computed:{
        datetime:function () {
			var d = new Date()
			var a = this.image_info.timestamp
            if (a < 1000000000000)
			{
				a *= 1000
			}
			d.setTime(a)
			return d.toLocaleString()
		},
        before_style:function(){
            var s = "background-image: url('" + this.image_info.old_img_src + "');"
            // alert(s)
            return s
        },
        after_style:function(){
            var s = "background-image: url('" + this.image_info.img_src + "');"
            // alert(s)
            return s
        }
    },
    methods:{
        go_to_route: function(){
            if(this.$route.name == 'image')
            {
                if(this.user_state.user_valid == false)
                {
                    this.openlogin()
                    return
                }
                this.$router.push({ name: 'repair', params: { id: String(this.image_info.id)} })
            }
            else
            {
                this.$router.push({ name: 'image', params: { id: String(this.image_info.id)} })
            }
        },
        // 点赞
        send_like: function(){
            if(this.user_state.user_valid == false)
            {
                this.openlogin()
                return
            }
            this.liked = true
            this.$set(this.image_info,'likes',this.image_info.likes+1)
            this.$props.image_operation(1,'')
        },
        // 取消点赞
        withdraw_like: function(){
            this.liked = false
            this.$set(this.image_info,'likes',this.image_info.likes-1)
            this.$props.image_operation(3,'')
        },
        bind_move(){
            const my_this = this
            $('.center-line').mousedown(function(e){
                // alert(my_this.show_tooltip)
                my_this.show_tooltip = 1
                
                var left = parseInt($('.center-line').css('left'))
                var downX = e.pageX;
                // 改成和document绑定，就会更顺滑
                $(document).bind("mousemove", function(es){
                    var endx = es.pageX - downX + left;
                    if(endx < 0)
                        endx = 0
                    var width_str = $('.img-container').css('width')
                    var width = Number(width_str.substr(0,width_str.length-2))
                    if(endx > width - 20)
                        endx = width - 20
                    $('.center-line').css('left',endx+'px')
                    $('.cover-wrap').css('left',endx+'px')
                })
            });

            $('.center-line').mouseup(function(){
                $(document).unbind("mousemove")
            })

            $('.center-line').on("touchstart",function(e){
                if(e.cancelable){
                    if(!e.defaultPrevented){
                        e.preventDefault()
                    }
                }
                // alert(my_this.show_tooltip)
                my_this.show_tooltip = 1
                
                var left = parseInt($('.center-line').css('left'))

                // 替换成手机touch事件
                var downX = e.originalEvent.changedTouches[0].pageX
                // 改成和document绑定，就会更顺滑
                $(document).bind("touchmove", function(es){
                    if(es.cancelable){
                        if(!es.defaultPrevented){
                            es.preventDefault()
                        }
                    }
                    var endx = es.originalEvent.changedTouches[0].pageX - downX + left;
                    if(endx < 0)
                        endx = 0
                    var width_str = $('.img-container').css('width')
                    var width = Number(width_str.substr(0,width_str.length-2))
                    if(endx > width - 20)
                        endx = width - 20
                    $('.center-line').css('left',endx+'px')
                    $('.cover-wrap').css('left',endx+'px')
                })
            });

            $('.center-line').on("touchend",function(e){
                if(e.cancelable){
                    if(!e.defaultPrevented){
                        e.preventDefault()
                    }
                }
                $(document).unbind("touchmove")
            })
    
        }
    },
    created:function(){
        $(document).ready(function(){
            // 执行代码
            var left = $('.center-line').css("left");
            $('.cover-wrap').css("left", left);
            setInterval(
                function(){
                var width = $('#after-repair').css('width');
                $('#before-repair').css('width',width);
                var left = $('.center-line').css("left");
                $('.cover-wrap').css("left", left);
                },1000
            )
        });
        
    },
    mounted:function(){
        
    },
    watch:{
        image_info(){
            this.liked = this.image_info.liked
            // 在这里绑定jquery
            this.bind_move()
        },
    }
}
</script>

<style scoped>
    #image-pic-board {
        height:100%;
        padding-bottom:5px;
    }
    .main-container {
        vertical-align:middle;
         display: flex;
    }

    .img-container {
        max-width: 600px;
        width:100%;
        height: 400px;
        margin:auto;
        text-align:center;
        min-height: 400px;
        border-style: inset;
        box-sizing: content-box;
        border-color:rgb(210, 210, 210);
        border-width: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    }

    #after-repair {
        display: block;
        position: relative;
        background-position: 50%;
        background-repeat: no-repeat;
        background-size: contain;
        max-width: 600px;
        width:100%;
        height: 400px;
        text-align:center;
        min-height: 400px;
    }

    .cover-wrap {
        position: absolute;
        left: 50%;
        margin-left: 11px;
        bottom: 0;
        right:0;
        top:0;
        box-sizing: border-box;
        overflow: hidden;
    }

    #before-repair{
        display: block;
        position: absolute;
        bottom: 0;
        right:0;
        top:0;
        background-position: 50%;
        background-repeat: no-repeat;
        background-size: contain;
        /* max-width: 600px;
        width:100%; */
        height: 400px;
        text-align:center;
        min-height: 400px;
        /* background: rgb(200, 200, 200); */
    }

    .center-line {
        cursor: move;
        position: absolute;
        bottom: 0;
        right:0;
        top:0;
        left: 40%;
        width: 24px;
        height: 100%;
        background-color: white;
        background-clip: content-box;
        padding: 0 11px;
        box-sizing: border-box;
        display: block;
    }

    .circle {
        position: absolute;
        top:70%;
        left:-7px;
        height: 40px;
        width: 40px;
        border-radius: 100%;
        background:gray;
        z-index: 100;
    }

    .el-icon-rank {
        position: absolute;
        bottom: 0;
        right: -8px;
        top:70%;
        font-size: 40px;
        font-weight: 700;
        color: white;
        z-index: 101;
        /* border-style: dotted; */
    }

    #after-sign {
        position: absolute;
        top:0;
        left: 0;
        opacity: 0.8;
    }

    #before-sign {
        position: absolute;
        top:0;
        right: 0;
        opacity: 0.8;
    }

    .el-footer {
        text-align: center;
        display: flex;
    }

    .button-section{
        display: block;
    }

    .el-footer .el-button--text{
        /* margin:5px; */
        padding: 3px;
    }

    .el-icon-s-operation,.el-icon-picture {
        font-size:250%; 
    }

    .anticon {   
        font-size:250%; 
        color:rgb(255, 77, 0);
    }
</style>