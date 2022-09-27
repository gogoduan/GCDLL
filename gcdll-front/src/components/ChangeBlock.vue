<template  class = "my-gallery">
<div>
<div class = "thumbs">
<vue-preview :slides="thumbsList" @close="handleClose"></vue-preview>
</div>

      name:{{name}}  introduction:{{ introduction }}
      <div class = "insideinfo"><el-input  v-model = "newtext" placeholder = "输入修改的内容"></el-input>
      <el-button @click = "changename">修改名称</el-button>
      <el-button @click = "changeintro">修改简介</el-button>
      </div>
      </div>
</template>

<script>

import {request_json} from "@/utils/communication"
export default {
	name: "ChangeBlock",
  props:{
  thumbsList:{
  type:Array,
  default:()=>new Array(1).fill({
  src: "https://img0.baidu.com/it/u=617532475,2586514872&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667",
  msrc: "https://img0.baidu.com/it/u=617532475,2586514872&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667",
  w: 600,
  h: 600
  })
  },
  get_fresh:{
  type:Function,
  required:true
  },
  img_src:{
  type:String,
  default:()=>"https://img0.baidu.com/it/u=617532475,2586514872&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667",
  },
  id:{
  type:Number,
  default:()=>14,
  },
  introduction:{
  type:String,
  default:()=>"This is intro1",
  },
  name:{
  type:String,
  default:()=>"name1",
  }
  },
	data(){
  return{
  newtext:"",
  }
  },
  methods:{
  getall(){
  this.thumbsList = [{w:600,h:600,src:this.img_src,msrc:this.img_src}]
  },
  changename(){
  var a = "change_name";
  var send = {};
  var data = {};
  data['new'] = this.newtext;
  data['id'] = this.id;
  send['data'] = data;
  send['wanted'] = a;
  request_json(send,'/api/photoadmin','POST');
  this.get_fresh();
  },
  changeintro(){
  var a = "change_intro";
  var send = {};
  var data = {};
  data['new'] = this.newtext;
  data['id'] = this.id;
  send['data'] = data;
  send['wanted'] = a;
  request_json(send,'/api/photoadmin','POST');
  this.get_fresh();
  }
  }
}
</script>

<style scoped>
.my-gallery:after {
content: "";
display: block;
visibility: hidden;
clear: both;
height: 0
}
figure {
width: 100px;
height: 100px;
float: left;
margin: .100px;
padding: 0;
}
.thumbs {
  /deep/ .my-gallery {
  display:flex;
  flex_wrap:wrap;
  figure{
    width:10%;
  }
  }

}
</style>