<template>
<div>
	<el-row style="height:70px; display: flex;">
		<b style="font-size:150%; box-sizing:border-box;margin:auto">
            查看所有展览
        </b>
		<div style="display:block;margin:auto">
			<el-row>
				<el-button circle type="success" v-on:click="newGallery" style="font-size:200%">
					<i class="el-icon-plus"></i>
				</el-button>
			</el-row>
			<el-row style="font-size:80%">
				添加展览
			</el-row>
		</div>
	</el-row>

<SearchPage
:type="1"
state = "display"
range = "exhibit"
>
</SearchPage>
</div>
</template>

<script>
import SearchPage from "@/components/SearchPage"
export default {
	name: "GalleryList",
  components:{
  SearchPage
  },
	props: {
  pastGallery: {
    type: Array,
    default: () => new Array(5).fill({
      name:"first",
			info:"111",
      urlsource:'https://img2.baidu.com/it/u=2259391972,2688676787&fm=253&fmt=auto&app=138&f=JPEG?w=499&h=332',
			timestamp:3715289999,
    })
  },
	},
	methods:{
	newGallery:function(){
		this.$router.push({name:"gallery"});
	},
	},
	created(){
		
	},
}
</script>

<style scoped>
</style>