<template>
    <div id="slide-board">
        <div class="image-container">
                <div class="image-item" v-for="image,index in image_list" :key="image.id" >
                    <el-col :span="20">
                    <div class="item-box">
                        <exhibit-block  :id="image.id" 
                        :add_to_list="add_to_list" :is_chosen="Boolean(chosen_list[index])"
                        :timestamp="image.timestamp" :tag_list="image.tag_list"
                        :likes="image.likes" :comments="image.comments"
                        :name="String(image.id)" :image_src="get_random_src(image.img_src)" :introduction="image.introduction" state="choose">
                        </exhibit-block>
                        <div class="tag-modal" v-if="chosen_list[index]==true">
                            <div class="compare-tag-bar">
                                <el-row style="background: rgb(103, 194, 58); font-size: 150%;">
                                    <span v-if="is_before(index)">
                                        修复前
                                    </span>
                                    <span v-else>
                                        修复后
                                    </span>
                                </el-row>
                            </div>
                        </div>
                    </div>
                    </el-col>
                    <el-col class="center-align-box" :span="4">
                        <i class="el-icon-arrow-right">
                        </i>
                    </el-col>
                </div>
                <el-empty v-if="image_list.length==0" description="暂时没有内容"></el-empty>
            </div>
        
        
    </div>
</template>

<script>
import ExhibitBlock from './ExhibitBlock.vue'
// 滑动展示多张照片的版面
export default {
    name: "SlideBoard",
    components: {
        ExhibitBlock,
    },
    props: {
        // 照片id，从router来
        id: {
            type:String,
            require:true
        },
        image_list: {
            type: Array,
			default: () => new Array(0)
        },
        // 回调函数，将参数赋给。。。
        resolve:{
            type: Function,
            default: function(){}
        },
    },
    data(){
        return {
            chosen_cnt: 0,
            chosen_list: [],
            select_list: [],
            request_id: 0,
        }
    },
    methods:{
        add_to_list:function(id, add){
            for(var i = 0;i < this.image_list.length;i+=1)
            {
                if(this.image_list[i].id == id)
                {
                    if(add)
                    {
                        if(this.chosen_cnt==2)
                        {
                            for(var j = 0;j < this.image_list.length;j+=1)
                            {
                                if(i+j < this.image_list.length)
                                {
                                    if(this.chosen_list[i+j] == 1)
                                    {
                                        // IMPORTANT: 使用splice来让vue检测到list的改变
                                        this.chosen_list.splice(i+j, 1, 0)
                                        // this.chosen_list[i+j] = 0
                                        break
                                    }
                                }
                                if(i-j >= 0)
                                {
                                    if(this.chosen_list[i-j] == 1)
                                    {
                                        this.chosen_list.splice(i-j, 1, 0)
                                        break
                                    }
                                }
                            }
                        }
                        else
                            this.chosen_cnt += 1
                    }
                    else
                        this.chosen_cnt -= 1
                    this.chosen_list.splice(i, 1, add)
                }
            }
            this.confirm()
        },
        confirm:function(){
            this.select_list = []
            for(var i = 0;i < this.image_list.length;i+=1)
            {
                if(this.chosen_list[i] == 1)
                    this.select_list.push(this.image_list[i])
            }
            if(this.chosen_cnt==2)
                this.resolve(this.select_list)
            // alert(JSON.stringify(this.chosen_list))
        },
        is_before:function(index){
            for(let i=index+1;i<this.chosen_list.length;i+=1)
            {
                if(this.chosen_list[i]==1)
                {
                    return 1
                }
            }
            return 0
        },
        get_random_src(src){
            return src+"?id="+String(this.request_id)
        },
    },
    created(){
    },
    watch:{
        image_list(){
            if(this.image_list.length==0)
                return
            this.request_id += 1;
            if(this.chosen_cnt!=0)
                return
            this.chosen_list = new Array(this.image_list.length).fill(0)
            this.chosen_list.splice(0, 1, 1)
            this.chosen_list.splice(this.image_list.length-1, 1, 1)
            this.chosen_cnt = 2
            this.confirm()
        }
    },
    computed:{
        
    }
}
</script>

<style scoped>
    #slide-board {
        background-color: rgb(200, 200, 200);
        padding: 10px;
    }

    .image-container {
        white-space: nowrap;
        justify-content: space-between;
        overflow-y: hidden;
        overflow-x: auto;
        
    }

    .tag-modal{
        position: relative;
    }

    .compare-tag-bar{
        position: absolute;
        width: 200px;
        /* top: -100px; */
        left: -200px;
    }

    .image-item {
        display: inline-block;  /* 横向滚动 */
        height: 220px;
        width: 250px;
        float: none;
        /* margin: 10px; */
        padding: 0;
    }

    .item-box {
        height: 200px;
        width: 200px;
        /* margin: 5px; */
    }

    .center-align-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height:100%;
    }

    i {
        font-size: 300%;
        margin: auto;
    }

</style>

<style>
/* 滚动条设置 */
    ::-webkit-scrollbar {
        width:5px;
        height:5px;
        background: rgb(230, 230, 230);
    }

    ::-webkit-scrollbar-track {
        width:5px;
        height:5px;
        border-radius: 0px;
    }

    ::-webkit-scrollbar-thumb {
        width: 10px;
        background: rgb(200, 200, 200);
    }

    ::-webkit-scrollbar-button {
        border-radius: 0px;
    }

    * {
        outline:none;
        scrollbar-width: thin;
    }
</style>