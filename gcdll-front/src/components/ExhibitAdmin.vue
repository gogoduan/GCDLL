<template>
    <div id="exhibit-admin">
        <div id="exhibit-roll">
            <el-collapse v-model="new_gallery_on" class="photo-block" id="new_gallery" accordion>
            <el-collapse-item name="1">
                <template slot="title">
                <el-row id="exhibit-admin-header" style="width:100%">
                    <b class="admin-text-title">新建展览</b>
                </el-row>
                </template>
                <new-gallery :refresh="refresh">
                </new-gallery>
            </el-collapse-item>
            </el-collapse>
            <el-collapse v-model="gallery_on" class="photo-block" id="gallery-view" accordion>
            <el-collapse-item name="1">
                <template slot="title">
                    <el-row id="fixing-header" style="width:100%">
                        <b class="admin-text-title">已设立展览预览</b>
                        <a style="box-sizing:border-box; float: right" @click="go_to_gallery_list">
                            查看更多
                        </a>
                    </el-row>
                </template>
                <div id="exhibit-admin-content">
                    <div class="button-item">
                        <el-button circle type="success" @click="add_gallery">
                                <i class="el-icon-plus">
                                </i>
                        </el-button>
                    </div>
                    <div class="slide-bar">
                        <transition-group name="listgroup" tag="ul">
                        <div class="image-item" v-for="image in exhibit_list" :key="image.id" >
                            <div class="item-box">
                                <ExhibitBlock  :type=1 :id="image.id" 
                                :name="image.name" :image_src="image.img_src" 
                                :introduction="image.introduction" 
                                :timestamp="image.timestamp" :tag_list="image.tag_list"
                                :likes="image.likes" :comments="image.comments"
                                state="sketch">
                                </ExhibitBlock>
                            </div>
                        </div>
                        </transition-group>
                    </div>
                </div>
                </el-collapse-item>
            </el-collapse>
        </div>
    </div>
</template>

<script>
import ExhibitBlock from './ExhibitBlock.vue'
// import SearchPage from './SearchPage.vue'
import NewGallery from './NewGallery.vue'
import {request_json} from '@/utils/communication.js'

// 管理主页中 展览管理版面
export default {
    name: "ExhibitAdmin",
    components: {
        ExhibitBlock,
        // SearchPage,
        NewGallery
    },
    props: {
    },
    data(){
        return {
            exhibit_list: [],
            new_gallery_on: '1',
            gallery_on: '2',
        }
    },
    methods: {
        add_gallery() {
            // this.$router.push({name: 'new_gallery'})
            this.new_gallery_on = '1'
            this.gallery_on = '2'
            document.body.scrollTop = document.documentElement.scrollTop = 0;
        },
        refresh(){
            this.gallery_on = '1'
            this.new_gallery_on = '2'
            this.update_admin_gallery()
        },
        update_admin_gallery() {
            var data = {
                type: 'exhibit', //搜索种类："photo","exhibit",//暂时不搜索"user"
                filters: [
                    {
                        tag:[],
                    }
                ],
                page: "1",
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
                console.log("receive: "+object)
                
                my_this.exhibit_list = object
            }
            request_json(data,url,method,get_response)
        },
        go_to_gallery_list(){
            this.$router.push('gallerylist')
        },
    },
    created() {
        this.update_admin_gallery()
    }
}
</script>

<style scoped>
    #exhibit-roll {
        /* border-bottom-style: solid; */
        min-height: 200px;
        text-align: left;
    }
    .photo-block{
        /* min-height: 250px; */
        text-align: left;
        background: white;
        border-radius: 20px;
        padding:10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    }
    #exhibit-admin-content {
        height: 200px;
        display: flex;
    }
    
    .slide-bar {
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
    .header {
        min-height: 60px;
        border-bottom: solid;
    }

    .item-box {
        display:flex;
        height: 100%;
        width: 100%;
    }

    .button-item {
        float: left;
        height: 200px;
        width: 15%;
        align-self: center;
        text-align: center;
        display:inline-flex;
    }

    .button-item .el-button {
        /* 居中 */
        display: block;
        margin: auto;
        align-self: center;
    }

    .el-icon-plus {
        font-size: 400%;
    }

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

</style>