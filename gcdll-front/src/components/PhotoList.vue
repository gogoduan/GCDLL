<template>
  <div id="photo-list">
    <el-row style="height:70px; display: flex;">
      <b style="font-size:150%; box-sizing:border-box;margin:auto">
              查看所有照片
          </b>
      <div style="display:block;margin:auto">
        <el-row>
          <el-button circle type="success" v-on:click="jumpchange" style="font-size:200%">
            <i class="el-icon-plus"></i>
          </el-button>
        </el-row>
        <el-row style="font-size:80%">
          上传照片
        </el-row>
      </div>
    </el-row>
    <SearchPage :type="0" state = "display" range = "photo"
      :keyword_from_props="tag" :scope_from_props="'photo'" :is_adv="is_adv"
      :resolve="resolve"
      >
    </SearchPage>
  </div>
</template>

<script>
import SearchPage from "@/components/SearchPage"
export default {
  name: 'PhotoList',
  components:{
  SearchPage
  },
  props: {

  },
  data() {
    return {
      tag: null,
      is_adv: false,
    };
  },
  methods:{
  resolve(){

  },
  jumpchange(){
      this.$router.push({name:"photo"});
  }
  },
    watch:{
        $route(){
            if(this.$route.params.tag != undefined)
            {
                this.tag = this.$route.params.tag
                this.is_adv = true
            }
        }
    },
    created(){
        if(this.$route.params.tag != undefined)
            {
                this.tag = this.$route.params.tag
                this.is_adv = true
            }
    }
}
</script>

<style scoped>
.carding {
  float:left;
}
</style>