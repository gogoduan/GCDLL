<template>
    <div class="order-manage-board">
        <draggable class="flex-container" v-model="image_list" :style="'height:'+height"
        forceFallback="true" :animation="500"
        draggable=".item">
                <exhibit-block class="item" v-for="image in image_list" :key="image.id"
                    state="drag"
                    :type="0" :id="image.id" :image_src="image.img_src" 
                    :introduction="image.introduction" 
                    :name="image.name"  :tag_list="image.tag_list"
                    :likes="image.likes" :comments="image.comments" 
                    :timestamp="image.timestamp">
                </exhibit-block>
        </draggable>
        <el-row style="width:100%; margin-top:10px;">
            <el-button type="normal" @click="dialog_visible=true">预览</el-button>
            <el-button type="success" @click="change">确认</el-button>
            <el-button type="warning" @click="withdraw()">撤销</el-button>
        </el-row>
        <el-dialog title="预览" :visible.sync="dialog_visible" width="80%" append-to-body
        top="20px">
            <div class="example-container">
                <exhibit-board :exhibit_style="exhibit_style" :type="0"
                 :image_list="image_list" :state="my_state"/>
            </div>
        </el-dialog>
    </div>
</template>

<script>
// import {request_json} from '@/utils/communication.js'
import Draggable from 'vuedraggable'
import ExhibitBlock from './ExhibitBlock.vue'
import ExhibitBoard from './ExhibitBoard.vue'
export default {
  name: 'OrderManageBoard',
  components: {
      Draggable,
      ExhibitBlock,
      ExhibitBoard
  },
  props:{
      height:{
          type:String,
          default:'400px'
      },
      exhibit_style:{
          type:String,
          required:true
      },
      myArray:{
          type:Array,
          required:true,
      },
      resolve:{
          type:Function,
          required:true,
      },

  },
  data(){
    return{
        dialog_visible: false,
        image_list:[],
    }
  },
  methods:{
      change(){
          this.resolve(this.image_list)
      },
      withdraw(){
          this.image_list = this.myArray
      }
  },
  computed:{
      my_state(){
            if(this.exhibit_style=='rank' || this.exhibit_style=='cross')
                return 'auto_photo'
            return 'photo'
        }
  },
  created(){
      this.image_list = this.myArray
  }
}
</script>

<style scoped>
    .bottom-box{
        margin-bottom:10px;
        float:left;
    }

    .center-align-box{
        display: flex;
        margin: auto;
        align-self: center;
    }

    .flex-container{
        overflow-y:auto;
        display: -webkit-flex;
        display: flex;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
        -webkit-align-content: space-between;
        align-content: space-between;
    }

    .example-container{
        overflow: auto;
        height:500px;
    }
</style>