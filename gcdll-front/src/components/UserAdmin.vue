<template>
    <div>
        <div id="new-users">
            <div id="new-header" class="header">
                <h2 style="width: 100px; box-sizing:border-box; float: left; margin: 0">新用户</h2>
            </div>
            <div id="new-list" class="list">
                <el-card v-for="user in new_user" :key="user" shadow="hover">
                    {{ user }}
                </el-card>                
            </div>
        </div>
        <div id="old-users">
            <div id="old-header" class="header">
                <h2 style="width: 100px; box-sizing:border-box; float: left; margin: 0">老用户</h2>
            </div>
            <div id="old-list" class="list">
                <el-card v-for="user in old_user" :key="user" shadow="hover">
                    {{ user }}
                </el-card>                
            </div>

        </div>
    </div>
</template>
<script>
export default {
    name: "UserAdmin",
    props: {
        new_user: {
            type: Array,
            default: () => [
                'Tom',
                'Jerry'
            ]
        },
        old_user: {
            type: Array,
            default: () => [
                'Tom',
                'Jerry',
                'Beth',
                'Alice',
                'Sam'
            ]
        }
    }
}
</script>
<style>
    #new-users {
        /* height: 150px; */
    }
    #old-users {
        height: 350px;
    }
    .list {
        overflow: auto;
        height: 150px;
    }
    .header {
        border-bottom: solid;
        height: 60px;
    }
</style>