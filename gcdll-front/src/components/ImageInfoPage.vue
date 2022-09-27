<template>
  <div id="image-info-page">
    <el-row>
      <el-col :span="14" class="main" :xs="{span:24}">
        <!-- 图片版面 -->
        <ImagePicBoard :user_state="userstate" :image_info="image_info" :image_operation="image_operation" :openlogin="openlogin">
        </ImagePicBoard>
      </el-col>
      <el-col :span="9" class="main" :xs="{span:24}">
        <!-- 图片详情版面 -->
        <image-info-board :user_state="userstate" 
        :type='1' :id="Number(image_info.id)" 
        :image_operation="image_operation" :need_update="image_info_page_update"
        :image_info="image_info" :openlogin="openlogin"
        :tag_list="image_info.tag_list">
        </image-info-board>
      </el-col>
    </el-row>
  </div>
</template>

<script>
// import ImageInfoBoard from "@/components/ImageInfoBoard"
import ImageInfoBoard from './ImageInfoBoard.vue'
import ImagePicBoard from './ImagePicBoard.vue'
import {request_json} from '@/utils/communication.js'

// 照片详情页
export default {
  name: "ImageInfoPage",
  components: {
    ImageInfoBoard,
    ImagePicBoard,
  },
  props: {
    // 账户
        userstate:{
            type: Object,
            required: true
        },
    // 照片id，从router来
      id: {
            type:String,
            require:true
        },
        openlogin:{
            type:Function,
            require:true
        },
        url_error_report:{
            type:Function,
            require:true
        },
  },
  data(){
		return {
      image_info:{},
    }
  },
  computed:{
      // // 图片id
      
  },
  created: function(){
    // TODO: 解决user state没有传进来的bug——手动刷新
    if(this.userstate==undefined)
    {
      alert(1)
      // this.$router.go(0);
    }
    this.image_info_page_update()
  },
  methods:{
    image_info_page_update: function(){
      var data = {id:this.id}
      var method = 'GET'
      var url = '/api/photo'
      const my_this = this
      var get_response = function (res) { 
          var response = res
          var object = response.data
          if(object.status!=undefined)
          {
              my_this.$message.error(object.detail);
              my_this.url_error_report()
              return
          }
          my_this.image_info = object
          console.log(object)
      }
      request_json(data,url,method,get_response)
      
    },

    // 给照片点赞、评论 需要cookie
    image_operation: function(type, content){
            var data = {
                    id:String(this.id),
                    type:String(type),
                    content:content,
                }
            var method = 'POST'
            var url = '/api/photo'
            const my_this = this
            var get_response = function (res) { 
                var object = res.data
                if(object.status!=undefined)
                {
                    my_this.$message.error(object.detail);
                    return
                }
                var message = ""
                if(type==1)
                  message = "点赞"
                else if(type==3)
                  message = "取消点赞"
                else
                  message = "发送评论"

                my_this.$message({
                  type:'success',
                  message: "成功"+message,
                })
                my_this.image_info_page_update()
            }
            // alert(this.id)
            request_json(data, url, method, get_response)
        },
  },
  watch:{
    userstate:function(){
      
      alert(JSON.stringify(this.userstate))
    }
  }
}
</script>

<style scoped>
  #image-info-page {
    padding: 5px;
  }

  @media screen and (min-width: 768px){
        .main{
            margin:10px;
        }
    }

  .el-col{
    height:600px;
  }

  .main {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    background-color: white;
    text-align: center;
    overflow: hidden;
    /* min-width: 500px; */
    padding:5px;
  }
</style>