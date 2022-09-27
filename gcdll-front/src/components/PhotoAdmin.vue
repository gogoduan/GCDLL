<template>
    <div id="photo-admin">
        <el-collapse v-model="fix_on" class="photo-block" id="fix-photos" accordion>
        <el-collapse-item name="1">
            <template slot="title">
            <el-row id="fixing-header" style="width:100%">
                <b class="admin-text-title">修复照片</b>
                <el-tooltip :content="fix_lock?'解锁':'锁定自动开闭'" placement="top">
                    <el-button class="lock-button" type="text" @click.stop.prevent="fix_lock=!fix_lock" style="font-size:200%;color:grey">
                        <a-icon v-if="fix_lock" type="lock" />
                        <a-icon v-else type="unlock" />
                    </el-button>
                </el-tooltip>
            </el-row>
            </template>
            <fix-photo :refresh="refresh" :refix_list="refix">
            </fix-photo>
        </el-collapse-item>
        </el-collapse>
        <el-collapse v-model="fixing_on" class="photo-block" id="fixing-photos" accordion>
        <el-collapse-item name="1">
            <template slot="title">
            <el-row id="fixing-header" style="width:100%">
                <b class="admin-text-title">修复中照片预览</b>
                <el-tooltip :content="fixing_lock?'解锁':'锁定自动开闭'" placement="top">
                    <el-button class="lock-button" type="text" @click.stop.prevent="fixing_lock=!fixing_lock" style="font-size:200%;color:grey">
                        <a-icon v-if="fixing_lock" type="lock" />
                        <a-icon v-else type="unlock" />
                    </el-button>
                </el-tooltip>
                <a style="box-sizing:border-box; float: right;" @click="go_to_past('修复中')">
                    查看更多
                </a>
            </el-row>
            </template>
        
            <div id="fixing-content">
                <div class="button-item">
                    <el-button circle type="text">
                            <i class="el-icon-loading">
                            </i>
                    </el-button>
                    <div class="button-row">
                    <el-button type="danger" v-on:click="go_to_edit('修复中')">
                        前往删除
                    </el-button>
                    </div>
                </div>
                <div class="slidebar">
                    <el-empty v-if="fixing.length==0" description="没有正在修复的照片" :image-size="100">
                        
                    </el-empty>
                    <transition-group name="listgroup" tag="ul">
                    <div class="image-item" v-for="image in fixing" :key="image.id" >
                        <div class="item-box">
                            <ExhibitBlock  :id="image.id" :name="image.name" 
                            :image_src="image.img_src" :introduction="image.introduction"
                            :timestamp="image.timestamp" :tag_list="image.tag_list"
                            :likes="image.likes" :comments="image.comments"
                            :is_progress="true" :expect_time="image.expect_time" :now_time="image.now_time" :wait_time="image.wait_time"
                            :operation="image.operation"
                             :jump_to="{name: 'repair_info'}" state="sketch">
                            </ExhibitBlock>
                        </div>
                    </div>
                    </transition-group>
                </div>
            </div>
            <el-row style="text-align: center;margin-top: 10px;">
                <el-pagination class="page-footer"
                background
                @current-change="handleCurrentChange"
                :current-page.sync="fixing_current_page"
                layout="total, prev, pager, next"
                :page-size="5"
                :total="Number(fixing_total)">
                </el-pagination>
            </el-row>
        </el-collapse-item>
        </el-collapse>
        <transition name="fade">
        <el-collapse v-model="fix_failed_on" class="photo-block" id="fix-failed-photos" v-if="fix_failed.length > 0">
        <el-collapse-item name="1">
            <template slot="title" id="fixing-header" class="header">
                <el-row style="width:100%">
                <b class="admin-text-title">修复失败图片</b>
                <el-tooltip :content="fix_failed_lock?'解锁':'锁定自动开闭'" placement="top">
                    <el-button class="lock-button" type="text" @click.stop.prevent="fix_failed_lock=!fix_failed_lock" style="font-size:200%;color:grey">
                        <a-icon v-if="fix_failed_lock" type="lock" />
                        <a-icon v-else type="unlock" />
                    </el-button>
                </el-tooltip>
                <a style="box-sizing:border-box; float: right;" @click="go_to_past('修复失败')">
                    查看更多
                </a>
                </el-row>
            </template>
            <div id="fixing-content">
                <div class="button-item">
                    <div class="button-row">
                    <el-button type="warning" v-on:click="add_photo(true)">
                        重新修复
                    </el-button>
                    </div>
                    <div class="button-row">
                    <el-button type="danger" v-on:click="go_to_edit('修复失败')">
                        前往删除
                    </el-button>
                    </div>
                </div>
                <div class="slidebar">
                    <transition-group name="listgroup" tag="ul">
                    <div class="image-item" v-for="image in fix_failed" :key="image.id" >
                        <div class="item-box">
                            <ExhibitBlock  :id="image.id" :name="image.name" :image_src="get_random_src(image.img_src)" 
                            :timestamp="image.timestamp" :tag_list="image.tag_list"
                            :likes="image.likes" :comments="image.comments"
                            :introduction="image.introduction" state="sketch">
                            </ExhibitBlock>
                        </div>
                    </div>
                    </transition-group>
                </div>
            </div>
        </el-collapse-item>
        </el-collapse>
        </transition>

        <el-collapse v-model="fixed_on" class="photo-block" id="fixed-photos">
            <el-collapse-item name="1">
                <template slot="title" id="fixing-header" class="header">
                    <el-row id="fixing-header" style="width:100%">
                        <b class="admin-text-title">已修复照片预览</b>
                        <el-tooltip :content="fixed_lock?'解锁':'锁定自动开闭'" placement="top">
                            <el-button class="lock-button" type="text" @click.stop.prevent="fixed_lock=!fixed_lock" style="font-size:200%;color:grey">
                                <a-icon v-if="fixed_lock" type="lock" />
                                <a-icon v-else type="unlock" />
                            </el-button>
                        </el-tooltip>
                        <el-button type="success" @click.stop.prevent="refresh();$message('刷新中')">
                            刷新
                        </el-button>
                        <a style="box-sizing:border-box; float: right;" @click="go_to_past('已修复')">
                            查看更多
                        </a>
                    </el-row>
                </template>
            <div id="fixing-content">
                <div class="button-item">
                    <el-button circle type="success" v-on:click="add_photo">
                            <i class="el-icon-plus">
                            </i>
                    </el-button>
                </div>
                <div class="slidebar">
                    <el-empty v-if="fixed.length==0" description="没有已修复的照片" :image-size="100">
                    </el-empty>
                        
                    <transition-group name="listgroup" tag="ul">
                    <div class="image-item" v-for="image in fixed" :key="image.id" >
                        <div class="item-box">
                            <ExhibitBlock  :id="image.id" :name="image.name" :image_src="get_random_src(image.img_src)" 
                            :timestamp="image.timestamp" :tag_list="image.tag_list"
                            :likes="image.likes" :comments="image.comments"
                            :introduction="image.introduction" state="sketch">
                            </ExhibitBlock>
                        </div>
                    </div>
                    </transition-group>
                </div>
            </div>
            
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import ExhibitBlock from './ExhibitBlock.vue'
import FixPhoto from './FixPhoto.vue'
// import SearchPage from './SearchPage.vue'
import {request_json} from '@/utils/communication'

export default {
    name: "PhotoAdmin",
    components: {
        ExhibitBlock,
        FixPhoto
        // SearchPage,
    },
    props: {

    },
    data(){
        return {
            refresh_cnt: 0,

            refix: [],
            fix_on:"1",
            fixing_on: "1",
            fixed_on: "2",
            fix_failed_on: "2",

            fix_lock: false,
            fixing_lock: false,
            fixed_lock: false,
            fix_failed_lock: false,

            fixed: [],
            fixing: [],
            fix_failed: [],
            progress_timer: null,
            request_id: 0,
            fixing_total: 0,
            fixing_current_page: 1,
        }
    },
    methods: {
        handleCurrentChange() {
            this.update_fixing_photo()
        },
        add_photo(refix=false) {
            // this.$router.push({name: 'fix_photo'})
            this.fix_on = '1'
            // const TOP = document.getElementById("fix-photos")
            // const y = TOP.offsetTop
            document.body.scrollTop = document.documentElement.scrollTop = 0;
            if(refix){
                this.refix = this.fix_failed.slice(0,this.fix_failed.length)
            }
        },
        go_to_past(tag) {
            this.$router.push({name: 'past', params:{ tag: tag }})
        },
        go_to_edit(tag) {
            this.$router.push({name: 'editphoto', params:{ keyword:tag, is_adv: true }})
        },
        lazy_update_fixing(new_list){
            var already_in = new Array(new_list.length).fill(0)
            var old_list = this.fixing.slice(0,this.fixing.length)
            this.fixing = new_list.slice(0,new_list.length)
            const my_this = this
            old_list.forEach(function(item){
                my_this.fixing.forEach(function(new_item, new_index){
                    if(item.id == new_item.id)
                    {
                        already_in[new_index] = 1
                        my_this.$set(new_item,'expect_time',item.expect_time)
                        my_this.$set(new_item,'operation',item.operation)
                        my_this.$set(new_item,'now_time',item.now_time)
                        my_this.$set(new_item,'wait_time',item.wait_time)
                    }
                })
            })
            this.fixing.forEach(function(item, new_index){
                if(!already_in[new_index])
                {
                    if(!my_this.fixing_lock)    
                        my_this.fixing_on = "1"
                    my_this.$set(item,'expect_time',100)
                    my_this.$set(item,'operation',"正在向后端查询中")
                    my_this.$set(item,'now_time',0)
                    my_this.$set(item,'wait_time',0)
                }
            })
            if(this.fixing.length==0){
                setTimeout(function(){
                    if(!my_this.fixing_lock)
                        my_this.fixing_on = "2"
                },2000)
            }
        },
        update_fixing_photo: function(){
            var data = {
                type: 'photo', //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: [
                    {
                        tag: ['修复中'],
                    }
                ],
                unique: false,
                page: this.fixing_current_page,
                amount: "5", // 数字：返回多少条信息,不存在该key则全部返回
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
                my_this.fixing_total = response.data.total
                // my_this.fixing = object
                my_this.lazy_update_fixing(object)
            }
            request_json(data,url,method,get_response)
        },
        update_fixed_photo: function(){
            this.request_id += 1;
            var data = {
                type: 'photo', //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: [
                    {
                        tag: ['已修复'],
                    },
                ],
                page:"1",
                unique: false,
                amount: "20", // 数字：返回多少条信息,不存在该key则全部返回
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
                
                my_this.fixed = object
            }
            request_json(data,url,method,get_response)
        },
        update_fix_failed_photo: function(){
            this.request_id += 1;
            var data = {
                type: 'photo', //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: [
                    {
                        tag: ['修复失败'],
                    },
                ],
                page:"1",
                unique: true,
                amount: "20", // 数字：返回多少条信息,不存在该key则全部返回
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
                
                my_this.fix_failed = object.slice(0,object.length)
                if(object.length > 0)
                {
                    if(!my_this.fix_failed_lock)
                        my_this.fix_failed_on = "1"
                }
            }
            request_json(data,url,method,get_response)
        },
        repair_info_update: function(id){
            var data = {id: String(id)}
            var method = 'GET'
            var url = '/api/repair'
            // alert(1)
            const my_this = this
            var get_response = function (res) { 
                var response = res
                var object = response.data
                if(object==undefined)
                {
                    return
                }
                var index=-1
                for(let i=0;i<my_this.fixing.length;i+=1)
                {
                    if(my_this.fixing[i].id == id)
                    {
                        index = i
                        break
                    }
                }
                if(index==-1)
                {
                    // my_this.refresh()
                    return
                }
                var item = my_this.fixing[index]
                // 当正在进行的操作改变时，自动刷新搜索
                if(item.operation!=undefined)
                {
                    if(item.operation != object.operation)
                    {
                        // console.log(item.operation,object.operation)
                        if(!my_this.fixed_lock)
                            my_this.fixed_on = "1"
                        // 当上次刷新后超过1s再刷新
                        if(my_this.refresh_cnt==0)
                            my_this.refresh()
                    }
                }
                my_this.$set(item,'expect_time',Number(object.expect_time))
                my_this.$set(item,'operation',object.operation)
                my_this.$set(item,'now_time',Number(object.now_time))
                my_this.$set(item,'wait_time',Number(object.wait_time))
                // 当全部完成时，自动刷新搜索
                if(Boolean(object.flag)==true)
                {
                    my_this.refresh()
                    return
                }
                my_this.fixing[index] = item
                // my_this.fixing.splice(index,1,item)
                // console.log(my_this.fixing[index],object.flag)
                }
            request_json(data,url,method,get_response)
            
        },
        update_fixing_progress(){
            for(var i=0;i<this.fixing.length;i+=1)
            {
                var id = this.fixing[i].id
                const my_this = this
                const my_id = id
                setTimeout(function(){
                    my_this.repair_info_update(my_id)
                }, (i+1)*200)
            }
        },
        refresh(){
            if(!this.fix_lock)
                this.fix_on = "2"
            const my_this = this
            this.refresh_cnt = 1
            setTimeout(()=>{
                my_this.refresh_cnt = 0
            },1500)
            this.update_fixing_photo();
            this.update_fixed_photo();
            this.update_fix_failed_photo();
            // this.request_id += 1;
            if(this.progress_timer==null){
                this.start_timer()
            }
            if(this.fixing.length>0)
                return 1
            return 0
        },
        start_timer(){
            const my_this = this
            this.end_timer()
            this.progress_timer = setInterval(function(){
                if(Number(my_this.fixing_on)==1)
                    my_this.update_fixing_progress()
            },1200)
        },
        end_timer(){
            clearInterval(this.progress_timer)
            this.progress_timer = null
        },
        get_random_src(src){
            return src
            // +"?id="+String(this.request_id)
        },
    },
    beforeRouteEnter(from,to,next){
        next(vm=>{
            vm.refresh()
            // const my_vm = vm
            setTimeout(function(){
                if(vm.fixing.length==0){
                    vm.refresh()
                }
            },2000)
            
            vm.start_timer()
        })
    },
    beforeRouteLeave(from,to,next){
        this.end_timer()
        next()
    },
    created:function(){
        this.update_fixing_photo()
        this.update_fixed_photo()
        this.update_fix_failed_photo()
    },
    watch:{
        // fixing:function(){
        //     this.update_fixing_progress()
        // },
    }
}
</script>

<style scoped>
    .photo-block{
        /* min-height: 250px; */
        text-align: left;
        background: white;
        border-radius: 20px;
        padding:10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    }
    #fixing-content {
        height: 200px;
        display: flex;
    }

    .el-empty{
        padding:0
    }
    
    .slidebar {
        height: 200px;
        width: 85%;
        /* 沿x轴滑动查看照片 */
        white-space: nowrap;
        justify-content: space-between;
        overflow-y: hidden;
        overflow-x: auto;
    }

    .admin-text-title{
        font-size:150%; 
        box-sizing:border-box; 
        float: left; 
        margin-right: 20px;
    }
    .image-item {
        display: inline-block;  /* 横向滚动 */
        height: 200px;
        width: 200px;
        float: none;
        margin: 10px;
        padding: 0;
        
    }

    .item-box {
        display:flex;
        height: 100%;
        width: 100%;
    }

    .button-item {
        /* float: left; */
        height: 200px;
        width: 15%;
        align-self: center;
        text-align: center;
        display:inline-flex;
        flex-wrap: wrap;
    }

    .button-item .button-row{
        width:150px;
        height:60px;
    }

    .button-item .el-button {
        /* 居中 */
        display: block;
        margin: auto;
        align-self: center;
    }

    .button-item div {
        /* 居中 */
        display: block;
        margin: auto;
        align-self: center;
    }

    .el-icon-plus {
        font-size: 400%;
    }

    .el-icon-loading {
        font-size: 400%;
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
        transform: translateY(50px);
    }
    .listgroup-move {
        transition: transform 1s;
    }

    .fade-enter-active {
        transition: all 1s ease;
    }

    .fade-enter /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
        transform: translateX(50px);
    }
</style>