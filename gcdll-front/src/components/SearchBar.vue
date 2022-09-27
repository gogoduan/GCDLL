<template>
    <div class="search-bar">
            <el-menu id="search">
                <el-row id="search-wrapper">
                    <el-col :span="4" :xs="{span:12}">
                    <el-select placeholder="选择范围" v-model="display_scope" :disabled="type!=null" @change="handle_change_scope">
                        <el-option v-for="option in scope_options" :key="option.index" :label="option.value" :value="option.type">                    
                        </el-option>
                    </el-select>
                    </el-col>
                    <el-col class="fill-container" :span="8" :xs="{span:12}">
                    <el-dropdown style="width:100%" v-if="is_allow_advance_search" @command="handleCommand">
                        <el-button type="info">
                            添加高级搜索<i class="el-icon-arrow-down el-icon--right"></i>
                        </el-button>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item
                            v-for="index in adv_options_scopes[scope]"
                            :key="index"
                            :command="adv_options[index].index"
                            @select="add_adv(adv_options[index].index)">
                            {{   adv_options[index].value   }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <el-button v-else @click="go_to_search_page">
                        高级搜索
                    </el-button>
                    </el-col>
                    <el-col :span="12" :xs="{span:24}">
                    <el-input ref="search_input" v-if="filters.length==0" placeholder="搜索..." v-model="keyword"  @keyup.enter.native="send_filter();">                
                        <el-button slot="append" icon="el-icon-search" v-on:click="send_filter();$message('搜索中');">

                        </el-button>
                    </el-input>
                    <el-button type="info" v-else style="margin-left: 20%;" @click="send_adv_filters();$message('搜索中');">
                        高级搜索
                    </el-button>
                    </el-col>
                </el-row>
                <div id="all-adv-search-wrapper" v-for="(adv_index,index) in adv_list" :key="index">
                    <!-- 搜索文本 -->
                    <el-card class="box-card" id="adv-search-wrapper" v-if="adv_index==0" body-style="padding:5px;">
                        <el-row>
                            <el-col :span="4" :xs="{span:6}">
                                <el-row>
                                {{   adv_options[adv_index].value   }}
                                </el-row>
                                <el-row>
                                    <el-checkbox v-model="filters[index].negative">
                                        排除
                                    </el-checkbox>
                                </el-row>
                            </el-col> 
                            <el-col :span="18" :xs="{span:16}">
                                <el-col :span="(parent_width>768)?16:24"  :xs="{span:24}">
                                <el-col :span="6" :xs="{span:24}">
                                    <el-checkbox :indeterminate="filters[index].isIndeterminate" 
                                        v-model="filters[index].search_range_checkAll" 
                                        @change="search_range_handleCheckAllChange($event,index)">
                                        全选
                                    </el-checkbox>
                                </el-col>
                                <el-col :span="18" :xs="{span:24}">
                                    <el-checkbox-group v-model="filters[index].search_range_list" @change="search_range_handleCheckChange($event,index)">
                                        <el-checkbox v-for="item,index in search_range_options" :label="item" :key="index"></el-checkbox>
                                    </el-checkbox-group>
                                </el-col>
                                </el-col>
                                <el-col :span="(parent_width>768)?8:24"  :xs="{span:24}">
                                    <el-tooltip v-if="filters[index].search_range_list.length == 0" content="请选择搜索范围" placement="top">
                                        <el-input placeholder="搜索..." v-model="filters[index].keyword" disabled>
                                        </el-input>
                                    </el-tooltip>
                                    <el-input v-else placeholder="搜索..." v-model="filters[index].keyword">
                                    </el-input>
                                </el-col>
                            </el-col>
                            <el-col :span="2">
                                <!-- :disabled="is_disable_first_adv(index)" -->
                                <el-button style="float: right; padding: 3px 0" type="text" @click="remove_adv(index)">
                                    <i class = "el-icon-close">
                                    </i>
                                </el-button>
                            </el-col>
                        </el-row>
                    </el-card>
                    <!-- 上传时间 -->
                    <el-card class="box-card" id="adv-search-wrapper" v-if="adv_index==1" body-style="padding:5px;">
                        <el-row>
                            <el-col :span="4"  :xs="{span:6}">
                                <el-row>
                                {{   adv_options[adv_index].value   }}
                                </el-row>
                                <el-row>
                                    <el-checkbox v-model="filters[index].negative">
                                        排除
                                    </el-checkbox>
                                </el-row>
                            </el-col> 
                            <el-col :span="18" style="display:flex;"  :xs="{span:16}">
                                <el-date-picker style="width: 100%;"
                                    v-model="filters[index].time_range"
                                    type="daterange"
                                    range-separator="--"
                                    start-placeholder="开始日期"
                                    end-placeholder="结束日期">
                                </el-date-picker>
                            </el-col>
                            <el-col :span="2">
                                <el-button style="float: right; padding: 3px 0" type="text" @click="remove_adv(index)">
                                    <i class = "el-icon-close">
                                    </i>
                                </el-button>
                            </el-col>
                        </el-row>
                        
                        
                    </el-card>
                    <!-- id -->
                    <el-card class="box-card" id="adv-search-wrapper" v-if="adv_index==2" body-style="padding:5px;">
                        <el-row>
                            <el-col :span="4"  :xs="{span:6}">
                                <el-row>
                                {{   adv_options[adv_index].value   }}
                                </el-row>
                                <el-row>
                                    <el-checkbox v-model="filters[index].negative">
                                        排除
                                    </el-checkbox>
                                </el-row>
                            </el-col> 
                            <el-col :span="18" style="display:flex;"  :xs="{span:16}">
                                <el-input-number v-model="filters[index].min_id" 
                                controls-position="right" :min="1" :max="10000000">
                                </el-input-number>
                                <a-icon style="margin:auto" type="swap" />
                                <el-input-number v-model="filters[index].max_id" 
                                controls-position="right" :min="1" :max="100000000">
                                </el-input-number>
                            </el-col>
                            <el-col :span="2">
                                <el-button style="float: right; padding: 3px 0" type="text" @click="remove_adv(index)">
                                    <i class = "el-icon-close">
                                    </i>
                                </el-button>
                            </el-col>
                        </el-row>
                        
                        
                    </el-card>
                </div>
                    
            </el-menu>
    </div>
    
</template>

<script>

import {request_json} from '@/utils/communication.js'
// const MAX_timestamp = 1000000000000
export default {
    name: "SearchBar",
    components: {
        // Login
    },
    props: {
        parent_width:{
            type:Number,
            default:1200,
        },
        // 分页
        current_page:{
            type:Number,
            default:null,
        },
        amount:{
            type:Number,
            default:null,
        },
        //定义仅能搜索照片还是展览
        type: {
            type: String,
            default: null,
        },
        exhibit_id:{
            type:Number,
            default:null,
        },
        // 限定搜索顺序
        order_name:{
            type: String,
            default: "time",
        },
        // 限定搜索顺序
        order_method:{
            type: Boolean,
            default: true,
        },
        is_allow_advance_search:{
            type: Boolean,
            default: false,
        },
        ex_keyword:{
            type: String,
            default: null,
        },
        scope:{
            type: String,
            default: 'photo'
        },
        // 回调函数，将参数赋给。。。
        resolve:{
            type: Function,
            require: true,
        },
        start_loading:{
            type: Function,
            require: true,
        },
        // 传入默认搜索是否使用高级搜索
        is_adv:{
            type:Boolean,
            default: false,
        },
        // 是筛选功能-自动搜所有/搜索功能-不自动搜索
        is_filter:{
            type:Boolean,
            default: false,
        },
        // 是否再次搜索一遍
        search_again:{
            type:Boolean,
            default: false,
        },
        // 向父组件传递已经再次搜索完毕
        search_resolve:{
            type:Function,
            default:function(){}
        },
        auto_focus:{
            type:Boolean,
            default:false,
        },
        is_unique:{
            type:Boolean,
            default:false,
        },
        change_scope:{
            type:Function,
            required: true,
        }
    },
    data() {
        return {
            display_scope: 'photo',
            result_list: [],
            // 搜索关键词
            keyword: "",
            adv: "",
            // 搜索对象
            scope_options: [
                {
                    index:1,
                    value: "照片",
                    type: "photo",
                }, 
                {
                    index:3,
                    value: "展览",
                    type: "exhibit",
                }
            ],
            // 高级搜索选项
            adv_options: [
                {
                    index:0,
                    value: "搜索范围",
                },
                {
                    index:1,
                    value: "上传时间",
                },
                {
                    index:2,
                    value: "ID",
                },
            ],
            // 不同搜索对象有不同高级搜索选项的index
            adv_options_scopes:{
                "photo":[0,1,2],
                "exhibit":[0,1,2],
            },
            search_range_options: ['标签', '标题', '简介'],
            //
            adv_list: [],
            // 最终发给后端的过滤器
            filters:[
                
            ],
            filter: {
                    // 搜索标签，键值对
                    tag:[], // 列表可能为空！则不筛
                    title:[],
                    introduction:[],
            },
        }
    },
    methods:{
        handle_change_scope(new_scope){
            this.adv_list = []
            this.filters = []
            this.change_scope(new_scope)
        },
        // 选择添加高级搜索选项
        handleCommand(command) {
            var filter;
            if(command==0)//搜索文本
            {
                filter = {
                    type:0,
                    tag:[], // 列表可能为空！则不筛
                    title:[],
                    introduction:[],
                    
                    keyword: '',
                    // 搜索文本范围
                    search_range_checkAll:false,
                    search_range_list: ['标签'],
                    isIndeterminate: true,

                    // 是否是排除
                    negative: false,
                };
            }
            else if(command==1)//上传时间
            {
                filter = {
                    type : 1,
                    time_range: "",

                    // 是否是排除
                    negative: false,
                };
            }
            else if(command==2)//搜索id
            {
                filter = {
                    type: 2,
                    max_id: 200,
                    min_id: 0,

                    // 是否是排除
                    negative: false,
                };
            }
            this.adv_list.push(command)
            this.filters.push(filter)
            // this.$message('click on item ' + command);
        },
        remove_adv(index){
            this.adv_list.splice(index,1)
            this.filters.splice(index,1)
        },
        // 控制全选按钮
        search_range_handleCheckAllChange(val, filter_index) {
            this.filters[filter_index].search_range_list = val ? this.search_range_options : [];
            this.filters[filter_index].isIndeterminate = false;
        },
        search_range_handleCheckChange(val, filter_index) {
            // alert(filter_index)
            // alert(val)
            let checkedCount = val.length;
            this.filters[filter_index].search_range_checkAll = (checkedCount === this.search_range_options.length);
            // alert(checkedCount,this.search_range_options.length)
            this.filters[filter_index].isIndeterminate = checkedCount > 0 && checkedCount < this.search_range_options.length;
        },
        // 将输入的filter生成发送的filter
        filter_preprocess:function(filters){
            var new_filters = []
            for(var i=0;i<filters.length;i+=1)
            {
                var filter = filters[i]
                var new_filter = new Object()
                console.log(filter)
                new_filter.negative = filter.negative
                // 该filter筛选上传时间
                if(filter.type == 1)
                {
                    // alert(2)
                    new_filter.min_timestamp =  filter.time_range[0].getTime()
                    new_filter.max_timestamp =  filter.time_range[1].getTime()
                }
                // 该filter筛选文本
                else if(filter.type == 0)
                {
                    var keys = filter.keyword.split(" ");   // 使用空格分隔
                    while(keys.length != 0)
                    {
                        if(keys[0].length != 0)
                            break
                        keys.shift()
                    }
                    // console.log(keys)
                    var search_range = filter.search_range_list
                    // console.log(search_range)
                    for (var j=0;j<search_range.length;j+=1)
                    {
                        // console.log(j)
                        if(search_range[j]=='标签')
                        {
                            filter.tag = keys
                        }
                        else if(search_range[j]=='标题')
                        {
                            filter.title = keys
                        }
                        else if(search_range[j]=='简介')
                        {
                            filter.introduction = keys
                        }
                    }
                    if(filter.tag.length != 0)
                        new_filter.tag = filter.tag
                    if(filter.title.length != 0)
                        new_filter.title = filter.title
                    if(filter.introduction.length != 0)
                        new_filter.introduction = filter.introduction
                    filter.tag = []
                    filter.title = []
                    filter.introduction = []
                }
                // 该filter搜索年份
                else if(filter.type == 2)
                {
                    new_filter.max_id = filter.max_id
                    new_filter.min_id = filter.min_id
                }
                // alert(JSON.stringify(new_filter))
                new_filters.push(new_filter)
            }
            return new_filters
        },
        send: function(filter){
            var new_filter = filter.slice(0,filter.length)
            if(this.exhibit_id != null)
            {
                new_filter.push({
                    exhibit_id:String(this.exhibit_id),
                    negative:false,
                })
            }
            var data = {
                type: this.scope, //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: new_filter,
                order_name: this.order_name, // "early": 按时间由早到晚，"late": 按时间由最近到最早，"popularity": 点赞数由高到低
                order_method: this.order_method,
                unique: this.is_unique,
            }
            if(this.current_page!=null)
            {
                data.amount = String(this.amount) // 数字：返回多少条信息,不存在该key则全部返回
                data.page = String(this.current_page)
            }
            // alert(JSON.stringify(data))
            this.start_loading()
            var method = 'POST'
            var url = '/api/search'
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                // console.log("receive: "+object)
                
                my_this.result_list = object.mes
                my_this.resolve(object)
            }
            request_json(data,url,method,get_response)
        },
        // init_filters:function(){
        //     for (var i=0;i<this.filters.length;i+=1)
        //     {
        //         var filter = this.filters[i]
        //         filter.tag = []
        //         filter.title = []
        //         filter.introduction = []
        //     }
        // },
        // 高级搜索，发送filters
        send_adv_filters: function(){
            // alert(JSON.stringify(this.filters))
            // console.log(this.filters)
            this.send(this.filter_preprocess(this.filters))
            // this.init_filters()
        },
        // 普通默认搜索
        send_filter: function(){
            if(this.is_allow_advance_search==false)
            {
                this.$router.push({name:"search", params:{
                    ex_keyword: this.keyword,
                    ex_scope: this.scope,
                }})
                
                return
            }
                var keys = this.keyword.split(" ");   // 使用空格分隔
                // console.log(keys)
                // console.log(search_range)
                for (var j=0;j<this.search_range_options.length;j+=1)
                {
                    this.filter.tag = keys
                    this.filter.title = keys
                    this.filter.introduction = keys
                }
            // console.log([this.filter])
            this.send([this.filter])
        },
        // 从导航页去搜索页
        go_to_search_page: function(){
            this.$router.push({name:"search",params:{is_adv:true, ex_scope: this.scope}})
        },
        is_disable_first_adv: function(index){
            if(index==0 && this.is_adv==true)
                return true
            return false
        },
        default_search(){
            this.filters = []
            this.adv_list = []
            this.keyword = this.ex_keyword
                    // this.scope = this.ex_scope
                    this.send_filter()
                    this.$message('搜索中')
        },
        default_adv_search(){
            // this.scope = this.ex_scope
                    this.filters = []
                    this.adv_list = []
                    this.handleCommand(0)
                    this.filters[0].keyword = this.ex_keyword
                    this.send_adv_filters()
                    this.$message('搜索中')
        },
    },
    mounted:function(){
        // if(this.type!=null)
        // {
        //     this.display_scope = this.type
        // }
        // 在创建时需要检验是否自动搜索
        this.display_scope = this.scope
        if(this.ex_keyword!=null)
        {
                // 默认是普通搜索
                if(this.is_adv==false)
                {
                    this.default_search()
                    return
                }
                else
                {
                    this.default_adv_search()
                    return
                }
                
        }
        else{
                if(this.is_adv)
                {
                    // this.scope = this.ex_scope
                    this.keyword = ""
                }
        }
        if(this.auto_focus)
        {
            this.$nextTick(function(){
                this.$refs.search_input.$refs.input.focus();
            });
        }
        // 若是筛选器，则自动搜索所有
        if(this.is_filter)
        {
            this.keyword = ""
            this.send_filter()
            return
        }
    },
    watch:{
        // type(){
        //     if(this.type!=null)
        //     {
        //         this.display_scope = this.type
        //     }
        // },
        // 在ex_keyword更改时需要检验是否自动搜索
        ex_keyword:function(){
            if(this.ex_keyword!=null)
            {
                // 默认是普通搜索
                if(this.is_adv==false)
                {
                    this.default_search()
                    return
                }
                else
                {
                    this.default_adv_search()
                    return
                }
                
            }
            else{
                if(this.is_adv)
                {
                    // this.scope = this.ex_scope
                    this.keyword = ""
                }
            }
        },
        // 检测是否需要自动弹出高级搜索的栏目
        is_adv(){
            if(this.is_adv && this.ex_keyword==null)
            {
                // this.scope = this.ex_scope
                this.filters = []
                this.adv_list = []
                this.handleCommand(0)
            }
        },
        is_filter:function(){
            if(this.is_filter)
            {
                this.keyword = ""
                this.send_filter()
            }
        },
        scope(){
            this.display_scope = this.scope
        },
        search_again(){
            if(this.search_again==true)
            {
                this.search_resolve()
                // 判断是否是高级搜索
                if(this.filters.length!=0)
                    this.send_adv_filters()
                else
                    this.send_filter()
            }
        },
    },
}
</script>

<style>
    #search {
        width: 100%;
        background: none;
    }
    #search .el-select {
        width: 100%;
        border-radius: 0px;
    }
    .fill-container .el-dropdown, .fill-container .el-dropdown /deep/ .el-button {
        width: 100%;
        border-radius: 0px;
    }
    .fill-container .el-button {
        width: 100%;
    }
    .el-card {
        padding: 5px;
    }
    @media screen and (max-width: 768px) {
        .el-card /deep/ .el-checkbox__label{
            font-size: 10px;
        }
        .el-checkbox{
            margin-right: 5px;
        }
    }
</style>