<template>
    <div class="user">
        <el-card shadow="never" class="box">
            <div class="message">
                <el-popover placement="right" width="540" trigger="hover">
                    <div class="message" style="width:max-content;">
                        <el-avatar slot="reference" :size="80" :src="avasrc" shape="square" fit="fill"
                            icon="el-icon-user">
                        </el-avatar>
                        <div>
                            <h3 style="margin:auto; width:max-content;">{{name}}</h3>
                        </div>
                        <div>
                            <h4 style="margin:auto; width:max-content;">用户id: {{id}}</h4>
                        </div>
                    </div>
                    <div class="message">
                    </div>
                    <div class="message">
                        <!-- <div>
                            <h3>邮箱：{{mailbox}};</h3>
                        </div> -->
                        <!-- <div>
                            <a>用户简介:{{intro}};</a></div> -->
                        <el-form inline>
                            <el-form-item>
                            <a>注册时间：{{this.datetime}};</a>
                            </el-form-item>
                            <el-form-item>
                            <a>评论数：{{commentnum}};</a>
                            </el-form-item>
                            <el-form-item>
                            <a>被举报次数：{{badtime}};</a>
                            </el-form-item>
                        </el-form>
                        <!-- <div>
                            <a>注册时间:{{this.datetime}};</a>
                            <a>评论数:{{commentnum}};</a>
                            <a>被举报次数:{{badtime}};</a>
                        </div> -->
                    </div>
                    <el-avatar class="mes1" slot="reference" :size="50" :src="avasrc" shape="square" fit="fill"
                        icon="el-icon-user">
                    </el-avatar>
                </el-popover>
            </div>
            <div class="mes2">
                <div>
                    <h2>{{name}}</h2>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
    export default {
        name: "UserBlock",
        props: {
            avasrc: {
                type: String,
                default: () =>
                    "https://img1.baidu.com/it/u=3009859673,2327944616&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",
            },
            name: {
                type: String,
                default: () => "name5",
            },
            intro: {
                type: String,
                default: () => "intro5",
            },
            commentnum: {
                type: Number,
                default: () => 0,
            },
            id: {
                type: Number,
                default: () => "id_12345",
            },
            timestamp: {
                type: Number,
                default: () => 3706727999,
            },
            mailbox: {
                type: String,
                default: () => "1@163.com",
            },
            badtime: {
                type: Number,
                default: () => 1,
            },
        },
        data() {
            return {}
        },
        methods: {},
        computed: {
            datetime: function () {
                var d = new Date();
                var a = this.timestamp;
                if (this.timestamp < 1e12) {
                    a = this.timestamp * 1000;
                }
                d.setTime(a);
                return d.toLocaleString();
            },
        }
    }
</script>

<style scoped>
.user{
width:700px;
height:70px;
}
.message{
float:left;
}
.box{
height:60px;
}
.mes1{
position:absolute;
top:20px;
left:25px;
}
.mes2{
position:absolute;
top:0px;
left:100px;
}
</style>