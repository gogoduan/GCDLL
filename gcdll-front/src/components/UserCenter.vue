<template>
    <div class="user-center">
        <el-row>
            <el-col :span="6">
                <el-tag effect="dark" style="font-size:150%"
                    :type="(state.type=='admin')?'danger':'success'" size="medium">
                    {{(state.type=='admin')?'管理员':'游客'}}
                </el-tag>
            </el-col>
            <!-- 头像部分 -->
            <el-col :span="12" >
                <div @mouseenter="handle_mouse_enter"  @mouseleave="handle_mouse_leave" style="width:100px;margin:auto">
                    <!-- 用key强制刷新 -->
                    <el-avatar v-if="new_cover.length==0" :size="100" fit="cover" :src="get_random_src" :key="state.avatar">
                        <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>
                    </el-avatar>
                    <el-avatar v-else :size="100" :src="new_cover[0].url" fit="cover">
                    </el-avatar>
                    <div class="button-modal" v-if="show_modal">
                                    <div class="text-modal-wrapper">
                                    </div>
                                    <div class="button-container center-align-box">
                                        <el-col :span="24">
                                            <el-upload class="my-upload"
                                                action="#" :on-change="handlechange"
                                                list-type="picture-card"
                                                :auto-upload="false"
                                                :show-file-list="false"
                                                :file-list ="new_cover"
                                                :multiple="false"
                                                accept=".jpg,.png,.bmp,.jpeg"
                                                :limit ="1"
                                                >
                                                <i slot="default" class="el-icon-plus"></i>
                                            </el-upload>
                                        </el-col>
                                    </div>
                    </div>
                </div>
                <el-row>
                    <span>
                        {{  state.username  }}
                    </span>
                </el-row>
            </el-col>
            <!-- 上传头像操作 -->
            <el-col :span="6">
                <el-row v-if="new_cover.length > 0">
                    <span class="bottom-box">
                        已上传新头像
                    </span>
                            <el-col :span="24">
                            <el-button class="bottom-box" type="warning" @click="withdraw_cover">
                                撤销
                            </el-button>
                            </el-col>
                            <el-col :span="24">
                            <el-button class="bottom-box" type="success" @click="change_avatar">
                                确认
                            </el-button>
                            </el-col>
                        </el-row>
            </el-col>
        </el-row>
        <el-skeleton v-if="user_info.state==null">
        </el-skeleton>
        <el-row v-else>
            <el-descriptions title="用户信息" :column="2">
                <el-descriptions-item label="用户名">{{state.username}}</el-descriptions-item>
                <el-descriptions-item label="id">{{state.user_id}}</el-descriptions-item>
                <el-descriptions-item label="注册时间">{{register_datetime}}</el-descriptions-item>
                <!-- <el-descriptions-item label="上次登陆时间">{{login_datetime}}</el-descriptions-item> -->
            </el-descriptions>
            <el-descriptions title="违规情况" :column="1">
                <el-descriptions-item label="当前状态"> {{user_info.state}} </el-descriptions-item>
                <el-descriptions-item label="权限">
                    <el-tag effect="dark"
                    v-for="item in user_info.permissions" :key="item.label"
                    :type="(Boolean(item.type))?'success':'danger'" size="mini">
                    {{(Boolean(item.type))?'可':'不可'}}{{item.label}}
                    </el-tag>
                </el-descriptions-item>
            </el-descriptions>
        </el-row>
    </div>
</template>

<script>
import {request_json} from '@/utils/communication.js'
export default {
  name: 'UserCenter',
  components: {
      
  },
  props:{
      state:{
          type:Object,
          required:true,
      },
      update:{
          type:Function,
          required:true,
      },
      visible:{
          type:Boolean,
          required:true,
      }
  },
  data(){
    return{
        request_id: Math.random(),
        show_modal: false,
        new_cover: [],
        base_list: [],

        // 
        user_info:{
            register_time: 1234235498435,
            login_time: 1234935493455,
            state: null,
            permissions:[
                {
                    label: "访问修复详情",
                    type: true,
                },
                {
                    label: "点赞与评论",
                    type: false,
                }
            ],
        }
    }
  },
  methods:{
        handle_mouse_enter:function(){
            
            this.show_modal = true
        },
        handle_mouse_leave:function(){
            // alert(1)
            this.show_modal = false
        },
        handlechange(file,fileList){
            this.new_cover = fileList;
            console.log(this.new_cover)
            var reader = new FileReader();
            reader.readAsDataURL(file.raw);
            reader.onload=()=>{
            this.base_list.push(reader.result);
            }
        },
        withdraw_cover(){
            this.new_cover = []
            this.base_list = []
        },
        // 更换头像
        change_avatar(){
            this.$message({
                message:"正在更换头像"
            })
            this.request_id += 1;
            var data = {
                avatar: true,
                avatar_src: this.base_list[0],
            }
            var method = 'POST'
            var url = '/api/user'
            const my_this = this
            var get_response = function () { 
                my_this.$message({
                    message:'头像更换成功',
                    type:'success'
                    })
                my_this.base_list = []
                my_this.new_cover = []
                // 让父组件更新state，并且不显示更新提示
                my_this.update(1)
            }
            request_json(data,url,method,get_response)
        },
        // 更新用户信息
        update_user_info(){
            var data = {
                id:this.state.user_id
            }
            this.user_info.state = null
            var method = 'GET'
            var url = '/api/user'
            const my_this = this
            var get_response = function (res) { 
                my_this.user_info = res.data.user_info
            }
            request_json(data,url,method,get_response)
        },
  },
  computed:{
        get_random_src(){
            return this.state.avatar+"?id="+String(this.request_id)
        },
        login_datetime:function () {
			var d = new Date()
			var a = this.user_info.login_time
            if (a < 1000000000000)
			{
				a *= 1000
			}
			d.setTime(a)
			return d.toLocaleString()
		},
        register_datetime:function () {
			var d = new Date()
			var a = this.user_info.register_time
            if (a < 1000000000000)
			{
				a *= 1000
			}
			d.setTime(a)
			return d.toLocaleString()
		},
  },
  watch:{
      visible(){
          if(this.visible==true){
              this.update_user_info()
          }
          else{
              this.user_info.state = null
          }
      }
  },
  created(){
      this.update_user_info()
  }
}
</script>

<style scoped>
    .button-modal{
        position: relative;
    }

    .button-modal .button-container{
        position: absolute;
        width:100%;
        height: 80px;
        top: -95px;
    }

    /deep/ .el-avatar img{
        width:100%
    }

    /deep/ .el-upload{
        border: 0px;
        border-radius: 40px;
        box-sizing: border-box;
        width: 80px;
        height: 80px;
        line-height: 80px;
        opacity: 0.8;
    }

    .bottom-box{
        margin-bottom:10px;
        float:left;
    }

    .center-align-box{
        display: flex;
        margin: auto;
        align-self: center;
    }
</style>