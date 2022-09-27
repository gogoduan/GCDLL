<template>
  <div id="message_list">
    <!--复用messagelist展示用户数据-->
    <h2>修改照片名称等</h2>
    <ChangeBlock v-for="(changeblock, index) in imgList" :key = index
    :get_fresh = "refresh"
    :name = "changeblock.name"
    :introduction = "changeblock.introduction"
    :id = "changeblock.id"
    :img_src = "changeblock.img_src">
    </ChangeBlock>
  </div>
</template>

<script>
import ChangeBlock from "@/components/ChangeBlock"
import {request_json} from "@/utils/communication"
export default {
	name: "ChangeInfo",
	components: {
		ChangeBlock
	},
  data(){
  return{
  imgList:[
  {
  name:"name8",
  introduction:"introduction8",
  id:14,
  img_src:"https://img0.baidu.com/it/u=617532475,2586514872&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667"
  },
  {
  name:"name8",
  introduction:"introduction8",
  id:14,
  img_src:"https://img0.baidu.com/it/u=617532475,2586514872&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667"
  },
  {
  name:"name8",
  introduction:"introduction8",
  id:14,
  img_src:"https://img0.baidu.com/it/u=617532475,2586514872&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667"
  }
  ]
  }
  },
	props: {
	},
  methods:{
  refresh(){
  request_json('','/api/useradmin/','GET',"getlist");
  }
  },
  created(){
  request_json('','/api/useradmin/','GET',"getlist");
  }
}
</script>