<template>
    <el-row>
        <el-row>
            <a>一次最多自本地提交20张，只能是jp(e)g/png/bmp格式</a>
        </el-row>
        <el-row>
        <el-col class="grey-background" :span="12" >
            <el-row style="height:50px">
                <el-tag type="info" effect="dark">本地上传</el-tag>
                <el-tooltip content="进入全屏" placement="top">
                <el-button v-if="baseList.length>0" type="text" style="font-size:150%;color:grey;float:right" @click="base_fullscreen=true">
                    <a-icon type="fullscreen" />
                </el-button>
                </el-tooltip>
            </el-row>
            <div class="slide-bar">
                <el-upload ref="elupload" action="" :multiple="true" :auto-upload="false" :file-list="fileList"
                    :on-change="handlechange" list-type="picture-card" accept=".jpg,.png,.bmp,.jpeg" :limit="20"
                    :on-exceed="masterFileMax">
                    <i class="el-icon-plus"></i>
                    <div slot="file" slot-scope="{file}" class="clss">
                        <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                        <span class="el-upload-list__item-actions">
                            <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                                <i class="el-icon-zoom-in"></i>
                            </span>
                            <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                                <i class="el-icon-delete"></i>
                            </span>
                        </span>
                    </div>
                </el-upload>
            </div>
        </el-col>
        <el-col class="grey-background" :span="12">
            <el-row style="height:50px">
                <el-tag type="info" effect="dark">线上重修</el-tag>
                <el-tooltip content="进入全屏" placement="top">
                <el-button v-if="withsendList.length>0" type="text" style="font-size:150%;color:grey;float:right" @click="select_fullscreen=true">
                    <a-icon type="fullscreen" />
                </el-button>
                </el-tooltip>
            </el-row>
            <div class="slidebar fix-bar">
                    <el-empty v-if="withsendList.length==0" description="没有需要重新修复的照片" :image-size="100">
                        
                    </el-empty>
                    <transition-group name="listgroup" tag="ul">
                    <div class="sketch-item" v-for="image,index in withsendList" :key="image.id" >
                        <div class="modal">
                            <div class="operation-modal">
                                <el-button type="text" @click="remove_withsend(index)"
                                style="font-size:200%; color:white; cursor:pointer">
                                    <i class="el-icon-delete"/>
                                </el-button>
                            </div>
                        </div>
                        <div class="item-box">
                            <ExhibitBlock  :id="image.id" :name="image.title" 
                            :image_src="image.img_src" :introduction="image.introduction"
                            :timestamp="image.timestamp" :tag_list="image.tag_list"
                            :likes="image.likes" :comments="image.comments"
                            state="sketch">
                            </ExhibitBlock>
                        </div>
                    </div>
                    </transition-group>
            </div>
        </el-col>
        </el-row>
        <el-col :span="24" style="margin-top:5px">
        <el-col :span="12">
            <el-row>
                当前修复步骤，共{{(steps[0]!=null)?steps.length:0}}步
            </el-row>
            <el-col :span="7">
                <el-dropdown @command="add_to_steps">
                    <el-button type="primary">
                        添加修复步骤<i class="el-icon-arrow-down el-icon--right"></i>
                    </el-button>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item v-for="op in operation_options" :key="op.value" :command="op" icon="el-icon-circle-plus-outline">{{op.label}}</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </el-col>
            <el-col :span="17" class="steps-container">
                
            <div class="slide-bar" style="height:70px">
                    <!-- <transition name="change" mode="out-in"> -->
                    <transition-group name="list" tag="p" mode="out-in">
                    <div class="step-box" v-for="step,index in steps" :key="(step==null)?index:step.value"
                         @click="withdraw_step(index)">
                         <div v-if="step==null" class="step-container">
                             无操作
                         </div>
                         <div v-else class="step-container">
                             {{step.label}}
                         </div>
                         <div class="step-container">
                            <a-icon type="right" style="font-size:200%"/>
                         </div>
                    </div>
                    </transition-group>
                    <!-- </transition> -->
                    
                </div>
            </el-col>
        </el-col>
        <el-col :span="12">
            <el-card>
                <!-- <h2>请将照片上传，并开始修复</h2> -->
                <el-button @click="fromsite">网站上传，重新修复</el-button>
                <el-button @click="uploadelupload" type="success">开始修复</el-button>
                <el-button @click="clear" type="danger">全部清除</el-button>

            
            </el-card>
        </el-col>
        </el-col>
        <el-dialog :visible.sync="onvisible" width="1200px">
            <SearchPage height="400px" :type="0" state="choose" range="photo" :resolve="resolve">
            </SearchPage>
        </el-dialog>
        <el-dialog :visible.sync="Visible">
            <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
        <el-dialog :visible.sync="select_fullscreen" width="70%" top="30px">
            <transition-group name="listgroup" tag="div" class="flex-container" style="height:500px">
                    <el-empty v-if="withsendList.length==0" description="没有需要重新修复的照片" :image-size="100">
                        
                    </el-empty>
                    <div class="sketch-item" v-for="image,index in withsendList" :key="image.id" 
                    style="margin-bottom:30px">
                        <div class="modal">
                            <div class="operation-modal">
                                <el-button type="text" @click="remove_withsend(index)"
                                style="font-size:200%; color:white; cursor:pointer">
                                    <i class="el-icon-delete"/>
                                </el-button>
                            </div>
                        </div>
                        <div class="item-box">
                            <ExhibitBlock  :id="image.id" :name="image.title" 
                            :image_src="image.img_src" :introduction="image.introduction"
                            :timestamp="image.timestamp" :tag_list="image.tag_list"
                            :likes="image.likes" :comments="image.comments"
                            state="sketch">
                            </ExhibitBlock>
                        </div>
                    </div>
                </transition-group>
        </el-dialog>
        <el-dialog :visible.sync="base_fullscreen" title="上传" width="70%" top="30px">
            <div class="flex-container" style="height:500px">
                <el-upload ref="upload" action="" :multiple="true" :auto-upload="false" :file-list="fileList"
                    :on-change="handlechange" list-type="picture-card" accept=".jpg,.png,.bmp,.jpeg" :limit="20"
                    :on-exceed="masterFileMax">
                    <i class="el-icon-plus"></i>
                    <div slot="file" slot-scope="{file}" class="clss">
                        <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                        <span class="el-upload-list__item-actions">
                            <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                                <i class="el-icon-zoom-in"></i>
                            </span>
                            <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                                <i class="el-icon-delete"></i>
                            </span>
                        </span>
                    </div>
                </el-upload>
            </div>
        </el-dialog>
    </el-row>
    
</template>

<script>
import ExhibitBlock from './ExhibitBlock.vue'
import {
        request_json
    } from '@/utils/communication.js'
import SearchPage from "@/components/SearchPage"
    export default {
        name: 'fix_photo',
        components: {
            SearchPage,
            ExhibitBlock,
        },
        props: {
            refresh:{
                type:Function,
                required:true,
            },
            refix_list:{
                type:Array,
                required:true,
            }
        },
        data() {
            return {
                select_fullscreen:false,
                base_fullscreen: false,
                Visible: false,
                returncode: 200,
                withsendList: [],
                fileList: [],
                hrefList: [],
                baseList: [],
                user: "",
                onvisible: false,
                pub_date: "",
                operation_options: [{
                    value: 'shangse',
                    label: '黑白上色'
                }, {
                    value: 'duibidu',
                    label: '对比度增强'
                }, {
                    value: 'tuxiangchuwu',
                    label: '图像除雾'
                }, {
                    value: 'qingxidu',
                    label: '清晰度增强'
                }],
                steps: [],
                dialogImageUrl: null,
            };
        },
        created() {
            this.steps.push(null)
            var date = new Date();
            var seperator1 = "-";
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            var strDate = date.getDate();
            if (month >= 1 && month <= 9) {
                month = "0" + month;
            }
            if (strDate >= 0 && strDate <= 9) {
                strDate = "0" + strDate;
            }
            this.pub_date = year + seperator1 + month + seperator1 + strDate;
        },
        methods: {
            resolve(res) {
                this.withsendList = this.withsendList.concat(res);
                this.onvisible = false;
            },
            clear() {
                this.fileList = [];
                this.baseList = [];
                this.withsendList = []
            },
            fromsite() {
                this.onvisible = true;
            },
            add_to_steps(step){
                if(this.steps[0]==null)
                    this.steps = []
                const my_this= this
                setTimeout(function(){
                    my_this.steps.push(step)
                },500)
                
            },
            withdraw_step(index){
                this.steps.splice(index,1)
                if(this.steps.length==0){
                    const my_this= this
                    setTimeout(function(){
                        my_this.steps.push(null)
                    },500)
                }
            },
            remove_withsend(index){
                this.withsendList.splice(index,1)
            },
            /**
             * 文件框改变事件
             * @param file
             * @param fileList
             */
            handlechange(file, fileList) {
                this.fileList = fileList;
                var reader = new FileReader();
                reader.readAsDataURL(file.raw);
                reader.onload = () => {
                    this.baseList.push(reader.result);
                }
            },
            handleRemove(file) {
                this.fileList.forEach((element, i) => {
                    if (file === element) {
                        this.fileList.splice(i, 1)
                        this.baseList.splice(i, 1)
                    }
                })
                console.log(this.baseList);
            },
            uploadelupload() {
                const my_this = this
                //let Base64 = require('js-base64').Base64;
                var put = [];
                //this.$refs.elupload.submit(); // 这里是执行文件上传的函数，其实也就是获取我们要上传的文件
                this.baseList.forEach(item => {
                    put.push(item);
                })
                if (this.withsendList.length > 20) {
                    alert("网站最多上传20张！")
                    return;
                }
                var doo = [];
                this.steps.forEach(function(item){
                    if(item!=null){
                        doo.push(item.value)
                    }
                })
                if (this.fileList.length + this.withsendList.length == 0) {
                    alert("请上传图片！不要给后端带来额外的负担！");
                    return;
                }
                this.$message("上传中")
                for(let i=0;i<put.length;i+=1)
                {
                    const my_list = put.slice(i,i+1)
                    setTimeout(function(index=i,sum=put.length){
                        my_this.fix_photo(doo,my_list)
                        if(index==sum-1){
                            my_this.$message({
                                type:"success",
                                message:"上传部分发送完毕"
                                })
                        }
                    },(i)*100)
                }
                const my_sum = this.withsendList.length
                this.withsendList.forEach(function(item,i){
                    const my_list = [item.id]
                    setTimeout(function(index=i,sum=my_sum){
                        my_this.refix_photo(doo,my_list)
                        if(index==(sum-1)){
                            my_this.$message({
                                type:"success",
                                message:"重修部分发送完毕"
                                })
                        }
                    },(i)*100)
                })
                this.fileList = [];
                this.baseList = [];
                this.withsendList = [];
                const timer = setInterval(function(){
                    if(my_this.refresh())
                    {
                        clearInterval(timer)
                    }
                },2000)
                setTimeout(function(){
                    clearInterval(timer)
                }, 12000)
                this.$router.push({
                    path: '/admin/photo'
                });
                
            },
            fix_photo(doo,put){
                var dat = {};
                dat['fixstep'] = doo;
                dat['fixlist'] = put;
                // dat['refix'] = this.withsendList;
                dat['user'] = this.user;
                dat['pub_date'] = this.pub_date;
                //  formdata.append("score", 4)
                var sending = {};
                sending['wanted'] = "please_fix";
                sending['data'] = dat;
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
                    my_this.$message({
                        message:"成功修复",
                        type:"success",
                    })
                }
                request_json(sending, '/api/fixupload', 'POST', get_response);
            },
            refix_photo(doo,put){
                var dat = {};
                dat['fixstep'] = doo;
                dat['refix'] = put;
                dat['user'] = this.user;
                dat['pub_date'] = this.pub_date;
                //  formdata.append("score", 4)
                var sending = {};
                sending['wanted'] = "please_fix";
                sending['data'] = dat;
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
                    my_this.$message({
                        message:"成功修复",
                        type:"success",
                    })
                }
                request_json(sending, '/api/fixupload', 'POST', get_response);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.Visible = true;
            },
            masterFileMax() {
                alert("本地图片上传上限为20张！");
            },

        },
        watch:{
            refix_list(){
                this.withsendList = this.withsendList.concat(this.refix_list);
                console.log("===================",this.withsendList)
            }
        },
    }
</script>

<style scoped>
    .fileParent {
        position: relative;
    }

    .clss img {
        position: absolute;
        object-fit: cover;
        left: 0;
        top: 0;
    }

    .file {
        position: absolute;
        left: 0;
        opacity: 0;
    }

    .steps-container{
        background: none;
        padding: 10px;
    }

    .fix-bar{
        height:160px;
        width:100%;
    }

    .grey-background{
        /* background: rgb(230,230,230); */
        padding: 10px;
        height: 220px;
    }

    .sketch-item {
        display: inline-block;  /* 横向滚动 */
        height: 146px;
        width: 146px;
        float: none;
        margin-right: 10px;
        padding: 0;
        
    }

    .modal{
        position: relative;
    }

    .operation-modal{
        position:absolute;
        z-index:10;
        height: 146px;
        width:100%;
        text-align: center;
        color: white;
        background: rgba(0, 0, 0, 0.2);
        padding: 30px;
        box-sizing: border-box;
    }

    .slide-bar,.slidebar {
        display:flex;
        text-align: left;
        /* 沿x轴滑动查看照片 */
        white-space: nowrap;
        overflow-y: hidden;
        overflow-x: auto;
    }

    .el-empty{
        padding:0
    }

    .item-box {
        display:flex;
        height: 100%;
        width: 100%;
    }

    .step-box{
        padding:10px;
        border-radius: 10px;
        background: white;
        display: inline-block;
        min-width: 100px;
        height:100%;
        margin-top:5px;
        margin-left: 10px;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
        text-align: center;
        display:inline-flex;
    }

    .flex-container{
        width: 100%;
        display: -webkit-flex;
        display: flex;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
        /* -webkit-align-content: space-around; */
        align-content: space-between;
        overflow-y: auto;
    }

    .step-box:hover{
        opacity: 0.8;
        cursor: pointer;
    }

    .step-container{
        align-self: center;
    }

    .change-enter-active, .change-leave-active {
    transition: all 1s;
    }
    .change-enter{
        opacity: 0;
        transform: translateX(-100px);
    }
    .change-leave-to {
        opacity: 0;
        transform: translateX(100px);
    }

    .list-enter-active, .list-leave-active {
    transition: all 0.5s;
    }
    .list-enter{
        opacity: 0;
        transform: translateX(-50px);
    }
    .list-leave-to {
        opacity: 0;
        transform: translateX(50px);
    }
    .list-move {
        transition: transform 1s;
    }

    .listgroup-enter-active, .listgroup-leave-active {
        transition: all 1s;
        /* position: absolute; */
    }
    .listgroup-enter{
        opacity: 0;
        transform: translateY(30px);
    }
    .listgroup-leave-to {
        opacity: 0;
        transform: translateY(30px);
    }
    .listgroup-move {
        transition: transform 1s;
    }
</style>