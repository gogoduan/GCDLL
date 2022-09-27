<template>
    <div id="exhibit-block" :style="[style[state].exhibit_block,has_border]">
        <el-container>
            <el-tooltip content="点击选中" effect="dark" placement="top" :disabled="state!='single_choose'">
            <div class="main-container" :style="style[state].container">
                        <div class="text-modal" v-if="(state=='photo'||state=='auto_photo')">
                            <div class="button-container">
                                <el-button type="text" style="font-size: 200%;color:grey;" 
                                @mouseenter.native="start_play()" @mouseleave.native="end_play()" 
                                @touchstart.native.prevent="handle_touch_play()" @touchmove.native="handle_touch_move">
                                    <a-icon v-if="playing" type="play-circle" theme="filled" />
                                    <a-icon v-else type="play-circle" />
                                </el-button>
                            </div>
                        </div>             
                    <div class="img-container" :style="[style[state].img_container,style[state].container]"
                        @mouseenter="handle_mouse_enter" @mouseleave="handle_mouse_leave" @click="handle_click"
                        @dblclick="send_like" @touchstart="handle_touch_start" @touchmove="handle_touch_move" @touchend.prevent="handle_touch_end"
                    >
                        <div class="img-button" :style="style[state].container">
                            <img v-if="onlyinfo==false&&playing==false" :src="image_src" :style="style[state].img_fit">
                            <img v-else-if="onlyinfo==false&&playing" :src="image_history_list[display_image_cnt].img_src" :style="style[state].img_fit">
                            <swiper v-else-if="playing_props" class="swiper-auto" :options="swiperOption">
                                <swiper-slide 
                                v-for="image in image_history_list" :key="image.id" 
                                :style="get_background(image.img_src)">
                                    
                                </swiper-slide>
                            </swiper>
                        </div>
                        <div class="text-modal" v-if="show_modal && playing==false && playing_props==false">
                            <div class="text-modal-wrapper" :style="style[state].text_container">
                            </div>
                            <div class="text-container" :style="style[state].text_container">
                                <el-row>
                                    <el-col :span="12" class="hide-container">
                                        <span>
                                            #{{  id  }}
                                        </span>
                                        <span style="margin-left: 5px;">
                                            {{   name    }}
                                        </span>
                                    </el-col>
                                    <el-col :span="12" class="hide-container">
                                        <span style="font-size:60%">
                                            {{ datetime }}
                                        </span>
                                    </el-col>
                                </el-row>
                                <el-row class="introduction-bar">
                                    <span>
                                        {{  introduction  }}
                                    </span>
                                </el-row>
                                <el-row class="overflow-container">
                                    <el-tag type="info" effect="dark" style="border-radius:20px;"
                                        v-for="tag,index in tag_list" :key="index" :size="(size>=200)?'medium':'mini'">
                                        {{tag.tag}}
                                    </el-tag>
                                </el-row>
                                <el-row style="font-size: 70%; margin-top:5px;">
                                    <el-col :span="4">
                                        <a-icon type="like" />
                                        {{likes}}
                                    </el-col>
                                    <el-col :span="4">
                                        <i class="el-icon-s-comment">
                                            {{comments}}
                                        </i>
                                    </el-col>
                                    <el-col :span="16" style="text-align:right" class="hide-container">
                                        <i class="el-icon-date">
                                            {{  datetime   }}
                                        </i>
                                    </el-col>
                                </el-row>
                            </div>
                        </div>
                        <div class="progress-modal" v-if="!show_modal && is_progress">
                            <div class="progress-container">
                                <!-- 显示排队中 -->
                                <el-row v-if="expect_time==0">
                                    <el-row>
                                    <a-icon type="pause-circle" style="font-size:800%"/>
                                    </el-row>
                                    <el-row>
                                    <span style="font-size:80%">
                                        已等待：{{wait_time.toFixed(0)}}s
                                    </span>
                                    </el-row>
                                </el-row>
                                <el-row v-else>
                                <el-progress type="circle" :percentage="Number(((now_time/expect_time)*100).toFixed(1))" :stroke-width="15">
                                </el-progress>
                                </el-row>
                                <el-row>
                                <span style="font-size:80%">
                                    正在{{    operation   }}
                                </span>
                                </el-row>
                            </div>
                        </div>
                    </div>
            </div>
            </el-tooltip>
        </el-container>
    </div>
</template>

<script>
import {request_json} from '@/utils/communication.js'
import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
// import $ from 'jquery'
// 展览中一张照片的版面
export default {
    name: "ExhibitBlock",
    components: {
        Swiper,
        SwiperSlide
    },
    props: {
        size:{
            type:Number,
            default:200,
        },
        onlyinfo:{
            type:Boolean,
            default:false,
        },
        // 照片/展览 id
        id: {
            type:Number,
            require:true
        },
        // 0-照片 1-展览
        type: {
            type:Number,
            default: 0,
        },
        name: {
            type: String,
            default: "一个名字"
        },
        timestamp: {
            type: Number,
            default: 0,
        },
        image_src: {
            type: String,
            default: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdesk-fd.zol-img.com.cn%2Ft_s960x600c5%2Fg5%2FM00%2F02%2F05%2FChMkJ1bKyaOIB1YfAAusnvE99Z8AALIQQPgER4AC6y2052.jpg&refer=http%3A%2F%2Fdesk-fd.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1649854587&t=a5f1e9e174a7316000f9488d6365590d"
        },
        introduction: {
            type: String,
            default: "no"
        },
        comments: {
            type:Number,
            require:true
        },
        likes: {
            type:Number,
            require:true
        },
        tag_list: {
            type: Array,
            default(){return [{'tag':'默认'}]}
        },
        // 所需block的状态：exhibit、sketch、photo
        state: {
            type: String,
            default: "photo"
        },
        // 走马灯里展示的样例照片
        display_image_list: {
            type: Array,
            default: () => new Array(4).fill({
                id: 10,
                name: "名字",
				introduction: "这张照片拍摄于1900年......",
				img_src: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdesk-fd.zol-img.com.cn%2Ft_s960x600c5%2Fg5%2FM00%2F02%2F05%2FChMkJ1bKyaOIB1YfAAusnvE99Z8AALIQQPgER4AC6y2052.jpg&refer=http%3A%2F%2Fdesk-fd.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1649854587&t=a5f1e9e174a7316000f9488d6365590d"
			})
        },
        add_to_list: {
            type: Function,
            default: 
                function(){
                    return
                }
        },
        // 是否已选择
        is_chosen: {
            type: Boolean,
            default:false,
        },
        // 是否需要显示进度条
        is_progress:{
            type: Boolean,
            default: false,
        },
        now_time:{
            type: Number,
            default: 0,
        },
        expect_time:{
            type: Number,
            default: 1,
        },
        wait_time:{
            type: Number,
            default: 1,
        },
        operation:{
            type: String,
            default: "",
        },
        // 是否需要自动切换
        playing_props:{
            type: Boolean,
            default: false,
        },
    },
    data(){
        return {
            touch_loop:0,
            swiperOption: {
                spaceBetween: 30,
                effect: 'fade',
                centeredSlides: true,
                autoplay: {
                    delay: 1500,
                    disableOnInteraction: false
                },
            },
            // 是否已经点赞
            liked: false,
            // 多种样式的样式库
            style: 
            {
                //选择照片
                choose: {
                    img_fit: {
                        'width': '100%',
                        'height':'100%',
                        'object-fit':'cover',
                        // 'max-height': '300px',
                    },
                    img_container:{
                        'width':'100%',
                        'height':'100%',
                        'max-height': '300px',
                        "padding": "0px",
                    },
                    container:{
                        'width':'100%',
                        'height':'100%',
                    },
                    text_container:{
                        'top': String(-(this.size-50))+"px",
                        'height': String((this.size-50))+"px",
                        'font-size': (this.size>=200)?'100%':'70%',
                    },
                    exhibit_block:{
                        "height": String((this.size))+"px",
                        "width": String((this.size))+"px",
                        'margin-bottom': '30px',
                    },
                },
                //单选照片
                single_choose: {
                    img_fit: {
                        'width': '100%',
                        'height':'100%',
                        'object-fit':'cover',
                        // 'max-height': '300px',
                    },
                    img_container:{
                        'width':'100%',
                        'height':'100%',
                        'max-height': '300px',
                        "padding": "0px",
                    },
                    container:{
                        'width':'100%',
                        'height':'100%',
                    },
                    text_container:{
                        'top': String(-(this.size-50))+"px",
                        'height': String((this.size-50))+"px",
                        'font-size': (this.size>=200)?'100%':'70%',
                    },
                    exhibit_block:{
                        "height": String((this.size))+"px",
                        "width": String((this.size))+"px",
                        'margin-bottom': '30px',
                    },
                },
                //以照片库展示照片
                display: {
                    img_fit: {
                        'width': '100%',
                        'height': '100%',
                        'object-fit':'cover',
                        'max-height': '300px',
                    },
                    img_container:{
                        'width':'100%',
                        'height': '100%',
                        'max-height': '300px',
                        "padding": "0px",
                    },
                    container:{
                        'width':'100%',
                        'height':'100%',
                    },
                    text_container:{
                        'top': String(-(this.size-50))+"px",
                        'height': String((this.size-50))+"px",
                        'font-size': (this.size>=200)?'100%':'70%',
                    },
                    exhibit_block:{
                        "height": String((this.size))+"px",
                        "width": String((this.size))+"px",
                        'margin-bottom': '30px',
                    },
                },
                //以照片库展示照片
                drag: {
                    img_fit: {
                        'width': '100%',
                        'height': '100%',
                        'object-fit':'cover',
                        'max-height': '300px',
                    },
                    img_container:{
                        'width':'100%',
                        'height': '100%',
                        'max-height': '300px',
                        "padding": "0px",
                    },
                    container:{
                        'width':'100%',
                        'height':'100%',
                    },
                    text_container:{
                        'top': String(-(this.size-50))+"px",
                        'height': String((this.size-50))+"px",
                        'font-size': (this.size>=200)?'100%':'70%',
                    },
                    exhibit_block:{
                        "height": String((this.size))+"px",
                        "width": String((this.size))+"px",
                        'margin-bottom': '30px',
                    },
                },
                //用于展示照片，包含点赞和点进去看看
                photo: {
                    img_fit: {
                        'width': '100%',
                        'object-fit':'cover',
                        "min-height": '200px',
                    },
                    img_container:{
                        "padding": "10px",
                        "height": "auto",
                        "width": '100%',
                    },
                    container:{
                        "min-height": '200px',
                    },
                    text_container:{
                        "padding": "10px",
                    },
                    exhibit_block:{
                        'background': 'white',
                        "min-height": '200px',
                        "height": "auto",
                        "width": "100%",
                        'margin-bottom': '30px',
                    },
                },
                //缩略图，仅包含进去看看
                sketch: {
                    img_fit: {
                        'width': '100%',
                        'height': '100%',
                        'object-fit':'cover',
                        // 'height': '280px',
                    },
                    img_container:{
                        'width':'100%',
                        "padding": "0px",
                    },
                    container:{
                        'width':'100%',
                        'height':'100%',
                    },
                    text_container:{
                        "padding": "5px",
                    },
                    exhibit_block:{
                        "height": "100%",
                        "width": "100%",
                    },
                },
                auto_photo: {
                    img_fit: {
                        'width': '100%',
                        "height": '100%',
                        'object-fit':'cover',
                    },
                    img_container:{
                        "padding": "0px",
                        "width": '100%',
                    },
                    container:{
                        "width": '100%',
                        "height": '100%',
                    },
                    text_container:{
                        "padding": "10px",
                    },
                    exhibit_block:{
                        "min-height": '200px',
                        "height": "100%",
                        "width": "100%",
                        'margin-bottom': '30px',
                    },
                },
                //用于展示展览，包含走马灯，包含点赞和点进去看看
                exhibit: {
                    img_fit: {
                        'width': '100%',
                        "height": '100%',
                        'object-fit':'cover',
                    },
                    img_container:{
                        "padding": "0px",
                        "width": '100%',
                    },
                    container:{
                        "width": '100%',
                        "height": '100%',
                    },
                    text_container:{
                        "padding": "10px",
                    },
                    exhibit_block:{
                        "min-height": '200px',
                        "height": "100%",
                        "width": "100%",
                        'margin-bottom': '30px',
                    },
                },
            },
            //
            show_modal: false,
            chosen: false,
            // 照片组的列表
            image_history_list: [],
            playing: false,
            display_image_cnt: 0,
            play_timer: null
        }
    },
    methods:{
        start_play(){
            if(this.image_history_list.length==0)
            {
                this.image_group_update(true)
            }
            else{
                this.playing = true
            }
            this.set_autoplay()
        },
        end_play(){
            this.playing = false
            if(this.play_timer!=null)
            {
                clearInterval(this.play_timer)
            }
        },
        handle_touch_play(){
            // 表明不要点击
            this.touch_loop = 0;
            let self = this;
            setTimeout(function () {
                self.touch_loop = 0;
            }, 100);
            if(this.playing)
                this.end_play()
            else
                this.start_play()
        },
        // ==================渲染效果相关函数===============
        handle_click(){
            if(!this.is_phone){
                this.go_to_route()
                this.choose_this_block()
            }
        },
        handle_touch_move(){
            // 手指移动，则表明不要点击
            this.touch_loop = 0;
        },
        handle_touch_start(){
            let self = this;
            //执行长按的内容
            this.handle_mouse_enter();
            self.touch_loop = setTimeout(function () {
                self.touch_loop = 0;
            }, 500);
            return false;
        },
        handle_touch_end(){
            let self = this;
            this.handle_mouse_leave();
            clearTimeout(self.touch_loop);
            //这里click内容，若不移动且小于0.5s
            if (this.touch_loop != 0) {
                this.go_to_route()
                this.choose_this_block()
            }
            return false;
        },
        handle_mouse_enter:function(){
            if(this.state!='exhibit')
                this.show_modal = true
            else{
                this.show_modal = false
            }
            // // 展览中照片加载全套
            // if(this.state == 'photo' || this.state=='auto_photo' || this.onlyinfo)
            // {
            //     if(this.image_history_list.length==0)
            //     {
            //         this.image_group_update()
            //     }
            // }
        },
        handle_mouse_leave:function(){
            if(this.state!='exhibit')
                this.show_modal = false
            else{
                this.show_modal = true
            }
        },

        // ==================功能相关函数===============
        go_to_route: function(){
            if(!this.is_allow_router)
                return
            //用于展示照片时：
            if(this.type == 0)
            {
                if(this.is_progress)
                    this.$router.push({ name: 'repair', params: { id: String(this.id) } })
                else
                    this.$router.push({ name: 'image', params: { id: String(this.id) } })
            }
            //用于展示展览时：
            else
                this.$router.push({ name: 'exhibit', params: { id: String(this.id) } })
        
        },
        // 点赞与取消点赞
        send_like: function(){
            if(this.is_show_like_button==false)
            {
                return
            }
            if(this.liked == false)
            {
                this.liked = true
                this.image_operation(1,'')
            }
            else{
                this.liked = false
                this.image_operation(3,'')
            }
        },
        // 给照片点赞、评论 需要cookie
        image_operation: function(type, content){
            var data = {
                    id:String(this.id),
                    type:String(type),
                    content:content,
                }
            var method = 'POST'
            var url 
            if(this.type == 0)
                url = '/api/photo'
            else
                url = '/api/exhibit'
            // alert(url)
            request_json(data, url, method)
        },
        // 选择该block
        choose_this_block: function(){
            if(this.state=='single_choose')
            {
                // this.chosen = true
                this.$props.add_to_list(this.id, 1)
            }
            if(this.state!='choose')
                return
            if(this.chosen)
            {
                this.chosen = false
                this.$props.add_to_list(this.id, 0)
            }
            else
            {
                this.chosen = true
                this.$props.add_to_list(this.id, 1)
            }
        },
        // 获取整个照片组的信息
        image_group_update: function(need_to_be_true=false){
            var data = {id: String(this.id)}
            var method = 'GET'
            var url = '/api/repair'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                if(object.status!=undefined)
                {
                    console.log(object)
                    my_this.$message.error(object.detail);
                    setTimeout(()=>{
                        my_this.$message.error("无法查看修复动态")
                    },200)
                    return
                }
                if(need_to_be_true)
                    my_this.playing = true
                my_this.image_history_list = object.image_history_list.slice(0,object.image_history_list.length)
                }
            request_json(data,url,method,get_response)
            
        },
        set_autoplay(){
            const my_this = this
            this.play_timer = setInterval(
                function(){
                    if(my_this.image_history_list.length>0)
                    {
                        my_this.display_image_cnt += 1
                        if(my_this.display_image_cnt >= my_this.image_history_list.length)
                            my_this.display_image_cnt = 0
                    }
                },1000
            )
        },
        get_background(url,style="contain"){
            return {
                'background': "url("+url+")",
                'background-position': '50%',
                'background-repeat': 'no-repeat',
                'background-size': style,
            }
        },
    },
    created:function(){
        this.liked = false
        this.chosen = this.is_chosen
        if(this.state!='exhibit')
            this.show_modal = false
        else{
            this.show_modal = true
        }
    },
    computed:{
        is_phone(){
            var info = navigator.userAgent;
            //通过正则表达式的test方法判断是否包含“Mobile”字符串
            var isPhone = /mobile/i.test(info);
            //如果包含“Mobile”（是手机设备）则返回true
            return isPhone
        },
        // 是否有点赞按钮
        is_show_like_button:function(){
            if(this.state=='exhibit' || this.state=='photo')
                return true
            return false
        },
        // 是否有选择按钮
        is_show_choose_button:function(){
            if(this.state=='choose')
                return true
            return false
        },
        // 是否可跳转
        is_allow_router:function(){
            if(this.state=='choose')
                return false
            if(this.state=='drag')
                return false
            if(this.state=='single_choose')
                return false
            return true
        },
        //
        background_img:function(){
            if(this.state == 'photo' || this.state=='exhibit')
                return ""
            return{
                // '-webkit-filter': 'grayscale(100%)',
                'background': 'url('+this.image_src+')',
                'background-repeat': 'no-repeat',
                'background-size':'100% 100%',
                'background-color':'rgba(0,0,0,0.5)',
                // 'opacity': '0.5',
            }
        },

        // 控制选中按钮状态
        button_style:function(){
            if(this.chosen)
            {
                return ""
            }
            return "color:#67C23A;background:white;"
        },
        has_border:function(){
            if(this.chosen==false)
            {
                return ""
            }
            return {
                'border': 'solid',
                'border-color': 'rgb(103, 194, 58)'
            }
        },
        datetime:function () {
			var d = new Date()
			var a = this.timestamp
            if (a < 1000000000000)
			{
				a *= 1000
			}
			d.setTime(a)
			return d.toLocaleString()
		},

    },
    watch:{
        is_chosen:function(){
            this.chosen = this.is_chosen
        },
        playing_props(){
            if(this.playing_props)
            {
                if(this.image_history_list.length==0)
                {
                    this.image_group_update()
                }
            }
        }
    },
    mounted(){
        // $('*').on('touchstart', function(){
        //     $(this).trigger('hover');
        // }).on('touchend', function(){
        // // $(this).
        // });
    },
}
</script>

<style scoped>
    #exhibit-block {
        cursor: pointer;
        /* background: white; */
        display: flex;
        margin: auto;
        box-sizing: border-box;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    }

    .main-container {
        position: relative;
        /* height: 100%; */
        width: 100%;
        margin: auto;
        /* background: rgb(255, 255, 255); */
        text-align: right;
        display: inline-block;
        box-sizing: content-box;
    }

    .img-container:hover {
        opacity: 0.8
    }

    .img-container {
        text-align:center;
        display: inline-block;
    }

    .swiper-auto{
        height: 100%;
    }

    .text-modal {
        
        position: relative;
    }

    .button-container{
        width: 100%;
        position: absolute;
        top: 10px;
        right:10px;
        height: 50px;
        padding-left: 5px;
        padding-right: 5px;
        text-align: right;
        z-index: 10;
    }

    .text-container {
        box-sizing: border-box;
        width: 100%;
        position: absolute;
        top: -150px;
        height: 150px;
        padding-left: 5px;
        padding-right: 5px;
        text-align:left;
    }

    .white-text-container{
        padding-left: 5px;
        padding-right: 5px;
        text-align:left;
    }

    .overflow-container{
        height:25%;
        overflow-x:auto;
        white-space: nowrap;
    }

    .hide-container{
        overflow: hidden;
        text-overflow:ellipsis;
        white-space: nowrap;
    }

    .text-modal-wrapper {
        background-color: white;
        opacity: 0.7;
        box-sizing: border-box;
        width: 100%;
        position: absolute;
        top: -150px;
        height: 150px;
        padding-left: 5px;
        padding-right: 5px;
        text-align:left;
    }

    .progress-modal{
        position: relative;
    }

    .progress-container{
        position: absolute;
        top: -200px;
        height: 200px;
        width: 100%;
        text-align: center;
        color: white;
        background: rgba(0, 0, 0, 0.2);
        padding: 30px;
        box-sizing: border-box;
    }

    .progress-container /deep/  .el-progress__text{
        color: white;
        font-size: 200% !important;
        font-weight: bold;
    }

    .introduction-bar{
        height: 40%; 
        overflow-x: hidden;
        overflow-y: auto;
        white-space: normal;
        font-size: 80%;
    }

    .el-footer {
        /* background: rgb(255, 255, 255); */
        margin-bottom: 5px;
        /* display: none; */
    }

    .neccessary-buttons,.optional-buttons {
        margin: 0;
        display: inline-flex;
    }

    .neccessary-buttons{
        width: 80%;
    }

    .optional-buttons{
        width: 10%;
    }

    .neccessary-buttons .el-button {
        border-radius: 0;
        /* border-color: black; */
        margin: auto;
        /* color: black; */
        /* background-color: white; */
    }
    .optional-buttons .el-button {
        border-radius: 200%;
    }

    .el-footer .el-button :hover {
        /* background: black; */
        opacity: 0.8;
        /* color: white; */
    }

    .router-link{
        text-decoration: none;
    }

    .fade-enter-active .fade-leave-active {
        transition: opacity 1s;
    }
    .fade-enter, .fade-leave-active {
        opacity: 0
    }
</style>