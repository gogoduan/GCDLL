<template>
    <div class="upload-cover">
                <el-card>
                    <div slot="header" class="clearfix edit-title">
                        {{title}}
                    </div>
                    <el-col :span="20">
                    <div class="cover-container"  @mouseenter="handle_mouse_enter" @mouseleave="handle_mouse_leave">
                        <div>
                            <img v-if="new_cover==null" v-bind:src="origin_cover" alt="封面">
                            <img v-else v-bind:src="new_cover" alt="新封面">
                        </div>
                        <div class="button-modal" v-if="show_modal">
                            <div class="text-modal-wrapper">
                            </div>
                            <div class="button-container center-align-box">
                                <el-col :span="12">
                                    <el-row style="margin-top:20px;">
                                        <el-button type="success" circle size="medium" @click="open_dialog">
                                            <i class="el-icon-plus" style="font-size:400%">
                                            </i>
                                        </el-button>
                                    </el-row>
                                    <el-row style="font-size:80%; margin-top:20px; color:white">
                                        从照片库中选取
                                    </el-row>
                                </el-col>
                                <el-col :span="12">
                                    <el-upload ref="upload"
                                        action="#" :on-change="handlechange"
                                        list-type="picture-card"
                                        :auto-upload="false"
                                        :show-file-list="false"
                                        :multiple="false"
                                        accept=".jpg,.png,.bmp,.jpeg"
                                        :limit ="1"
                                        >
                                        <i slot="default" class="el-icon-plus"></i>
                                    </el-upload>
                                </el-col>
                            </div>
                        </div>
                    </div>
                    </el-col>
                    <el-col :span="4" v-if="new_cover!=null">
                        <el-col :span="24" style="margin-top:30px">
                        <el-button type="warning" @click="withdraw_cover">
                            撤销
                        </el-button>
                        </el-col>
                        <el-col :span="24" style="margin-top:30px">
                        <el-button type="success" @click="change_cover">
                            确认
                        </el-button>
                        </el-col>
                    </el-col>
                    </el-card>
        <el-dialog :visible.sync="dialog_visible"
            title="上传照片中选择封面" width="80%">
            <search-page :resolve="get_selected_photos" :type="0" state="single_choose" range="photo" :is_filter="true" height="400px">
            </search-page>
        </el-dialog>
    </div>
</template>

<script>
import SearchPage from "./SearchPage.vue"
export default {
    name: 'UploadCover',
    components:{
        SearchPage,
    },
    props:{
        title:{
            type:String,
            default:'上传展览封面'
        },
        resolve:{
            type:Function,
            required:true,
        },
        origin_cover:{
            type:String,
            required:true,
        }
    },
    data(){
        return{
            new_cover: null,
            baseList: [],
            select_list: [],
            show_modal: false,
            type: 'upload', // 'select'
            dialog_visible: false,
        }
    },
    methods:{
        open_dialog(){
            this.dialog_visible = true
        },
        handle_mouse_enter:function(){
            this.show_modal = true
        },
        handle_mouse_leave:function(){
            this.show_modal = false
        },
        handlechange(file,fileList){
            this.new_cover = file.url;
            this.type = 'upload'
            console.log(fileList)
            var reader = new FileReader();
            reader.readAsDataURL(file.raw);
            reader.onload=()=>{
                this.baseList = []
                this.baseList.push(reader.result);
            }
        },
        withdraw_cover(){
            this.new_cover = null
            this.baseList = []
            this.select_list = []
        },
        change_cover(){
            this.new_cover = null
            this.resolve({
                type: this.type,
                data: (this.type=='upload')?this.baseList:[this.select_list[0].id],
            })
        },
        get_selected_photos(res){
            this.type = 'select'
            this.new_cover = res[0].img_src
            this.select_list = []
            this.select_list = res
            this.dialog_visible = false
            // this.$refs.upload.clearFiles()
            
        }
    }
}
</script>

<style scoped>
    .cover-container {
        height: 240px;
        margin: 10px;
        width: 400px;
        /* border-style: inset;
        border-color:rgb(210, 210, 210);
        border-width: 10px; */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
        float: left;
    }

    .cover-container img {
        padding-bottom: 0px;
        height: 240px;
        width: 400px;
        margin: auto;
        display: inline-block;
        object-fit: cover;
    }

    .button-modal{
        position: relative;
    }

    .button-modal .button-container{
        position: absolute;
        width:400px;
        height: 200px;
        top: -200px;
    }

    .text-modal-wrapper{
        position: absolute;
        width:400px;
        /* 对齐要求 */
        top: -240px;
        height: 240px;
        opacity:0.7;
        background: grey;
    }

    .button-container .el-button {
        /* 居中 */
        display: block;
        margin: auto;
        align-self: center;
    }

    .edit-title{
        text-align:left; 
        font-weight:bold;
    }
</style>
