<template>
    <div class="user-comment-center">

    </div>
</template>

<script>
// import {request_json} from '@/utils/communication.js'
export default {
  name: 'UserCommentCenter',
  components: {
      
  },
  props:{
      state:{
          type:Object,
          required:true,
      }
  },
  data(){
    return{
    }
  },
  methods:{

  },
  computed:{
  },
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
</style>