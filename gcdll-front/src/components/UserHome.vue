<template>
    <div class="user-home">
        <el-carousel :interval="5000" arrow="always" height="350px">
            <el-carousel-item v-for="image,index in image_example_list" :key="image.id">
                <el-col :span="12" class="compare-container-bar" :style="[get_background(image.old_img_src)]"  >
                    <div style="height:100%" @click="go_to_tag_search(index)">
                    </div>
                </el-col>
                <el-col :span="12" class="compare-container-bar" :style="[get_background(image.img_src)]">
                    <div style="height:100%" @click="go_to_tag_search(index)">
                    </div>
                </el-col>
            </el-carousel-item>
        </el-carousel>
        <div style="position:relative">
            <div class="modal-title">
                <div style="margin:auto; background: gray; width:200px; border-radius: 10px">
                <b style="font-size: 200%; color:white">
                    AI REPAIR
                </b>
                </div>
            </div>
        </div>
        <el-container>
            <el-main>
        <div class="recommend-bar">
            <div class="title-recommend-bar">
                <span style="font-size: 200%;">
                    近期热门
                </span>
            </div>
            <el-divider>
            </el-divider>
            <exhibit-board :image_list="display_list['like']" :state="'exhibit'" :exhibit_style="(page_width<768)?'slide':'rank-left'" :type="1">
            </exhibit-board>
        </div>

        <div class="recommend-bar">
            <div class="title-recommend-bar">
                <span style="font-size: 200%;">
                    最新发布
                </span>
            </div>
            <el-divider>
            </el-divider>
            <exhibit-board :image_list="display_list['time']" :state="'exhibit'" :exhibit_style="(page_width<768)?'slide':'rank-left'" :type="1">
            </exhibit-board>
        </div>
            </el-main>
        </el-container>
    </div>
</template>

<script>
// import ExhibitBoard from './ExhibitBoard.vue'
// import ExhibitBlock from './ExhibitBlock.vue'
import {request_json} from '@/utils/communication.js'
import ExhibitBoard from './ExhibitBoard.vue'

// 游客默认主页
export default {
    name: "UserHome",
    components: {
        // ExhibitBlock,
        ExhibitBoard,
        // ExhibitBoard
    },
    props: {
        // TODO: 游客主页信息
        page_width:{
            type:Number,
            required:true,
        },
        // 账户
        userstate:{
            type: Object,
            required: true
        },
    },
    data(){
        return {
            loading:true,
            // 照片样例
            image_example_tag_list:[],
            image_example_list: [
            ],
            top:[],
            // 展览集
            exhibit_list:[], 
            display_list:{
                time: [],
                like: []
            }
        }
    },
    methods:{
        //从后端要信息
        user_home_update: function(){
            var data = 1
            var method = 'GET'
            var url = '/api/home'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                my_this.exhibit_list = object
                my_this.loading = false
            }
            request_json(data,url,method,get_response)
        },

        update_best_photo: function(amount,order){
            var data = {
                type: 'exhibit', //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: [
                    {
                        tag: [],
                    }
                ],
                unique: true,
                page: this.fixing_current_page,
                amount: amount, // 数字：返回多少条信息,不存在该key则全部返回
                order_name: order, 
                order_method: false,
            }
            var method = 'POST'
            var url = '/api/search'
            const my_this = this
            // alert(JSON.stringify(data))
            var get_response = function (res) { 
                var response = res
                var object = response.data.mes
                // console.log("receive: "+object)
                my_this.display_list[order] = object
            }
            request_json(data,url,method,get_response)
        },

        image_example_update: function(id,tag){
            var data = {id:id}
            var method = 'GET'
            var url = '/api/photo'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                my_this.image_example_list.push(object)
                my_this.image_example_tag_list.push(tag)
                console.log(object)
            }
            request_json(data,url,method,get_response)
        },

        get_tag_photo: function(tag){
            var data = {
                type: 'photo', //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: [
                    {
                        tag: [tag],
                    }
                ],
                amount: "1", // 数字：返回多少条信息,不存在该key则全部返回
                unique: true,
                order_name: 'time', 
                order_method: false,
            }
            var method = 'POST'
            var url = '/api/search'
            const my_this = this
            // alert(JSON.stringify(data))
            var get_response = function (res) { 
                var response = res
                var object = response.data.mes
                // console.log("receive: "+object)
                if(object.length>0)
                    my_this.image_example_update(object[0].id,tag)
            }
            request_json(data,url,method,get_response)
        },

        get_background(url){
            return {
                'background': "url("+url+")",
                'background-position': '50%',
                'background-repeat': 'no-repeat',
                'background-size': 'cover'
            }
        },

        go_to_tag_search(index){
            var tag = this.image_example_tag_list[index]
            
            this.$router.push({name:"search", params:{
                    ex_keyword: tag,
                    ex_scope: 'photo',
                    is_adv: true,
                }})
        },
    },
    created: function(){
        this.user_home_update()
        this.update_best_photo(5,'time')
        this.update_best_photo(7,'like')
        
        this.get_tag_photo('人像')
        this.get_tag_photo('风景')
        this.get_tag_photo('物件')
        this.get_tag_photo('建筑')
        this.get_tag_photo('动物')
    },
}
</script>

<style scoped>
    .compare-container-bar{
        width: 50%;
        height: 100%;
        cursor: pointer;
    }

    .compare-container-bar:hover{
        opacity: 0.8;
    }

    .modal-title{
        position: absolute;
        top: -100px;
        height: 50px;
        width: 100%;
        z-index: 2;
    }
    .recommend-bar{
        width: 90%;
        margin-left: 5%;
        margin-right: 5%;
        margin-top: 20px;
    }

    .hover-item{
        width:400px;
        height: 300px;
        margin-top: 20px;
        transition: 0.3s ease-out;
    }

    .hover-item:hover{
        margin-left: 0px;
        margin-right: 0px;
        margin-top: 10px;
        width:420px;
        height: 310px;
    }

    .el-container {
        height: auto;
        /* background-color: rgb(220, 220, 220) */
    }

    .el-main {
        height: auto;
        overflow: hidden;
    }
</style>