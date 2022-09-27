<template>
    <div id="search-result-page">
        <search-page :is_filter="false" state="display"
        :keyword_from_props="ex_keyword" :is_adv="is_adv" :scope_from_props="ex_scope">
        </search-page>
    </div>
</template>


<script>
import SearchPage from './SearchPage.vue'
// 搜索的照片/展览库
export default {
    name: "SearchResultPage",
    components: {
        SearchPage
    },
    data(){
        return{
            ex_keyword:null,
            is_adv:false,
            ex_scope:null,
        }
    },
    activated(){
        var a = this.$route.params.is_adv
        if(a!=undefined && a==1)
        {
            this.ex_keyword = null
            this.is_adv = Boolean(a)
        }
        else
        {
            this.is_adv = false
            this.ex_keyword = this.$route.params.ex_keyword
        }
        this.ex_scope = this.$route.params.ex_scope
    }
}
</script>

<style scoped>

</style>
