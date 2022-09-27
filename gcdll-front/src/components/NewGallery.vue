<template>
    <div class="new-gallery">
        <el-col :span="20">
            <div class = "stepss">
            <a-steps :current="current">
            <a-step class = "steps" v-for="item in steps" :key="item.title" :title="item.title" />
            </a-steps>
            </div>
        </el-col>
        <el-col :span="4">
            <div class="steps-action">
            <a-button v-if="current < steps.length - 1" type="primary" @click="next">
                Next
            </a-button>
            <a-button
                v-if="current == steps.length - 1"
                type="primary"
                @click="create_new_gallery"
            >
                Done
            </a-button>
            <a-button v-if="current > 0" style="margin-left: 8px" @click="prev">
                Previous
            </a-button>
            </div>
        </el-col>
        <div class="steps-content">
        {{ steps[current].content }}
        <div v-if="current === 0">
        <!-- <div class="intro"> -->
            <search-page :type="0" state="choose" range="photo"
            :height="'400px'" :resolve="resolve"></search-page>
        <!-- </div> -->
        </div>
        <div v-else-if="current === 1">
        <div :class="canEdit? 'dargBtn-lock el-icon-unlock': 'dargBtn-lock el-icon-lock' "
            @click="removeEvent()">{{canEdit? '调整':'锁定'}}</div>
        <draggable v-model="imgList" chosenClass="chosen" forceFallback="true" group="people"
            animation="1000" @start="onStart" @end="onEnd" :sort="canEdit">
            <div class="item" v-for="element in imgList" :key="element.id">
                <a>
                    <img style="object-fit:cover" :src="element.img_src" height="130" width="130">
                </a>
            </div>
        </draggable>
        </div>
        <div v-else-if="current === 2">
        <el-row>
            <el-col :span="16" :offset="4" style="padding:20px">
                <upload-cover :resolve="get_cover" :origin_cover="imgList[0].img_src"/>
            </el-col>
        </el-row>
        </div>
        <div v-else-if="current === 3">
             <el-col :span="16" :offset="4">
                <div class="givein">
                    <h2>输入展览主题简介</h2>
                    <el-input class="margin" v-model="name" placeholder="标题">
                    </el-input>
                    <el-input class="margin"  v-model="info" placeholder="简介" type="textarea" :row="3"></el-input>
                    <el-button class="margin"  type="success" @click="create_new_gallery">
                        完成！
                    </el-button>
                </div>
            </el-col>
        </div>
        </div>
    </div>
</template>

<script>
    import SearchPage from "@/components/SearchPage"
    import Draggable from 'vuedraggable'
    import UploadCover from './UploadCover.vue'
    import {
        request_json
    } from '@/utils/communication.js'
    export default {
        name: 'NewGallery',
        components: {
            SearchPage,
            Draggable,
            UploadCover
        },
        props:{
            refresh:{
                type:Function,
                required:true
            }
        },
        data() {
            return {
                onvisible: false,
                withsendList: [],
                covertype: 'none',
                fileList: [],
                ifcover: false,
                baseList: [],
                canEdit: true,
                drag: false,
                name: "",
                info: "",
                tofind: "",
                postlist: [],
                middlelist: [],
                imgList: [],
                current: 0,
                steps: [
                    {
                    title: '选择展览内照片',
                    content: '',
                    },
                    {
                    title: '调整照片顺序',
                    content: '',
                    },
                    {
                    title: '调整封面',
                    content: '',
                    },
                    {
                    title: '编辑信息',
                    content: '',
                    },
                ],
            };
        },
        methods: {
            get_cover(res){
                if(res.type=='upload')
                {
                    this.baseList = res.data
                }
                else
                {
                    this.withsendList = res.data
                }
                this.current += 1
            },
            next() {
                if(this.current === 0){
                for (var i = 0; i < this.imgList.length; i += 1) {
                    if (this.imgList[i].ifchosen == true) {
                        this.postlist.push(this.imgList.id);
                    }
                }
                if (this.postlist.length == 0) {
                    alert("图片不能没有！");
                    return;
                }
                }
                this.current++;
            },
            prev() {
                this.current--;
            },
            onStart(event) {
                console.log(event.oldIndex);
            },
            //拖拽结束事件
            onEnd(event) {
                console.log(event.newIndex);
                this.middlelist = this.imgList;
                this.postlist = [];
                this.middlelist.forEach(item => {
                    this.postlist.push(item.id);
                })
            },
            resolve(res) {
                this.middlelist = res;
                this.postlist = [];
                this.middlelist.forEach(item => {
                    this.postlist.push(item.id);
                })
                this.imgList = res;
                // 选好就进入下一页
                this.next()
            },
            onMove(relatedContext, draggedContext) {
                console.log(relatedContext.relatedContext.list);
                console.log(draggedContext);
            },
            removeEvent(item) {
                if (this.canEdit) {
                    this.canEdit = false;
                } else {
                    this.canEdit = true;
                }
                console.log(this.canEdit);
                console.log(item);
            },
            create_new_gallery() {
                var n = {};
                var ik = this.baseList.length + this.withsendList.length;
                if (ik > 1) {
                    alert("不能上传多张封面！");
                    return;
                }
                if (this.baseList.length == 1) {
                    this.covertype = 'base64';
                    this.ifcover = true;
                    n['cover'] = this.baseList;
                } else if (this.withsendList.length == 1) {
                    this.covertype = 'src';
                    this.ifcover = true;
                    n['cover'] = this.withsendList;
                } else {
                    this.ifcover = false;
                    this.covertype = 'none';
                    n['cover'] = [];
                }
                n['covertype'] = this.covertype;
                n['ifcover'] = this.ifcover;

                n['name'] = this.name;
                n['info'] = this.info;
                n['postlist'] = this.postlist;
                var p = {};
                p['info'] = n;
                p['wanted'] = "send_new_gallery";
                this.postlist = [];
                for (var ji = 0; ji < this.imgList.length; ji += 1) {
                    this.imgList[ji].ifchosen = false;
                    this.imgList[ji].ifchosenconnected = "";
                }
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
                    my_this.refresh()
                    my_this.$message({
                        message:"成功新建展览",
                        type:"success",
                    })
                }
                request_json(p, '/api/newgallery', 'POST', get_response);
                this.fileList = [];
                this.baseList = [];
                this.imgList = [];
                this.postlist = [];
                this.middlelist = [];
                this.withsendList = [];
                this.ifcover = false;
                this.name = ""
                this.info = ""
                this.current = 0
            },
            visitdialog() {
                this.onvisible = true;
            },
            masterFileMax() {
                alert("不要试图弄两个封面！");
            },
            choosed() {
                this.onvisible = false;
            },
        },
        created() {},
    }
</script>

<style scoped>
    .new-gallery{
        height: 400px
    }

    .specialcol {
        overflow-x: hidden;
    }

    .givein {
        margin:auto;
        margin-top:20px;
    }

    .clsh4 {
        margin: 3px;
    }

    .item {
        float: left;
        margin: 6px;
    }
    .margin {
        margin-bottom: 20px;
    }
    .stepss{
        width:100%;
    }
    .steps{
        width:200px;
    }
    .steps-content {
        margin-top: 12px;
        border-radius: 6px;
        min-height: 60px;
        text-align: center;
        padding-top: 40px;
    }
</style>