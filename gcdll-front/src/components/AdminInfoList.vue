<template>
    <div id="admin-info-list" :style="[has_border,curser_style]" @click="choose_this_block">
        <el-popover
            placement="bottom"
            width="800"
            trigger="click"
            v-model="visible"
            :disabled="state=='choose'">
        <!-- 编辑模式时 -->
        <el-row>
                <el-col :span="21">
                    <el-descriptions :column="3" :border="true">
                        <el-descriptions-item label="标题">
                            <el-badge class="item" :hidden="name_has_border" is-dot>
                                <el-input size="small" 
                                v-model="new_name" class="input-new-name">
                                </el-input>
                            </el-badge>
                        </el-descriptions-item>
                        
                        <el-descriptions-item label="标签">
                            <el-row style="height:45px;width:300px;white-space: nowrap;overflow-y: hidden;overflow-x: auto;">
                            <el-input size="small" class="input-new-tag"
                                v-if="inputVisible"
                                v-model="inputValue"
                                ref="saveTagInput"
                                @keyup.enter.native="handleInputConfirm"
                                @blur="handleInputConfirm"
                            >
                            </el-input>
                            <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
                            
                            <el-tag :key="tag.tag" :type="get_tag_color(tag)"
                                v-for="tag in dynamic_tag_list"
                                closable
                                :disable-transitions="false"
                                @close="handleClose(tag)">
                                {{  tag.tag }}
                            </el-tag>
                            </el-row>
                        </el-descriptions-item>
                    </el-descriptions>
                    <el-descriptions :column='1' :border="true">
                        <el-descriptions-item label="简介" style="width">
                        <el-badge class="item" :hidden="introduction_has_border" is-dot>
                        <el-input style="width:100%"
                        type="textarea" :style="introduction_has_border"
                        :rows="2"
                        v-model="new_introduction">
                        </el-input>
                        </el-badge>
                        </el-descriptions-item>
                    </el-descriptions>
                </el-col>
                <el-col :span="2" style="margin-left:10px;">
                    <el-row>
                        <el-button type="warning" v-if="type==1" @click="$router.push({name:'exhibit_edit',params:{'id':String(id)}})">
                            编辑
                        </el-button>
                    </el-row>
                    <el-row style="margin-top:5px;">
                        <el-button type="danger" @click="before_delete">
                            删除
                        </el-button>
                    </el-row>
                    <el-row style="margin-top:5px;">
                    <el-button type="success" v-if="ready_to_change" @click="before_confirm">
                        修改
                    </el-button>
                    <el-button type="info" v-else disabled>
                        修改
                    </el-button>
                    </el-row>
                    <el-row style="margin-top:5px;">
                    <el-button type="info" v-if="ready_to_change" @click="reset">
                        撤销
                    </el-button>
                    </el-row>
                </el-col>
        </el-row>
        <!-- 选择模式时： -->
        
        <div slot="reference" class="info-container" style="height: 100px">
            <el-col :span="2" style="height:100%">
                        <div class="preview" @mouseenter="show_preview" @mouseleave="close_preview">
                            <img :src="image_src" class="cover-img">    
                        </div>
                            <div class="preview-modal">
                                <div class="preview-wrapper" v-if="preview_visible">
                                <exhibit-block state="display" :id="id" :image_src="image_src" >
                                </exhibit-block>
                                </div>
                        </div>
            </el-col>
            <el-tooltip class="item" effect="dark" :content="(state=='choose')?'点击选择':'点击编辑'" placement="top">
            <el-col :span="22" style="height:100%">
                <el-descriptions :column="5" :border="true">
                <el-descriptions-item label="ID">
                    {{id}}
                </el-descriptions-item>
                <el-descriptions-item label="创建人">{{publisher_name}}</el-descriptions-item>
                <el-descriptions-item label="上传时间">{{datetime}}</el-descriptions-item>
                <el-descriptions-item label="评论数">{{     comments    }}</el-descriptions-item>
                <el-descriptions-item label="点赞数">{{     likes    }}</el-descriptions-item>
                </el-descriptions>
                <el-row style="height:50px;margin-top:5px; font-size:80%; text-align:left">
                    <el-col :span="4" label="标题">
                        <el-col :span="8">
                            标题：
                        </el-col>
                        <el-col :span="16">
                        {{name}}
                        </el-col>
                    </el-col>
                    <el-col :span="10" class="overflow-box" label="标签">
                        <el-col :span="3">
                            标签：
                        </el-col>
                        <el-col :span="20">
                                <el-row style="height:30px;white-space: nowrap;overflow-y: hidden;overflow-x: auto;">
                                <el-tag :key="tag.tag" :type="get_tag_color(tag)"
                                    v-for="tag in tag_list" size="small">
                                    {{  tag.tag }}
                                </el-tag>
                                </el-row>
                        </el-col>
                    </el-col>
                    <el-col :span="10" label="简介" style="height:100%;">
                        <el-col :span="4">
                            简介：
                        </el-col>
                        <el-col :span="20" style="height:90%;overflow-y:auto;">
                            {{introduction}}
                        </el-col>
                    </el-col>
                </el-row>
            </el-col>
            </el-tooltip>
        </div>
        </el-popover>
    </div>
</template>

<script>
import {request_json} from '@/utils/communication.js'
import ExhibitBlock from './ExhibitBlock.vue'
// 展览中一张照片的版面
export default {
    name: "AdminInfoList",
    components: {
        ExhibitBlock
        
    },
    props: {
        // 照片/展览 id
        id: {
            type:Number,
            require:true
        },
        tag_list:{
            type:Array,
            default(){
                return ['风景']},
        },
        comments: {
            type:Number,
            require:true
        },
        likes: {
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
            default: 0
        },
        image_src: {
            type: String,
            default: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdesk-fd.zol-img.com.cn%2Ft_s960x600c5%2Fg5%2FM00%2F02%2F05%2FChMkJ1bKyaOIB1YfAAusnvE99Z8AALIQQPgER4AC6y2052.jpg&refer=http%3A%2F%2Fdesk-fd.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1649854587&t=a5f1e9e174a7316000f9488d6365590d"
        },
        introduction: {
            type: String,
            default: "no"
        },
        add_to_list: {
            type: Function,
            default: 
                function(){
                    return
                }
        },
        callback_state: {
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
        state: {
            type: String,
            default: "choose",
        },

        // 父组件传来的指令
        new_name_props:{
            type:String,
            default:"",
        },
        new_introduction_props:{
            type:String,
            default:"",
        },
        dynamic_tag_list_props:{
            type:Array,
            default(){return []},
        },
        clear_all_tags_props:{
            type: Boolean,
            default:false,
        },
        delete_block_props:{
            type: Boolean,
            default:false,
        },
        change_valid:{
            type: Boolean,
            default:false,
        }
    },
    data(){
        return {
            publisher_name: '查询中',
            publisher_id: 0,
            visible: false,
            // 
            dynamic_tag_list: ['风景','人像'],
            inputVisible: false,
            inputValue: '',
            tag_changed: false,

            new_name: "",
            new_introduction: "",

            preview_visible:false,
        }
    },
    methods:{
        // =========操作tag========
        get_tag_color(tag) {
            if(this.tag_list.includes(tag))
            {
                return 'normal'
            }
            else{
                return 'success'
            }
        },
        check_tags_change(){
            this.tag_changed = false
            for(let i =0;i<this.tag_list.length;i+=1)
            {
                if(!this.dynamic_tag_list.includes(this.tag_list[i]))
                {
                    this.tag_changed = true
                }
            }
            for(let i =0;i<this.dynamic_tag_list.length;i+=1)
            {
                if(!this.tag_list.includes(this.dynamic_tag_list[i]))
                {
                    this.tag_changed = true
                }
            }
        },
        handleClose(tag) {
            this.dynamic_tag_list.splice(this.dynamic_tag_list.indexOf(tag), 1);
            this.check_tags_change()
        },
        showInput() {
            this.inputVisible = true;
            this.$nextTick(function(){
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },
        handleInputConfirm() {
            let inputValue = this.inputValue;
            if(inputValue=="")
            {
                this.inputVisible = false;
                return
            }
            if(this.dynamic_tag_list.includes(inputValue))
            {
                this.$message('禁止输入重复内容')
                this.$nextTick(function(){
                    this.$refs.saveTagInput.$refs.input.focus();
                });
                return
            }
            if (inputValue) {
                this.dynamic_tag_list.push({tag:inputValue});
            }
            this.inputVisible = false;
            this.inputValue = '';
            this.check_tags_change()
        },

        show_preview:function(){
            this.preview_visible = true
        },

        close_preview:function(){
            this.preview_visible = false
        },

        // =========选中==========
        // 选择该block
        choose_this_block: function(){
            if(this.is_chosen)
            {
                this.$props.add_to_list(this.id, 0)
            }
            else
            {
                this.$props.add_to_list(this.id, 1)
            }
        },


        go_to_route: function(){
            //用于展示照片时：
            if(this.type == 0)
                this.$router.push({ name: 'image', params: { id: this.id } })
            //用于展示展览时：
            else
                this.$router.push({ name: 'exhibit', params: { id: this.id } })
        
        },

        publisher_info_update: function(){
            var data = {id:this.id}
            var method = 'GET'
            var url = this.query_url
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object
                if(my_this.type==0)
                    object = response.data
                else
                    object = response.data.exhibit_info
                my_this.publisher_name = object.publisher_name
                my_this.publisher_id = object.publisher_id
            }
            request_json(data,url,method,get_response)
            
        },

        // 删除该条信息
        delete_block: function(forbid_message=false){
            if(forbid_message==false)
            {
                this.$message({
                    message: '正在删除',
                    type: 'info'
                })
            }
            var a = "delete";
            var send = {};
            var data = {};
            data['id'] = this.id;
            send['data'] = data;
            send['wanted'] = a;
            const my_this = this
            var get_response = function(res) {
                if(res.data.status!=undefined)
                {
                    if(forbid_message)
                        my_this.callback_state(my_this.id, a, 3)
                    else
                        my_this.$message.error(res.data.detail);
                    return
                }
                if(forbid_message)
                {
                    my_this.callback_state(my_this.id, a, 2)
                    return 
                }
                my_this.$message({
                    message: '删除成功',
                    type: 'success'
                })
                my_this.$emit('update')
                // my_this.$emit('delete',this.id)
            }
            // this.$emit('delete',this.id)
            request_json(send,this.url,'POST',get_response);
        },
        // 更改名字
        changename(forbid_message=false){
            var a = "change_name";
            var send = {};
            var data = {};
            data['new'] = this.new_name;
            data['id'] = this.id;
            send['data'] = data;
            send['wanted'] = a;
            const my_this = this
            var get_response = function(res) {
                if(res.data.status!=undefined)
                {
                    if(forbid_message)
                        my_this.callback_state(my_this.id, 'name', 3)
                    else
                        my_this.$message.error(res.data.detail);
                    return
                }
                if(forbid_message)
                {
                    my_this.callback_state(my_this.id, 'name', 2)
                    return 
                }
                my_this.$emit('update')
                my_this.$message({
                    message: '修改标题成功',
                    type: 'success'
                })
            }
            request_json(send,this.url,'POST',get_response);
        },
        // 更改简介
        changeintro(forbid_message=false){
            var a = "change_intro";
            var send = {};
            var data = {};
            data['new'] = this.new_introduction;
            data['id'] = this.id;
            send['data'] = data;
            send['wanted'] = a;
            const my_this = this
            var get_response = function(res) { 
                if(res.data.status!=undefined)
                {
                    if(forbid_message)
                        my_this.callback_state(my_this.id, 'introduction', 3)
                    else
                        my_this.$message.error(res.data.detail);
                    return
                }
                if(forbid_message)
                {
                    my_this.callback_state(my_this.id, 'introduction', 2)
                    return 
                }
                my_this.$message({
                    message: '修改简介成功',
                    type: 'success'
                })
                my_this.$emit('update')
            }
            request_json(send,this.url,'POST',get_response);
        },
        // 更改标签
        change_tag(forbid_message=false){
            var a = "change_tag";
            var send = {};
            var data = {};
            var tags = []
            for(let i=0;i<this.dynamic_tag_list.length;i+=1)
            {
                tags.push(this.dynamic_tag_list[i].tag)
            }
            data['new'] = tags;
            data['id'] = this.id;
            send['data'] = data;
            send['wanted'] = a;
            const my_this = this
            var get_response = function(res) { 
                if(res.data.status!=undefined)
                {
                    if(forbid_message)
                        my_this.callback_state(my_this.id, 'tag', 3)
                    else
                        my_this.$message.error(res.data.detail);
                    return
                }
                if(forbid_message)
                {
                    my_this.callback_state(my_this.id, 'tag', 2)
                    return 
                }
                my_this.$emit('update')
                my_this.$message({
                    message: '修改标签成功',
                    type: 'success'
                })
            }
            request_json(send,this.url,'POST',get_response);
        },
        confirm(){
            this.$message("正在修改中")
            if(this.name!=this.new_name)
            {
                this.changename()
            }
            if(this.introduction!=this.new_introduction)
            {
                this.changeintro()
            }
            if(this.tag_changed)
            {
                this.change_tag()
            }
        },
        // 修改前确认
        before_confirm(){
            const my_this=this
            this.$confirm('确认修改？')
            .then(function(){
                my_this.confirm()
            })
        },
        // 删除前确认
        before_delete(){
            const my_this=this
            this.$confirm('确认删除？')
            .then(function(){
                my_this.delete_block()
            })
        },
        // 恢复原样
        reset(){
            if(this.tag_list!=undefined)
                this.dynamic_tag_list = this.tag_list.slice(0,this.tag_list.length)
            this.new_name = this.name
            this.new_introduction = this.introduction
            this.tag_changed = false
        }
    },
    created:function(){
        this.reset()
        this.publisher_info_update()
    },
    computed:{
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
        url:function(){
            if(this.type==0)
            {
                return '/api/photoadmin'
            }
            else{
                return '/api/galleryadmin'
            }
        },
        query_url(){
            if(this.type==0)
            {
                return '/api/photo'
            }
            else{
                return '/api/exhibit'
            }
        },
        has_border:function(){
            if(this.state!='choose')
                return
            if(this.is_chosen==false)
            {
                return ""
            }
            return {
                'border': 'solid',
                'border-color': 'rgb(103, 194, 58)'
            }
        },
        ready_to_change:function(){
            if(this.new_name != this.name)
                return true
            if(this.new_introduction != this.introduction)
                return true
            // alert(1)
            if(this.tag_changed)
            {
                return true
            }
            return false
        },
        name_has_border:function(){
            if(this.name==this.new_name)
            {
                return true
            }
            return false
        },
        introduction_has_border:function(){
            if(this.introduction==this.new_introduction)
            {
                return true
            }
            return false
        },
        curser_style(){
            if(this.state=='choose')
                return{
                    'cursor': 'pointer'
                }
            return ""
        },
    },
    watch:{
        name:function(){
            this.reset()
        },
        introduction:function(){
            this.reset()
        },
        // 检测props
        change_valid(){
            if(this.change_valid==0)
                return
            
            if(this.new_name_props!="")
            {
                this.new_name = this.new_name_props
                if(this.name!=this.new_name)
                {
                    this.changename(true)
                }
            }
            if(this.new_introduction_props!="")
            {
                this.new_introduction = this.new_introduction_props
                if(this.introduction!=this.new_introduction)
                {
                    this.changeintro(true)
                }
            }
            if(this.dynamic_tag_list_props.length!=0 || this.clear_all_tags_props)
            {
                // 如果清空原有所有tag
                if(this.clear_all_tags_props)
                    this.dynamic_tag_list = this.dynamic_tag_list_props
                else
                    this.dynamic_tag_list = this.tag_list.concat(this.dynamic_tag_list_props)
                this.change_tag(true)
            }
            // 取消选中，来表示已经操作完成
            this.add_to_list(this.id,0)
        },
        delete_block_props(){
            if(this.delete_block_props==true)
            {
                this.delete_block(true)
            }
            // 取消选中，来表示已经操作完成
            this.add_to_list(this.id,0)
        },
        tag_list(){
            this.reset()
        },
    }
}
</script>

<style>
    #admin-info-list{
        width:95%;
        min-width: 800px;
        margin-bottom: 3px;
        background: white;
    }

    /* .el-popover{
        background: grey;
    } */
    
  .el-tag {
    margin-right: 10px;
  }
  .button-new-tag {
    margin-right: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-right: 10px;
    vertical-align: bottom;
  }
  .input-new-name {
      width: 180px;
      height: 30px;
      vertical-align: bottom;
      line-height: 30px;
      padding-top: 0;
      padding-bottom: 0;
  }
  .overflow-box{
      white-space: nowrap;
      overflow-y: hidden;
      overflow-x: auto;
  }
  .preview{
      height: 100%;
  }
  .preview :hover{
      color: #409EFF;
  }
  .preview-modal{
      position:relative;

  }
  .preview-wrapper{
        position: absolute;
        height: 250px;
        width: 250px;
        top: -125px;
        left: 250px;
        z-index: 10;
  }

    .cover-img{
        height: 100%;
        width: 100%;
        object-fit: cover;
    }
</style>