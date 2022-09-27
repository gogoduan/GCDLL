<template>
    <div class="photos-edit-page">
        <div id="exhibit-admin-header" class="header">
            <b style="font-size:150%; box-sizing:border-box; float: left;">
                {{name_type[edit_type].label}}信息编辑
            </b>
        </div>
        <!-- 添加key重新渲染 -->
        <div v-if="edit_type=='photo'"  id="photo-info" :key="0">   
            <search-page :key="0" :display_type="'list'" :type="0" :range='edit_type' :force_unique="false"
                state='choosable' :keyword_from_props="keyword" :scope_from_props="'photo'" :is_adv="is_adv">
            </search-page>
        </div>
        <div v-else  id="photo-info" :key="1">   
            <search-page :key="1" :display_type="'list'" :type="1" :range='edit_type' :force_unique="true"
                state='choosable' :keyword_from_props="keyword" :scope_from_props="'exhibit'">
            </search-page>
        </div>
    </div>
</template>
        
<script>
import SearchPage from './SearchPage.vue'
// import {request_json} from '@/utils/communication'

export default {
    name: "PhotosEditPage",
    components: {
        SearchPage,
    },
    props: {

    },
    data(){
        return {
            keyword: null,
            is_adv:false,
            name_type:{
                'photo':{
                    type: 0,
                    label: '照片'
                },
                'exhibit':{
                    type: 1,
                    label: '展览'
                }
            }
        }
    },
    computed:{
        edit_type(){
            if(this.$route.name=='editphoto')
                return 'photo'
            else
                return 'exhibit'
        }
    },
    watch:{
        $route(){
            if(this.$route.params.keyword != undefined)
                this.keyword = this.$route.params.keyword
            else
                this.keyword = null
            if(this.$route.params.is_adv != undefined)
                this.is_adv = this.$route.params.is_adv
            // alert()
        }
    },
    created(){
        if(this.$route.params.keyword != undefined)
                this.keyword = this.$route.params.keyword
        if(this.$route.params.is_adv != undefined)
                this.is_adv = this.$route.params.is_adv
    }
}
</script>
