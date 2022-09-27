<template>
    <div id="exhibit-page">
        <!-- <el-container> -->
        <el-col :span="12" class="main" :xs="{span:24}">
            <!-- 图片版面 -->
            <ImagePicBoard :user_state="userstate" :image_info="image_info">
            </ImagePicBoard>
        </el-col>
        <el-col :span="11" :xs="{span:24}">
            <el-row style="text-align:left; border-bottom:solid; font-size:150%">
                <b>
                修复进度
                </b>
            </el-row>
            <slide-board :id="id" :image_list="image_history_list" :resolve="get_before_after">
            </slide-board>
            <el-container>
                    <el-main>
                        <el-card style="text-align:left">
                            <el-timeline>
                                <el-timeline-item
                                v-for="(activity, index) in activities"
                                :key="index"
                                :timestamp="datetime(activity.timestamp)"
                                >
                                {{activity.content}}
                                <el-progress v-if="index==2" :percentage="100" :stroke-width="20" :text-inside="true" status="success">
                                </el-progress>
                                <div v-else-if="index==1 && flag==false">
                                    <el-progress :percentage="Number((now_time*100/expect_time).toFixed(1))" :stroke-width="20" :text-inside="true">
                                    </el-progress>
                                    <div class="progress-info">
                                    <el-descriptions class="margin-top" :column="1">
                                    <el-descriptions-item label="正在进行">
                                        {{    operation   }} 操作
                                    </el-descriptions-item>
                                    </el-descriptions>
                                    </div>
                                </div>
                                <div v-else-if="index==0 && expect_time==0">
                                    <el-descriptions class="margin-top" :column="1">
                                    <el-descriptions-item label="已等待时间">
                                        <template slot="label">
                                           已等待时间
                                        </template>
                                        {{  wait_time.toFixed(0) }}秒
                                    </el-descriptions-item>
                                    </el-descriptions>
                                </div>
                                </el-timeline-item>
                            </el-timeline>
                        </el-card>
                    </el-main>
            </el-container>
        </el-col>
        <!-- </el-container> -->
    </div>
</template>

<script>
import SlideBoard from "./SlideBoard.vue"
import ImagePicBoard from './ImagePicBoard.vue'
import {request_json} from '../utils/communication.js'

// 展示修复详情
export default {
    name: "RepairInfoPage",
    components: {
        SlideBoard,
        ImagePicBoard
    },
    props: {
        // 账户
        userstate:{
            type: Object,
            required: true
        },
        // 照片id，从router来
        id: {
            type:String,
            require:true
        },
    },
    data(){
        return {
            activities:[
            ],

            name: "一个名字",
            image_src: "",
            introduction: "修复详情的介绍",
            // TODO:预计完成任务的所需时间、和已进行时间，需要从后端接受
            expected_time: 100,
            now_time: 100,
            wait_time: 0,
            flag: true,
            operation: "增加清晰度",
            image_history_list: [],
            new_img: 0,
            old_img: 1,
            publisher_name: "",
            publisher_id: 0,

            // 自动刷新的指针
            progress_timer: null,
        }
    },
    methods:{
        datetime:function (timestamp) {
			var d = new Date()
			var a = timestamp
            if (a < 1000000000000)
			{
				a *= 1000
			}
			d.setTime(a)
			return d.toLocaleString()
		},
        go_to_route: function(){
            this.$router.push({ name: 'image', params: { id: this.id } })
        },

        repair_info_update: function(){
            var data = {id: String(this.id)}
            var method = 'GET'
            var url = '/api/repair'
            // alert(1)
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
                my_this.image_history_list = object.image_history_list.slice(0,object.image_history_list.length)
                my_this.name = object.name
                my_this.introduction = object.introduction
                my_this.image_src = object.img_src
                my_this.expect_time = Number(object.expect_time)
                my_this.now_time = Number(object.now_time)
                my_this.wait_time = Number(object.wait_time)
                my_this.operation = object.operation
                my_this.flag = object.flag
                my_this.publisher_name = object.publisher_name
                my_this.publisher_id = object.publisher_id
                my_this.update_timeline()
                }
            request_json(data,url,method,get_response)
            
        },

        get_before_after: function(select_list){
            this.new_img = select_list[0]
            this.old_img = select_list[1]
        },

        update_timeline(){
            // 正在排队
            if(this.expect_time==0){
                if(this.activities.length == 0){
                    this.activities.push({
                        content: "排队等待",
                        timestamp: this.image_history_list[0].timestamp
                    })
                }
            }
            // 修复完成
            else if(this.flag){
                if(this.activities.length == 2){
                    this.activities.push({
                        content: "已完成",
                        timestamp: this.image_history_list[this.image_history_list.length-1].timestamp
                    })
                }
                else if(this.activities.length < 2){
                    this.activities = []
                    this.activities.push({
                        content: "排队等待",
                        timestamp: this.image_history_list[0].timestamp
                    })
                    this.activities.push({
                        content: "进行修复",
                        timestamp: this.image_history_list[0].timestamp
                    })
                    this.activities.push({
                        content: "已完成",
                        timestamp: this.image_history_list[this.image_history_list.length-1].timestamp
                    })
                }
            }
            else{
                if(this.activities.length == 1){
                    this.activities.push({
                        content: "进行修复",
                        timestamp: this.image_history_list[0].timestamp
                    })
                }
                else if(this.activities.length < 1){
                    this.activities = []
                    this.activities.push({
                        content: "排队等待",
                        timestamp: this.image_history_list[0].timestamp
                    })
                    this.activities.push({
                        content: "进行修复",
                        timestamp: this.image_history_list[0].timestamp
                    })
                }
            }
        },

        start_timer(){
            const my_this = this
            this.progress_timer = setInterval(function(){
                if(my_this.userstate.user_valid == true)
                    my_this.repair_info_update()
                if(my_this.flag)
                {
                    my_this.end_timer()
                }
            },1000)
        },
        end_timer(){
            clearInterval(this.progress_timer)
            this.progress_timer = null
        }
    },
    beforeRouteEnter(from,to,next){
        next(vm=>{
            vm.start_timer()
        })
    },
    beforeRouteLeave(from,to,next){
        this.end_timer()
        next()
    },
    computed:{
        image_info:function(){
            var object = {
                id: this.id, 
                name: this.name, 
                introduction: this.introduction, 
                img_src: this.new_img.img_src,
                old_img_src: this.old_img.img_src,
                publisher_name: this.publisher_name,
                publisher_id: this.publisher_id,
            }
            if(this.image_history_list.length>0)
            {
                object.timestamp = this.image_history_list[0].timestamp
            }
            return object
        },
    },
    created: function(){
        
        if(this.userstate.user_valid == false)
        {
            this.$message({
                message: '先登陆才能查看',
                type: 'warning'
            })
            this.$router.push({ name: 'image', params: { id: this.id, user_state:this.userstate} })
            return
        }
        this.repair_info_update()
    },
}
</script>

<style scoped>
    #exhibit-page {
        background-color: rgb(220, 220, 220);
        padding:5px;
        min-height:600px;
    }
    @media screen and (min-width: 768px){
        .main{
            margin:20px;
        }
    }
    
    .main {
        background-color: white;
        text-align: left;
        padding: 0px;
        /* 不会自己飘走 */
        position: static; 
    }
    .progress-info {
        margin-top: 10px;
    }
    
</style>