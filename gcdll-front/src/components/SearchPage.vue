<template>
    <div id="search-page" :style="get_box_size">
        <el-container style="height: 100%;">
            <el-header class="search-header" height="auto">
                <el-row style="padding:10px">
                <el-col :span="(parent_width>PHONE_WIDTH)?16:24" :xs="{span:24}">
                    <div class="search-bar-wrap">
                        <search-bar 
                            :change_scope="change_scope"
                            :parent_width="parent_width"
                            :is_unique="is_unique" :start_loading="start_loading"
                            :current_page="current_page"
                            :amount="amount"
                            :exhibit_id="exhibit_id" :auto_focus="auto_focus"
                            :is_adv="is_adv" :is_filter="is_filter" 
                            :search_again="search_again" :search_resolve="search_resolve"
                            :scope="ex_scope" :ex_keyword="ex_keyword" 
                            :is_allow_advance_search="true" :type="range"
                            :resolve="get_search_result" :order_name="order_name" :order_method="order_method">
                        </search-bar>
                    </div>
                </el-col>
                <el-col :span="(parent_width>PHONE_WIDTH)?5:12" :xs="{span:12}">
                    <el-button v-if="now_state=='display'" @click="now_state='choose';select_list=[];init()">
                        开启批量选择
                    </el-button>
                    <el-button v-else-if="now_state=='choose'" @click="now_state='display'">
                        关闭批量选择
                    </el-button>
                    <span v-if="state=='single_choose'">
                        <el-tag type="info" effect="dark">
                            只能单选
                        </el-tag>
                    </span>
                </el-col>
                <el-col :span="(parent_width>PHONE_WIDTH)?3:12" :xs="{span:12}" v-if="force_unique==false">
                    <el-button v-if="is_unique" @click="is_unique=false;search_again=true;">
                        搜单张
                    </el-button>
                    <el-button v-else @click="is_unique=true;search_again=true;">
                        搜照片组
                    </el-button>
                </el-col>
                </el-row>
                <el-row style="width:100%;">
                <!-- 不绑定数据的表头 -->
                <el-col :span="(parent_width>PHONE_WIDTH)?10:18" :xs="{span:24}">
                    <el-table class="hide-table-header"
                        empty-text=" "
                        @sort-change="handle_sort_change"
                        style="width: 100%;background:none;"
                        :default-sort = "{prop: 'timestamp', order: 'descending'}"
                        >
                        <el-table-column
                        prop="timestamp"
                        label="上传时间"
                        sortable="custom"
                        style="width: 20%;background:none;">
                        </el-table-column>
                        <el-table-column
                        prop="comment"
                        label="评论数"
                        sortable="custom"
                        style="width: 20%;background:none;"
                        >
                        </el-table-column>
                        <el-table-column
                        prop="likes"
                        label="点赞数"
                        sortable="custom"
                        style="width: 20%;background:none;"
                        >
                        </el-table-column>
                        <!-- <el-table-column
                            align="right">
                            <template slot="header" :slot-scope="'scope'">
                                共{{   image_list.length   }}条记录，第{{current_page}}页
                            </template>
                        </el-table-column> -->
                    </el-table>
                </el-col>
                    <el-col :span="2" :xs="{span:12}" style="height:40px; display:flex;">
                        <span style="margin:auto;font-size:12px;color:grey">
                            共{{   total   }}条记录
                        </span>
                    </el-col>
                    <el-col :span="2" :xs="{span:12}" style="height:40px; display:flex;">
                        <span style="margin:auto;font-size:12px;color:grey">
                            第{{current_page}}页
                        </span>
                    </el-col>
                    <el-col :span="(parent_width>PHONE_WIDTH)?10:24" :xs="{span:24}">
                        <div v-if="now_state=='choose'||state=='choose'">
                            
                            <el-col :span="16">
                                <el-button :disabled="(chosen_cnt==chosen_list.length)" @click="choose_all">
                                    本页全选
                                </el-button>
                                <el-button :disabled="chosen_cnt==0" @click="un_choose_all">
                                    全不选
                                </el-button>
                            </el-col>

                            <el-col :span="8">
                                <el-badge :value="select_list.length" class="item">
                                    <el-popover v-if="state=='choose'"
                                        v-model="pop_visible"
                                        placement="left" width="480"
                                        height="400"
                                        :title="'已选中 ' + select_list.length +'项'"
                                        trigger="click">
                                        <el-table :data="select_list" style="max-height:300px;overflow:auto;">
                                            <el-table-column width="50" property="id" label="ID"></el-table-column>
                                            <el-table-column width="150" property="name" label="标题"></el-table-column>
                                            <el-table-column width="200" property="introduction" label="简介"></el-table-column>
                                            <el-table-column width="50" label="操作">
                                                <template slot-scope="scope">
                                                    <el-button @click="delete_choose(scope.row)" type="text" size="medium"
                                                    style="font-size:150%; color:red">
                                                        <a-icon type="minus-circle" theme="filled" />
                                                    </el-button>
                                                </template>
                                            </el-table-column>
                                        </el-table>
                                        <el-row style="text-align:center;margin-top:5px;">
                                            <el-button @click="pop_visible=false">
                                                取消
                                            </el-button>
                                            <el-button type="primary" @click="confirm_resolve">
                                                确认选中
                                            </el-button>
                                        </el-row>
                                        <el-button slot="reference" @click="confirm">
                                            <span >
                                                查看选中
                                            </span>
                                        </el-button>
                                    </el-popover>
                                    <el-popover v-else-if="state=='choosable'"
                                        v-model="pop_visible"
                                        placement="left" width="480"
                                        height="400"
                                        :title="'已选中 ' + select_list.length +'项'"
                                        trigger="click">
                                        <el-table :data="select_list" style="max-height:300px;overflow:auto;">
                                            <el-table-column width="50" property="id" label="ID"></el-table-column>
                                            <el-table-column width="150" property="name" label="标题"></el-table-column>
                                            <el-table-column width="200" property="introduction" label="简介"></el-table-column>
                                            <el-table-column width="50" label="操作">
                                                <template slot-scope="scope">
                                                    <el-button @click="delete_choose(scope.row)" type="text" size="medium"
                                                    style="font-size:150%; color:red">
                                                        <a-icon type="minus-circle" theme="filled" />
                                                    </el-button>
                                                </template>
                                            </el-table-column>
                                        </el-table>
                                        <el-row style="text-align:center;margin-top:5px;">
                                            <el-col :span="12">
                                                <el-input v-model="new_name" placeholder="输入新标题">
                                                </el-input>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-input v-model="new_introduction" placeholder="输入新简介">
                                                </el-input>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="8" style="padding-top: 10px;">
                                                <el-checkbox v-model="clear_all_tags">清除已有标签</el-checkbox>
                                            </el-col>
                                            <el-col :span="16"  class="tag-bar">
                                            <el-tag :key="tag.tag"
                                                v-for="tag in dynamic_tag_list"
                                                closable
                                                :disable-transitions="false"
                                                @close="handleClose(tag)">
                                                {{  tag.tag }}
                                            </el-tag>
                                            
                                            <el-input size="small" class="input-new-tag"
                                                v-if="inputVisible"
                                                v-model="inputValue"
                                                ref="saveTagInput"
                                                @keyup.enter.native="handleInputConfirm"
                                                @blur="handleInputConfirm"
                                            >
                                            </el-input>
                                            <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row style="text-align:center;margin-top:5px;">
                                            <el-button type="danger" @click="before_delete_all">
                                                删除所有
                                            </el-button>
                                            <el-button type="primary" @click="confirm_operation">
                                                确认修改
                                            </el-button>
                                        </el-row>
                                        <el-button slot="reference" @click="confirm">
                                            <span>
                                                批量操作
                                            </span>
                                        </el-button>
                                    </el-popover>
                                </el-badge>
                            </el-col>
                            
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-divider style="margin: 2px;"></el-divider>
            <el-main>
            <div class="search-main">
                <el-empty v-if="image_list.length==0&&loading==false" description="没有符合条件的内容"></el-empty>
                <div class="exhibit" style="width:100%;" v-if="display_type=='block'">
                    <exhibit-block :user_state="user_state" 
                    :add_to_list="add_to_list" :is_chosen="Boolean(chosen_list[index])"
                    :state="state" :size="get_exhibit_block_size"
                    v-for="image,index in image_list" 
                    :type="exhibit_block_type" :id="image.id" :image_src="image.img_src" 
                    :key="image.id" :introduction="image.introduction" 
                    :name="image.name"  :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                    </exhibit-block>
                </div>
                <div class="list" style="width:100%;" v-else>
                     <el-skeleton
                        style="width: 90%;margin-left:60px;"
                        :loading="loading"
                        animated
                        :count="5">
                        <template slot="template">
                            <el-row style="height:100px; background:white; padding:10px; margin-bottom:10px;">
                            <el-col :span="2">
                                <el-skeleton-item
                                    variant="image" style="height:80px;"
                                    />
                            </el-col>
                            <el-col :span="20" :offset="1">
                                <el-skeleton-item variant="p"/>
                                <el-skeleton-item variant="p"/>
                            </el-col>
                            </el-row>
                        </template>
                     </el-skeleton>
                    <transition-group name="listgroup" tag="ul">
                        <!-- 实现过渡必需key不同：令key为id -->
                        <admin-info-list class="list-item" 
                        v-on:update="update" v-on:delete="delete_block"
                        :change_valid="get_change_valid(index)" :delete_block_props="get_is_delete_block(index)"
                        :clear_all_tags_props="get_clear_all_tags(index)" :dynamic_tag_list_props="get_dynamic_tag_list(index)" 
                        :new_introduction_props="get_new_introduction(index)" :new_name_props="get_new_name(index)"
                        :add_to_list="add_to_list" :is_chosen="Boolean(chosen_list[index])"
                        v-for="image,index in image_list" 
                        :state="now_state" :callback_state="callback_state"
                        :type="type" :id="image.id" :image_src="image.img_src" 
                        :key="image.id" :introduction="image.introduction" 
                        :name="image.name" :comments="image.comments"
                        :likes="image.likes" :tag_list="image.tag_list"
                        :timestamp="image.timestamp">
                        </admin-info-list>
                    </transition-group>
                </div>
                
                
            </div>
            </el-main>
            <el-footer>
            <el-pagination class="page-footer"
            background @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="current_page"
            layout="total, sizes, prev, pager, next"
            :page-size.sync="amount"
            :total="Number(total)">
            </el-pagination>
            </el-footer>
        </el-container>
    </div>
</template>


<script>
import ExhibitBlock from './ExhibitBlock.vue'
import AdminInfoList from './AdminInfoList.vue'
import SearchBar from './SearchBar.vue'
import VALUE from '../utils/const'
// 搜索的照片/展览库
export default {
    name: "SearchPage",
    components: {
        ExhibitBlock,
        SearchBar,
        AdminInfoList
    },
    props: {
        width:{
            type: Number,
            default: 95,
        },
        height:{
            type: String,
            default: '',
        },
        // 展示的样式：block--照片块；list--信息列表
        display_type:{
            type: String,
            default: 'block',
        },
        // 回调函数，将参数赋给。。。
        resolve:{
            type: Function,
            default: function(){}
        },
        // 账户
        user_state:{
            type: Object,
            default: function(){
                return{
                user_valid:false,
                }
            }
        },
        // 0-照片 1-展览
        type: {
            type:Number,
            default: 0,
        },
        state: {
            type: String,
            default: "display",
        },
        //定义仅能搜索照片还是展览
        range: {
            type: String,
            default: null,
        },
        // 传入的默认搜索关键词
        keyword_from_props: {
            type: String,
            default: null,
        },
        // 传入的默认搜索领域
        scope_from_props: {
            type: String,
            default: null,
        },
        // // 传入默认搜索是否使用高级搜索
        is_adv:{
            type:Boolean,
            default: false,
        },
        // 是筛选功能-自动搜所有/搜索功能-不自动搜索
        is_filter:{
            type:Boolean,
            default: true,
        },
        // 搜索展览内照片
        exhibit_id:{
            type:Number,
            default:null,
        },
        auto_focus:{
            type:Boolean,
            default:false,
        },
        // 只能搜索单独的照片
        force_unique:{
            type:Boolean,
            default:true,
        },
    },
    data(){
        return {
            parent_width: 0,
            // is_adv: false,
            loading: true,
            // 是否只搜单张的形式
            is_unique: true,
            pop_visible: false,
            // 当前选择模式是否开启
            now_state:'',
            ex_keyword:null,
            ex_scope: 'photo',
            order_name: 'time',
            order_method: false,
            order_options: [
                {
                    index:1,
                    value: "按时间从最早到最近",
                    type: "early",
                }, 
                {
                    index: 2,
                    value: "按时间从最近到最早",
                    type: "late",
                }, 
                {
                    index:3,
                    value: "按热度",
                    type: "popularity",
                }
            ],
            select_list: [],
            chosen_cnt: 0,
            chosen_list: [],
            finish_list: {
                name:[],
                introduction:[],
                tag:[],
                delete:[],
            },
            image_list: [],

            // 操作相关
            new_name: "",
            new_introduction: "",
            dynamic_tag_list: [],
            clear_all_tags: false,
            change_valid: false,
            is_delete_block: false,

            //tag
            inputVisible: false,
            inputValue: '',

            // 再次搜索
            search_again: false,
            amount: 20,
            current_page: 1,
            total:0,

            PHONE_WIDTH: VALUE.PHONE_WIDTH,

            exhibit_block_type: 0,
        }
    },
    methods:{
        get_exhibit_block_type(){
            if(this.range!=null){
                if(this.range=='photo')
                {
                    return 0
                }
                else{
                    return 1
                }
            }
            else{
                if(this.ex_scope=='photo')
                {
                    return 0
                }
                else{
                    return 1
                }
            }
        },
        change_scope(new_scope){
            this.ex_scope = new_scope
        },
        get_box_width(){
            var object = document.getElementById("search-page")
            if(object!=null)
                this.parent_width = object.parentElement.clientWidth
        },
        handle_sort_change({column, prop, order}){
            column;
            this.current_page = 1
            if(order=='ascending')
                this.order_method = true
            else
                this.order_method = false
            if(prop=='timestamp')
            {
                this.order_name = 'time'
            }
            else if(prop=='likes')
            {
                this.order_name = 'like'  
            }
            else if(prop=='comment')
            {
                this.order_name = 'comment'  
            }
            this.search_again = true
        },
        // 初始化
        init(){
            this.chosen_list = new Array(this.image_list.length).fill(0)
            this.chosen_cnt = 0
            for(var i=0;i<this.chosen_list.length;i+=1)
            {
                const my_id = this.image_list[i].id
                var index = this.select_list.findIndex(function(image){
                    return image.id==my_id
                });
                if(index!=-1)
                {
                    this.chosen_list[i] = 1
                    this.chosen_cnt += 1
                }
            }
            
        },
        update(){
            this.$emit('update')
            this.search_again = true
        },
        // 前端手动将一个list删除，暂时弃用；目前全部采用向后端更新的方式
        delete_block(data){
            var index = -1
            for(let i= 0;i<this.image_list.length;i+=1)
            {
                if(this.image_list[i].id == data)
                {
                    index = i
                    break
                }
            }
            if(index!=-1)
                this.image_list.splice(index,1)
            this.$emit('update')
        },
        start_loading(){
            if(this.image_list.length==0)
                this.loading = true
        },
        get_search_result:function(data){
            var list = data.mes
            this.total = data.total
            this.image_list = list.slice(0,list.length)
            this.loading = false
            this.exhibit_block_type = this.get_exhibit_block_type()
            // this.select_list = []
            // this.chosen_cnt = 0
        },
        add_to_list:function(id, add){
            for(var i = 0;i < this.image_list.length;i+=1)
            {
                if(this.image_list[i].id == id)
                {
                    if(add)
                    {
                        this.select_list.push(this.image_list[i])
                        this.chosen_cnt += 1
                    }
                    else
                    {
                        const my_id = id
                        var index = this.select_list.findIndex(function(image){
                            return image.id==my_id
                        });
                        this.select_list.splice(index,1)
                        this.chosen_cnt -= 1
                    }
                    // 单选直接选中
                    if(this.state=='single_choose')
                    {
                        this.confirm_resolve()
                    }
                    else
                        this.chosen_list.splice(i,1,add)
                }
            }
        },
        // 反馈操作结果
        callback_state:function(id, type, state=2){
            for(var i = 0;i < this.image_list.length;i+=1)
            {
                if(this.image_list[i].id == id)
                {
                    this.finish_list[type].splice(i,1,state)
                }
            }
        },
        // 在选中栏内删除
        delete_choose(row){
            var my_id = row.id
            var index = this.select_list.findIndex(function(image){
                return image.id==my_id
            });
            if(index!=-1)
            {
                this.select_list.splice(index,1)
            }
            const my_this = this
            var page_index = this.chosen_list.findIndex(function(image,i){
                return my_this.image_list[i].id==my_id
            });
            if(page_index!=-1)
            {
                this.chosen_list[page_index] = 0
                this.chosen_cnt -= 1
            }
        },

        confirm:function(){
            // this.select_list = []
            // for(var i = 0;i < this.image_list.length;i+=1)
            // {
            //     if(this.chosen_list[i] == 1)
            //         this.select_list.push(this.image_list[i])
            // }
            console.log(this.select_list)
            // alert(JSON.stringify(this.select_list))
        },
        confirm_resolve(){
            this.pop_visible=false
            this.resolve(this.select_list)
            this.select_list = []
            this.init()
        },
        choose_all:function(){
            for(var i=0;i<this.image_list.length;i+=1)
            {
                if(this.chosen_list[i]==0)
                {
                    this.select_list.push(this.image_list[i])
                    this.chosen_list[i]=1
                    this.chosen_cnt+=1
                }
            }
        },
        un_choose_all:function(){
            for(var i=0;i<this.chosen_list.length;i+=1)
            {
                const my_id = this.image_list[i].id
                var index = this.select_list.findIndex(function(image){
                    return image.id==my_id
                });
                if(index!=-1)
                {
                    this.chosen_list[i] = 0
                    this.select_list.splice(index,1)
                    this.chosen_cnt -= 1
                }
            }
            this.init()
        },

        // =========操作tag========
        handleClose(tag) {
            this.dynamic_tag_list.splice(this.dynamic_tag_list.indexOf(tag), 1);
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
        },

        //==================操作==================
        confirm_operation(){
            if(this.chosen_list.includes(1)){
                this.change_valid=true;
                this.$message('批量操作进行中')
                // 将chosenlist复制一份给finishlist
                if(this.new_name!="")
                {
                    this.finish_list.name = this.chosen_list.slice(0,this.chosen_list.length) 
                }
                if(this.new_introduction!="")
                {
                    this.finish_list.introduction = this.chosen_list.slice(0,this.chosen_list.length)
                }
                if(this.dynamic_tag_list.length > 0 || this.clear_all_tags)
                {
                    this.finish_list.tag = this.chosen_list.slice(0,this.chosen_list.length)
                }
            }
            this.pop_visible=false;
        },
        before_delete_all(){
            const my_this=this
            this.$confirm('确认删除所有选中？')
            .then(function(){
                if(my_this.chosen_list.includes(1))
                {
                    my_this.$message('批量删除进行中')
                    my_this.is_delete_block=true
                    // my_this.change_valid=true;
                    my_this.finish_list.delete = my_this.chosen_list.slice(0,my_this.chosen_list.length)
                }
                my_this.pop_visible=false;
            })
        },
        get_new_name(index){
            if(this.chosen_list[index])
            {
                return this.new_name
            }
            else
            {
                return ""
            }
        },
        get_new_introduction(index){
            if(this.chosen_list[index])
            {
                return this.new_introduction
            }
            else
            {
                return ""
            }
        },
        get_dynamic_tag_list(index){
            if(this.chosen_list[index])
            {
                return this.dynamic_tag_list
            }
            else
            {
                return []
            }
        },
        get_clear_all_tags(index){
            if(this.chosen_list[index])
            {
                return this.clear_all_tags
            }
            else
            {
                return false
            }
        },
        get_change_valid(index){
            if(this.chosen_list[index])
            {
                return this.change_valid
            }
            else
            {
                return false
            }
        },
        get_is_delete_block(index){
            if(this.chosen_list[index])
            {
                return this.is_delete_block
            }
            else
            {
                return false
            }
        },
        // ==================搜索框重新搜索=================
        search_resolve(){
            this.search_again=false
        },

        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
            this.search_again = true
            // 自动跳到搜索页头
            const TOP = document.getElementById("search-page")
            const y = TOP.offsetTop
            document.body.scrollTop = document.documentElement.scrollTop = y;
        },

        handleSizeChange(){
            this.search_again = true
        }
    },
    watch:{
        range(){
            if(this.range!=null){
                this.ex_scope = this.range
            }
        },
        image_list:function(){
            this.init()
        },
        // chosen list清空时，说明操作已经部署完毕
        chosen_list(){
            if(!this.chosen_list.includes(1))
            {
                if(this.change_valid==true)
                {
                    if(this.now_state=='choose')
                    {
                        this.change_valid = false
                    }
                }
                if(this.is_delete_block==true)
                {
                    if(this.now_state=='choose')
                    {
                        this.is_delete_block = false
                    }
                }
            }
        },
        // 使用深度监听，检查finishlist中每一项的情况
        finish_list:{
            handler(){
                const operations=['name','introduction','tag','delete']
                const operation_name={
                    'name':'修改标题',
                    'introduction':"修改简介",
                    'tag':"修改标签",
                    'delete':"删除"}
                for(let j=0;j<4;j+=1)
                {
                    let operation = operations[j]
                    if(this.finish_list[operation].length==0)
                        continue
                    if(!this.finish_list[operation].includes(1))
                    {
                        var message = ""
                        for(let i=0;i<this.finish_list[operation].length;i+=1)
                        {
                            if(this.finish_list[operation][i] == 0)
                                continue
                            var val
                            if(this.finish_list[operation][i] == 2)//操作成功
                                val = '成功'
                            else if(this.finish_list[operation][i] == 3)//操作失败
                                val = '失败'
                            message += `<p>ID=${this.image_list[i].id}：${operation_name[operation]}操作${val}</p>`
                        }
                        this.$notify({
                            title: '批量操作结果',
                            dangerouslyUseHTMLString: true,
                            message: message,
                        });
                        this.finish_list[operation] = []
                        this.update()
                    }
                }
                
            },
            deep:true,
        },
    },
    computed:{
        total_page(){
            return parseInt((this.total-1)/20 + 1)
        },
        page_width(){
            var docEl = document.documentElement;
            return docEl.getBoundingClientRect().width;
        },
        get_box_size(){
            return{
                'height':this.height,
                'width':this.width + "%",
            }
        },
        get_exhibit_block_size(){
            if(Number(this.width)*this.parent_width/100 < VALUE.PHONE_WIDTH)
            {
                return 150
            }
            else{
                return 200
            }
        }
    },
    created:function(){
        if(this.force_unique)
            this.is_unique = this.force_unique
        if(this.state=='choosable')
            this.now_state = 'display'
        // 初始时监测props
        if (this.keyword_from_props != null)
        {
            // 检验scope是否准确
            if(this.scope_from_props == 'photo' || this.scope_from_props == 'exhibit')
            {
                this.ex_keyword = this.keyword_from_props
                this.ex_scope = this.scope_from_props
            }
        }
        if(this.range!=null){
            this.ex_scope = this.range
        }
        // else{
        //     this.ex_keyword = this.$route.params.ex_keyword
        //     this.ex_scope = this.$route.params.ex_scope
        //     // 检验scope是否准确
        //     if(this.ex_scope != 'photo' && this.ex_scope != 'exhibit')
        //     {
        //         this.ex_keyword = null
        //         this.ex_scope = null
        //     }
        // }
        this.init()
        // this.activated()
    },
    mounted(){
        const my_this = this
        setInterval(
            function(){
                my_this.get_box_width()
            },2000
        )
        this.get_box_width()
    },
    // 用于解决searchResultPage懒加载
    activated(){
        var a = this.$route.params.is_adv
        if(a!=undefined && a==1)
        {
            this.is_adv = Boolean(a)
        }
        else
        {
            this.is_adv = false
        }
        if(this.$route.params.ex_keyword!=undefined){
            this.ex_keyword = this.$route.params.ex_keyword
        }
        else{
            this.ex_keyword = null
        }
        if(this.$route.params.ex_scope!=undefined)
        this.ex_scope = this.$route.params.ex_scope
    }
}
</script>

<style scoped>
    #search-page {
        width:100%;
        height:100%;
        /* min-width: 600px; */
        min-height: 400px;
        overflow: auto;
        overflow-x: hidden;
    }
    .search-bar-wrap{
        width: 90%;
        /* min-width: 600px; */
        display: inline-block;
    }
    .search-main{
        display: -webkit-flex;
        display: flex;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
        -webkit-align-content: space-between;
        align-content: space-between;
    }
    #search-page /deep/ .el-table{
        background: none;
    }
    #search-page /deep/ .el-table tr{
        background: none;
    }
    #search-page /deep/ .el-table th.el-table__cell{
        background: none;
    }
    .hide-table-header /deep/ .el-table__cell{
        padding:0;
    }
    .hide-table-header /deep/ .el-table__body-wrapper{
        height:0;
    }

    @media screen and (max-width: 768px) {
        .hide-table-header /deep/ .cell {
            font-size:9px;
        }
    }
    .exhibit {
        width: 100%;
        display: -webkit-flex;
        display: flex;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
        -webkit-align-content: space-around;
        align-content: space-between;
    }
    .el-empty{
        margin:auto;

    }
    .el-divider {
        margin: 2px;
    }
    /* list的渐出效果 */
    .list-item {
        /* transition: all 1s; */
        display: inline-block;
        margin-right: 10px;
    }
    .listgroup-enter-active, .listgroup-leave-active {
        transition: all 1s;
        /* position: absolute; */
    }
    .listgroup-enter, .listgroup-leave-to {
        opacity: 0;
        transform: translateX(50px);
    }
    .listgroup-move {
        transition: transform 1s;
    }

    .tag-bar{
        margin-top:5px; 
        white-space: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        height:50px;
    }

    .tag-bar.el-tag {
        margin-left: 10px;
    }
    .tag-bar.button-new-tag {
        margin-left: 10px;
        height: 32px;
        line-height: 30px;
        padding-top: 0;
        padding-bottom: 0;
    }
    .tag-bar.input-new-tag {
        width: 90px;
        margin-left: 10px;
        vertical-align: bottom;
    }

    .page-footer{
        margin-bottom: 20px;
    }
</style>
