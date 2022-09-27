<template>
    <div id="exhibit-edit-page">
            <el-row style="height: 400px">
                <el-col :span="14" style="height:100%">
                    <upload-cover :title="'展览封面管理'"
                    :resolve="get_cover" :origin_cover="get_random_src(exhibit_info.img_src)"/>
                </el-col>
                <el-col :span="8" :offset="1" style="height:100%">
                    <el-card style="height:80%">
                        <div slot="header" class="clearfix edit-title">
                            展览简介管理
                        </div>
                        <div class="introduction-container">
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
                        </div>
                    </el-card>
                </el-col>
                
            </el-row>
            <el-card>
                <div slot="header" class="clearfix edit-title">
                    <span>展览内部照片</span>
                </div>
                <el-col :span="20">
                    <search-page :resolve="get_selected_photos" :exhibit_id="Number(id)"
                     :type="0" state="choose" range="photo" :is_filter="true"
                     height="600px">
                    </search-page>
                </el-col>
                <el-col :span="1" style="height:200px">
                    <div class="border">
                    </div>
                </el-col>
                <el-col :span="3">
                    <div class="info-container">
                        <el-row>
                            <el-row>
                                <el-button type="success" circle size="medium" @click="choose_dialog_visible = true">
                                    <i class="el-icon-plus big-icon">
                                    </i>
                                </el-button>
                            </el-row>
                            <el-row style="font-size:80%">
                                添加照片
                            </el-row>
                        </el-row>
                        <el-row>
                            <el-row>
                                <el-button type="success" circle size="medium" @click="order_dialog_visible = true">
                                    <i class="el-icon-refresh big-icon">
                                    </i>
                                </el-button>
                            </el-row>
                            <el-row style="font-size:80%">
                                更改照片顺序
                            </el-row>
                        </el-row>
                        <el-row>
                            <el-row>
                                <el-button type="success" circle size="medium" @click="style_dialog_visible = true">
                                    <i class="el-icon-menu big-icon">
                                    </i>
                                </el-button>
                            </el-row>
                            <el-row style="font-size:80%">
                                更改布局
                            </el-row>
                        </el-row>
                    </div>
                </el-col>
            </el-card>
        <!-- 确认删除 -->
        <el-dialog
            title="操作"
            :visible.sync="dialogVisible"
            width="600px">
                                        <el-table :data="select_list" style="max-height:300px;overflow:auto;">
                                            <el-table-column width="50" property="id" label="ID"></el-table-column>
                                            <el-table-column width="250" property="name" label="标题"></el-table-column>
                                            <el-table-column width="300" property="introduction" label="简介"></el-table-column>
                                        </el-table>
        <span slot="footer" class="dialog-footer">
            <el-button type="danger" @click="before_delete_all">
                删除所有
            </el-button>
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
        </el-dialog>
        <!-- 选择加入的新照片 -->
        <el-dialog  title="照片库" :visible.sync="choose_dialog_visible" height="600px" width="1200px" :fullscreen="fullscreen">
            <span slot="title">
                <b style="font-size:150%;">
                    照片库
                </b>
                <el-button type="text" style="font-size:150%;color:grey;float:left" @click="fullscreen=!fullscreen">
                    <a-icon v-if="!fullscreen" type="fullscreen" />
                    <a-icon v-else type="fullscreen-exit" />
                </el-button>
            </span>
            <SearchPage
            :type="0"
            state = "choose"
            range = "photo"
            :height="fullscreen?'600px':'400px'"
            :resolve="add_photo_to_exhibit"
            >
            </SearchPage>
        </el-dialog>
        <!-- 选择照片顺序 -->
        <el-dialog :visible.sync="order_dialog_visible" height="400px" width="1200px" top="50px"
        title="拖动更改顺序" :fullscreen="fullscreen">
            <span slot="title">
                <b style="font-size:150%;">
                    拖动更改顺序
                </b>
                <el-button type="text" style="font-size:150%;color:grey;float:left" @click="fullscreen=!fullscreen">
                    <a-icon v-if="!fullscreen" type="fullscreen" />
                    <a-icon v-else type="fullscreen-exit" />
                </el-button>
            </span>
            <OrderManageBoard :height="fullscreen?'500px':'400px'" 
            :myArray="image_list" :resolve="change_order" :exhibit_style="exhibit_style">
            </OrderManageBoard>
        </el-dialog>
        <!-- 选择展览布局 -->
        <el-dialog title="选择布局" :visible.sync="style_dialog_visible" width="80%" fullscreen>
            <div class="example-container">
                <exhibit-board :exhibit_style="exhibit_style" :type="0"
                 :image_list="image_list" :state="my_state"/>
            </div>
            <span slot="footer" class="dialog-footer" style="margin-top:10px">
                <el-row>
                <el-col :span="16">
                    <el-radio-group v-model="exhibit_style">
                        <el-radio border v-for="style in style_options" :key="style.label" :label="style.label"
                        style="padding:10px">
                            <a-icon :type="style.icon" style="font-size:200%"/>
                            <span style="margin:3px">{{style.name}}</span>
                        </el-radio>
                    </el-radio-group>
                </el-col>
                <el-col :span="8">
                <el-button @click="style_dialog_visible = false">取 消</el-button>
                <el-button type="primary" @click="change_exhibit_style();style_dialog_visible = false">确定修改</el-button>
                </el-col>
                </el-row>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import OrderManageBoard from './OrderManageBoard.vue'
import SearchPage from './SearchPage.vue'
import ExhibitBoard from './ExhibitBoard.vue'
import UploadCover from './UploadCover.vue'
import {request_json} from '@/utils/communication.js'

// 展览页面
export default {
    name: "ExhibitEditPage",
    components: {
        OrderManageBoard,
        SearchPage,
        UploadCover,
        ExhibitBoard
    },
    props: {
        // 展览id，从router来
        id: {
            type:String,
            require:true
        },

    },
    data(){
        return {
            fullscreen: false,
            show_modal: false,
            cover_list: [],
            base_list: [],

            dialogVisible:false,
            choose_dialog_visible:false,
            order_dialog_visible:false,
            style_dialog_visible:false,
            select_list:[],

            exhibit_style:'board',
            style_options:[
                {
                    label: 'swipe',
                    name: '滑动',
                    icon: 'pic-center'
                },
                {
                    label: 'board',
                    name: '展板',
                    icon: 'project'
                },
                {
                    label: 'rank',
                    name: '重点',
                    icon: 'pic-left'
                },
                {
                    label: 'cross',
                    name: '错落',
                    icon: 'block'
                },
            ],

            cover_type:'upload',

            //展览信息
            exhibit_info: { 
                id: "展览id", 
                name: "展览名字", 
                introduction: "这是⼀个关于⻛景的展览", 
                timestamp: "1000000000000", 
                img_src: 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdesk-fd.zol-img.com.cn%2Ft_s960x600c5%2Fg5%2FM00%2F02%2F05%2FChMkJ1bKyaOIB1YfAAusnvE99Z8AALIQQPgER4AC6y2052.jpg&refer=http%3A%2F%2Fdesk-fd.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1649854587&t=a5f1e9e174a7316000f9488d6365590d', 
                comments: "109", 
                likes: "3534", 
                style: "board",
                },
            // 展览中照片集
            image_list: Array(20).fill({
                id: 10,
                name: "名字",
                comments: "109", 
                likes: "3534", 
				introduction: "这张照片拍摄于1900年......",
				img_src: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fphoto.tuchong.com%2F2301431%2Ff%2F45600443.jpg&refer=http%3A%2F%2Fphoto.tuchong.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1652157610&t=e13845787a08fdf534dc09af50a26943"
			}),
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
        get_random_src(url){
            return url + "?id=" + Math.random()
        },
        get_cover(res){
            this.cover_type = res.type
                if(res.type=='upload')
                {
                    this.base_list = res.data
                }
                else
                {
                    this.cover_list = res.data
                }
                this.change_cover()
        },

        //从后端要信息
        exhibit_update: function(){
            var data = {id: String(this.id)}
            var method = 'GET'
            var url = '/api/exhibit'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                my_this.image_list = object.img_list
                my_this.exhibit_info = object.exhibit_info
                my_this.exhibit_style = object.exhibit_info.style
            }
            request_json(data,url,method,get_response)
            
        },
        get_selected_photos(res){
            this.select_list = res
            this.dialogVisible = true
        },
        before_delete_all(){
            const my_this=this
            this.$confirm('确认将所有选中从展览中删除？')
            .then(function(){
                if(my_this.select_list.length!=0)
                {
                    my_this.delete_photo_from_exhibit(my_this.select_list)
                }
                my_this.dialogVisible=false;
            })
        },
        // 向展览加入照片
        add_photo_to_exhibit(res){
            if(res.length == 0)
            {
                const my_this = this
                this.$confirm('未选中任何照片，是否退出').then(function(){
                my_this.choose_dialog_visible=false;
                })
                return
            }
            this.choose_dialog_visible = false
            var postlist = []
            for(var i = 0; i < res.length; i += 1){
                postlist.push(res[i].id);
            }
            var data = {
                add: true,
                id: this.id,
                postlist: postlist,
            }
            // console.log(data)
            var method = 'POST'
            var url = '/api/exhibit_edit'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                    {
                        console.log(object)
                        my_this.$message.error(object.detail);
                        return
                    }
                my_this.$message({
                    message:'添加成功',
                    type:'success'
                    })
                my_this.exhibit_update()
            }
            request_json(data,url,method,get_response)
        },
        delete_photo_from_exhibit(res){
            var postlist = []
            for(var i = 0; i < res.length; i += 1){
                postlist.push(res[i].id);
            }
            var data = {
                delete: true,
                id: this.id,
                postlist: postlist,
            }
            // console.log(data)
            var method = 'POST'
            var url = '/api/exhibit_edit'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                    {
                        console.log(object)
                        my_this.$message.error(object.detail);
                        return
                    }
                my_this.$message({
                    message:'删除成功',
                    type:'success'
                    })
                my_this.exhibit_update()
            }
            request_json(data,url,method,get_response)
        },

        // 更换展览封面
        change_cover(){
            this.$message({
                message:"正在更换封面"
            })
            var data = {
                cover: true,
                id: this.id,
            }
            if(this.base_list.length > 0)
            {
                data.cover_src = this.base_list[0]
            }
            if(this.cover_list.length > 0)
            {
                data.cover_id = this.cover_list[0]
            }
            var method = 'POST'
            var url = '/api/exhibit_edit'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                    {
                        console.log(object)
                        my_this.$message.error(object.detail);
                        return
                    }
                my_this.$message({
                    message:'封面更换成功',
                    type:'success'
                    })
                my_this.base_list = []
                my_this.cover_list = []
                my_this.exhibit_update()
            }
            request_json(data,url,method,get_response)
        },
        // 更换展览风格
        change_exhibit_style(){
            this.$message({
                message:"正在更换展览样式"
            })
            var data = {
                style: true,
                id: this.id,
                style_name: this.exhibit_style,
            }
            var method = 'POST'
            var url = '/api/exhibit_edit'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                    {
                        console.log(object)
                        my_this.$message.error(object.detail);
                        return
                    }
                my_this.$message({
                    message:'展览样式更换成功',
                    type:'success'
                    })
                my_this.exhibit_update()
            }
            request_json(data,url,method,get_response)
        },
        
        // 更换展览顺序
        change_order(res){
            this.order_dialog_visible = false
            this.$message({
                message:"正在更换展览顺序"
            })
            var data = {
                order: true,
                id: this.id,
                new_image_list: res,
            }
            var method = 'POST'
            var url = '/api/exhibit_edit'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                    {
                        console.log(object)
                        my_this.$message.error(object.detail);
                        return
                    }
                my_this.$message({
                    message:'展览中照片顺序修改成功',
                    type:'success'
                    })
                my_this.exhibit_update()
            }
            request_json(data,url,method,get_response)
        },
    },
    created: function(){
        this.exhibit_update()
    },
}
</script>

<style scoped>
    .edit-title{
        text-align:left; 
        font-weight:bold;
    }

    .border {
        width: 1px;
        height: 100%;
        margin-left: 20px;
        margin-right: 20px;
        background-color: #888888;
        float: left;
    }

    .example-container{
        overflow: auto;
        height:500px;
    }

    .introduction-container {
        height: 100%;
        float: left;
        text-align: left;
        padding-left: 10px;
        overflow: auto;
    }

    .info-container {
        width: 100px;
        height: 100%;
        float: right;
        padding: 10px;
    }

    .big-icon{
        font-size:300%;
    }

    .el-radio{
        height:auto;
    }
</style>