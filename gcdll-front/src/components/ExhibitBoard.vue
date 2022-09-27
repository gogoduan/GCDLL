<template>
    <div id="exhibit-board">
        <div class="board" v-if="exhibit_style=='board'||(column==2&&exhibit_style!='swipe')">
            <el-col :span="24/column-1" :offset="(index==1)?0:1" v-for="index in column" :key="index">
                <exhibit-block
                :state="state" 
                v-for="image in image_list_group[index-1]" 
                :type="type" :id="image.id" :image_src="image.img_src" 
                :key="image.id" :introduction="image.introduction" 
                :display_image_list="image.display_image_list" 
                :name="image.name" :tag_list="image.tag_list"
                :likes="image.likes" :comments="image.comments" 
                :timestamp="image.timestamp">
                </exhibit-block>
            </el-col>
        </div>
        <div class="swipe-container" v-else-if="exhibit_style=='swipe'">
            <div class="modal">
                <div class="modal-header">
                    <el-button type="text info" v-if="background_fit!='cover'" 
                    @click="background_fit='cover';zooming=false;" :disabled="zooming||playing">
                        <el-tooltip content="开启全屏" placement="top">
                        <i class="el-icon-full-screen hover-button">
                        </i>
                        </el-tooltip>
                    </el-button>
                    <el-button type="text info" v-else @click="background_fit='contain'">
                        <el-tooltip content="关闭全屏" placement="top">
                        <i class="el-icon-crop hover-button">
                        </i>
                        </el-tooltip>
                    </el-button>
                    <el-button type="text info" v-if="zooming==false" @click="zooming=true;background_fit='contain';">
                        <el-tooltip content="开启放大模式" placement="top">
                        <i class="el-icon-zoom-in hover-button">
                        </i>
                        </el-tooltip>
                    </el-button>
                    <el-button type="text info" v-else @click="zooming=false">
                        <el-tooltip content="关闭放大模式" placement="top">
                        <a-icon type="zoom-out" class="hover-button"/>
                        </el-tooltip>
                    </el-button>
                    <el-button type="text info" v-if="zooming==false" 
                    @mouseenter.native="playing=true;background_fit='contain';" 
                    @mouseleave.native="playing=false"
                    @touchstart.native.prevent="handle_touch">
                        <el-tooltip content="正在播放" placement="top">
                        <a-icon v-if="playing" type="play-circle" class="hover-button"/>
                        <a-icon v-else type="play-circle" theme="filled" class="hover-button"/>
                        </el-tooltip>
                    </el-button>
                </div>
            </div>
            <div class="swipe">
            <!-- swiper1 -->
            <swiper class="swiper gallery-top" :options="swiperOptionTop" ref="swiperTop">
                <swiper-slide v-for="image,index in image_list" :key="image.id" 
                    :style="get_background(image.img_src,background_fit)"
                    class="slide-1">
                    <exhibit-block v-if="zooming==false"
                    :state="'sketch'"
                    :onlyinfo="true" :playing_props="check_playing(index)"
                    :type="type" :id="image.id" :image_src="image.img_src" 
                    :introduction="image.introduction" 
                    :display_image_list="image.display_image_list" 
                    :name="image.name" :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
                    <div class="swiper-zoom-container" v-else>
                        <el-tooltip content="双击放大" placement="top">
                        <img :src="image.img_src">
                        </el-tooltip>
                    </div>
                </swiper-slide>
            <div class="swiper-button-next swiper-button-white" slot="button-next"></div>
            <div class="swiper-button-prev swiper-button-white" slot="button-prev"></div>
            </swiper>
            <!-- swiper2 Thumbs -->
            <swiper class="swiper gallery-thumbs" :options="swiperOptionThumbs" ref="swiperThumbs">
                <swiper-slide v-for="image in image_list" :key="image.id" 
                    :style="get_background(image.img_src,'cover')"
                    class="slide-1">
                </swiper-slide>
            </swiper>
            </div>
        </div>
        <div class="board" v-else-if="exhibit_style=='rank-left'">
            <el-row v-if="image_list.length!=0" style="height:500px">
                <el-col class="hover-item" style="height:100%" :span="24/(Math.floor(image_list.length/2)+1)">
                    <exhibit-block 
                    :state="state" 
                    v-for="image in image_list.slice(0,1)" 
                    :type="type" :id="image.id" :image_src="image.img_src" 
                    :key="image.id" :introduction="image.introduction" 
                    :display_image_list="image.display_image_list" 
                    :name="image.name" :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
                </el-col>
                <el-col style="height:100%" :span="24-24/(Math.floor(image_list.length/2)+1)">
                    <el-row style="height:50%">
                        <el-col class="hover-item" style="height:100%" :span="24/Math.floor(image_list.length/2)" 
                        :key="image.id"
                        v-for="image in image_list.slice(1,Math.floor(image_list.length/2)+1)"> 
                        <exhibit-block  
                        :state="state" 
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :introduction="image.introduction" 
                        :display_image_list="image.display_image_list" 
                        :name="image.name" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments" 
                        :timestamp="image.timestamp">
                        </exhibit-block>
                        </el-col>
                    </el-row>
                    <el-row style="height:50%">
                        <el-col class="hover-item" style="height:100%" :span="24/Math.floor(image_list.length/2)" 
                        :key="image.id"
                        v-for="image in image_list.slice(Math.floor(image_list.length/2)+1,image_list.length)"> 
                        <exhibit-block 
                        :state="state" 
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :introduction="image.introduction" 
                        :display_image_list="image.display_image_list" 
                        :name="image.name" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments" 
                        :timestamp="image.timestamp">
                        </exhibit-block>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-empty v-else description="暂时没有展览"></el-empty>
        </div>
        <div class="board" v-else-if="exhibit_style=='rank'">
            <el-row v-for="index in Math.floor(image_list.length/12)" :key="index">
            <el-row  style="height:500px">
                <el-col class="hover-item" style="height:100%" :span="24/(Math.floor(5/2)+1)">
                    <exhibit-block 
                    :state="state" 
                    v-for="image in image_list.slice((index-1)*12,(index-1)*12 + 1)" 
                    :type="type" :id="image.id" :image_src="image.img_src" 
                    :key="image.id" :introduction="image.introduction" 
                    :display_image_list="image.display_image_list" 
                    :name="image.name" :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
                </el-col>
                <el-col style="height:100%" :span="24-24/(Math.floor(5/2)+1)">
                    <el-row style="height:50%">
                        <el-col class="hover-item" style="height:100%" :span="24/Math.floor(5/2)" 
                        :key="image.id"
                        v-for="image in image_list.slice((index-1)*12 + 1,(index-1)*12 + Math.floor(5/2)+1)"> 
                        <exhibit-block 
                        :state="state" 
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :introduction="image.introduction" 
                        :display_image_list="image.display_image_list" 
                        :name="image.name" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments" 
                        :timestamp="image.timestamp">
                        </exhibit-block>
                        </el-col>
                    </el-row>
                    <el-row style="height:50%">
                        <el-col class="hover-item" style="height:100%" :span="24/Math.floor(5/2)" 
                        :key="image.id"
                        v-for="image in image_list.slice((index-1)*12 + Math.floor(5/2)+1,(index-1)*12 + 5)"> 
                        <exhibit-block 
                        :state="state" 
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :introduction="image.introduction" 
                        :display_image_list="image.display_image_list" 
                        :name="image.name" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments" 
                        :timestamp="image.timestamp">
                        </exhibit-block>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row  style="height:500px">
                <el-col style="height:100%" :span="24-24/(Math.floor(7/2)+1)">
                    <el-row style="height:50%">
                        <el-col class="hover-item" style="height:100%" :span="24/Math.floor(7/2)" 
                        :key="image.id"
                        v-for="image in image_list.slice((index-1)*12 + 1 + 5,(index-1)*12 + Math.floor(7/2)+1 +5 )"> 
                        <exhibit-block 
                        :state="state" 
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :introduction="image.introduction" 
                        :display_image_list="image.display_image_list" 
                        :name="image.name" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments" 
                        :timestamp="image.timestamp">
                        </exhibit-block>
                        </el-col>
                    </el-row>
                    <el-row style="height:50%">
                        <el-col class="hover-item" style="height:100%" :span="24/Math.floor(7/2)" 
                        :key="image.id"
                        v-for="image in image_list.slice((index-1)*12 + 5 + Math.floor(7/2)+1,(index-1)*12 + 7  + 5)"> 
                        <exhibit-block  
                        :state="state" 
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :introduction="image.introduction" 
                        :display_image_list="image.display_image_list" 
                        :name="image.name" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments" 
                        :timestamp="image.timestamp">
                        </exhibit-block>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col class="hover-item" style="height:100%" :span="24/(Math.floor(7/2)+1)">
                    <exhibit-block  
                    :state="state" 
                    v-for="image in image_list.slice((index-1)*12 + 5,(index-1)*12 + 1  + 5)" 
                    :type="type" :id="image.id" :image_src="image.img_src" 
                    :key="image.id" :introduction="image.introduction" 
                    :display_image_list="image.display_image_list" 
                    :name="image.name" :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
                </el-col>
            </el-row>
            </el-row>
            <el-col class="hover-item" style="height:300px" 
            :span="cross_span[(index%6)]"
            v-for="image,index in image_list.slice(Math.floor(image_list.length/12)*12,image_list.length)" :key="image.id">
                    <exhibit-block 
                    :state="state" 
                    
                    :type="type" :id="image.id" :image_src="image.img_src" 
                    :key="image.id" :introduction="image.introduction" 
                    :display_image_list="image.display_image_list" 
                    :name="image.name" :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
            </el-col>
        </div>
        <div class="board" v-else-if="exhibit_style=='cross'">
            <el-col class="hover-item" style="height:300px" 
            :span="cross_span[(index%6)]"
            v-for="image,index in image_list" :key="index">
                    <exhibit-block 
                    :state="state" 
                    
                    :type="type" :id="image.id" :image_src="image.img_src" 
                    :key="image.id" :introduction="image.introduction" 
                    :display_image_list="image.display_image_list" 
                    :name="image.name" :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
            </el-col>
        </div>
        <div class="slide-bar" v-else-if="exhibit_style=='slide'" style="width:100%">
                <!-- <el-skeleton v-if="loading" style="" animated :count="3">
                    <template slot="template">
                        <div class="hover-item image-item" style="background:white">
                        <el-skeleton-item variant="image" style="margin:5%;width: 90%; height: 90%" />
                        </div>
                    </template>
                </el-skeleton> -->
                    <div class="image-item hover-item" v-for="image in image_list" :key="image.id" >
                            <ExhibitBlock  :type=1 :id="image.id" 
                            :name="image.name" :image_src="image.img_src" 
                            :introduction="image.introduction" 
                            :timestamp="image.timestamp" :tag_list="image.tag_list"
                            :likes="image.likes" :comments="image.comments"
                            state="exhibit">
                            </ExhibitBlock>
                    </div>
        </div>
    </div>
</template>

<script>
import ExhibitBlock from './ExhibitBlock.vue'
import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'

// 管理多张照片的版面
export default {
    name: "ExhibitBoard",
    components: {
        ExhibitBlock,
        Swiper,
        SwiperSlide
    },
    props: {
        exhibit_style:{
            type: String,
            required:true,
        },
        // 走马灯里展示的样例照片
        display_image_list: {
            type: Array, 
        },
        // 0-照片 1-展览
        type: {
            type:Number,
            default: 0,
        },
        state: {
            type: String,
            require: true,
        },
        image_list: {
            type: Array,
			default: () => new Array(2).fill({
                id: 10,
                name: "名字",
                likes: 10,
                comments: 100,
				introduction: "这张照片拍摄于1900年......",
				img_src: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdesk-fd.zol-img.com.cn%2Ft_s960x600c5%2Fg5%2FM00%2F02%2F05%2FChMkJ1bKyaOIB1YfAAusnvE99Z8AALIQQPgER4AC6y2052.jpg&refer=http%3A%2F%2Fdesk-fd.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1649854587&t=a5f1e9e174a7316000f9488d6365590d"
			})
        },
        column:{
            type: Number,
            default: 4,
        }
    },
    data(){
        return {
            swiperOptionTop: {
                // loop: true,
                zoom: true,
                // slidesPerView: 'auto',
                // loopedSlides: 5, // looped slides should be the same
                spaceBetween: 10,
                // pagination: {
                //     el: '.swiper-pagination',
                //     type: 'progressbar'
                // },
                // 允许键盘滑动
                keyboard: {
                    enabled: true,
                },
                //允许触控板滑动
                mousewheel: true,
                //允许抓取滑动
                // grabCursor: true,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev'
                }
            },
            swiperOptionThumbs: {
                // loop: true,
                // loopedSlides: 5, // looped slides should be the same
                spaceBetween: 10,
                centeredSlides: true,
                slidesPerView: 'auto',
                touchRatio: 0.2,
                slideToClickedSlide: true
            },
            background_fit:'contain',
            playing:false,
            zooming:false,

            cross_span:[7,9,8,9,8,7,8],
        }
    },
    methods:{
        check_playing(index){
            // console.log(this.$refs.swiperTop.$swiper.activeIndex,index)
            try{
                if(index==this.$refs.swiperTop.$swiper.activeIndex)
                    if(this.playing)
                        return true
            }catch{
                return false
            }
            return false
        },
        handle_touch(){
            if(this.playing)
            {
                this.playing = false
            }
            else{
                this.playing=true;
                this.background_fit='contain';
            }
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
    computed:{
        image_list_group: function(){
            var group = []
            for(var j = 0;j<this.column;j+=1)
            {
                group.push([])
            }
            for(var i=0;i<this.image_list.length;i+=1)
            {
                group[i%this.column].push(this.image_list[i])
            }
            return group
        },
    },
    mounted(){
        const my_this = this
        this.$nextTick(() => {
            if(my_this.exhibit_style!='swipe')
                return
            const swiperTop = my_this.$refs.swiperTop.$swiper
            const swiperThumbs = my_this.$refs.swiperThumbs.$swiper
            swiperTop.controller.control = swiperThumbs
            swiperThumbs.controller.control = swiperTop
        })
    },
    watch:{
        exhibit_style(){
            const my_this = this
            this.$nextTick(() => {
                if(my_this.exhibit_style!='swipe')
                    return
                const swiperTop = my_this.$refs.swiperTop.$swiper
                const swiperThumbs = my_this.$refs.swiperThumbs.$swiper
                swiperTop.controller.control = swiperThumbs
                swiperThumbs.controller.control = swiperTop
            })
        }
    }
}
</script>

<style scoped>
    #exhibit-board {
        display: flex;
        align-content: space-between;
    }

    .board{
        width:100%;
        padding:10px;
        /* padding-left:30px; */
    }

    .swipe-container .el-row {
        display: inline-block;
        padding: 5px;
        width:90%;
        max-width: 1000px;
        background-color: black;
    }

    .modal{
        margin:auto;
        position:relative;
        width:90%;
        max-width: 1000px;
    }

    .modal-header{
        position:absolute;
        z-index:2;
        right:10px;
        top:0;
    }

    .modal-header .el-button{
        float:right;
        color:white;
        font-size:200%;
    }

    .hover-button:hover{
        color:grey;
        opacity: 0.8;
    }

    .swipe-container{
        width:100%;
    }

    .swipe {
        width:90%;
        max-width: 1000px;
        height: 480px;
        margin:auto;
        background-color: black;
    }

        .gallery-top {
        height: 80%;
        width: 100%;
        }
        .gallery-thumbs {
        height: 20%;
        box-sizing: border-box;
        padding: gap 0;
        }
        .gallery-thumbs .swiper-slide {
        width: 25%;
        height: 100%;
        opacity: 0.4;
        }
        .gallery-thumbs .swiper-slide-active {
        opacity: 1;
        }


        .hover-item{
            padding:10px;
            transition: 0.3s ease-out;
        }

        .hover-item:hover{
            padding:2px;
        }

        .image-item {
            display: inline-block;  /* 横向滚动 */
            height: 300px;
            width: 400px;
            float: none;
        }
        .slide-bar {
            height: 300px;
            /* 沿x轴滑动查看照片 */
            white-space: nowrap;
            /* justify-content: space-between; */
            overflow-y: hidden;
            overflow-x: auto;
        }
</style>
