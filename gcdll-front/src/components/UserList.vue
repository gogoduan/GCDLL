<template>
    <div id="message_list">
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane label="正常用户" name="first">
                <div class="searchbox" style="margin-bottom:10px;">
                    <span style="margin-right:10px;">搜索用户</span>
                    <el-input v-model="searchmes" style="margin-right:10px; width:300px;">
                    </el-input>
                    <span style="margin-right:10px;">注册时间</span>
                    <el-date-picker v-model="datevalue1" type="datetimerange" range-separator="至"
                        start-placeholder="开始日期" end-placeholder="结束日期" style="margin-right:10px;">
                    </el-date-picker>
                    <el-button @click="search" type="primary">search</el-button>
                </div>
                <div style="margin-bottom: 10px;">
                    <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange" style="margin-right:10px;">
                        全选
                    </el-checkbox>
                    <el-button @click="() => forbiduser(1)" type="warning">
                        封禁</el-button>
                    <el-button @click="() => deleteuser(1)" type="danger">
                        删除</el-button>
                </div>
                <el-table ref="user1" :data="Userlist11" :height="370" :border="true" @sort-change="(x) => sort(x, 1)"
                    tooltip-effect="dark" style="width:100%" @selection-change="handleCheckedChange"
                    :default-sort="{prop: 'comment_cnt', order: 'descending'}">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column prop="username" label="用户名" width="120">
                    </el-table-column>
                    <el-table-column prop="id" label="id" width="120">
                    </el-table-column>
                    <el-table-column prop="time" sortable="true" label="注册时间">
                        <template slot-scope="scope">{{ datetime(scope.row.timestamp) }}</template>
                    </el-table-column>
                    <el-table-column prop="comment_cnt" sortable="custom" label="评论数" width="120">
                    </el-table-column>
                    <el-table-column prop="reported_cnt" label="用户违规次数" sortable="custom" width="120">
                    </el-table-column>
                    <el-table-column label="是否封禁" width="90">
                        <el-tag :type="'success'" disable-transitions>
                            正常
                        </el-tag>
                    </el-table-column>
                </el-table>
                <el-pagination @size-change="handleSizeChange1" @current-change="handlecurrentChange1"
                    :current-page="currentPage1" :page-sizes="[2, 10, 20]" :page-size="pagenum1"
                    layout="total, sizes, prev, pager, next, jumper" :total="total1">
                </el-pagination>
            </el-tab-pane>


            <el-tab-pane label="封禁用户" name="second">
                <div class="searchbox" style="margin-bottom:10px;">
                    <span style="margin-right:10px;">搜索用户</span>
                    <el-input v-model="searchmes2" style="margin-right:10px; width: 300px;">
                    </el-input>
                    <span style="margin-right:10px;">注册时间</span>
                    <el-date-picker v-model="datevalue2" type="datetimerange" range-separator="至"
                        start-placeholder="开始日期" end-placeholder="结束日期" style="margin-right:10px;">
                    </el-date-picker>
                    <el-button @click="search2" type="primary">search</el-button>
                </div>
                <div style="margin-bottom: 10px;">
                    <el-checkbox :indeterminate="isIndeterminate2" v-model="checkAll2" @change="handleCheckAllChange2" style="margin-right:10px;">
                        全选
                    </el-checkbox>
                    <el-button @click="unforbiduser" type="success">
                        解封</el-button>
                    <el-button @click="deleteuser2" type="danger">
                        删除</el-button>
                </div>
                <el-table ref="user2" :data="Userlist21" :height="370" :border="true" @sort-change="(x) => sort(x, 2)"
                    tooltip-effect="dark" style="width:100%" @selection-change="handleCheckedChange2"
                    :default-sort="{prop: 'comment_cnt', order: 'descending'}">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column prop="username" label="用户名" width="120">
                    </el-table-column>
                    <el-table-column prop="id" label="id" width="120">
                    </el-table-column>
                    <el-table-column prop="time" sortable="true" label="注册时间">
                        <template slot-scope="scope">{{ datetime(scope.row.timestamp) }}</template>
                    </el-table-column>
                    <el-table-column prop="comment_cnt" sortable="custom" label="评论数" width="120">
                    </el-table-column>
                    <el-table-column prop="reported_cnt" label="用户违规次数" sortable="custom" width="120">
                    </el-table-column>
                    <el-table-column label="是否封禁" width="90">
                        <el-tag :type="'warning'" disable-transitions>
                            封禁
                        </el-tag>
                    </el-table-column>
                </el-table>
                <el-pagination @size-change="handleSizeChange2" @current-change="handlecurrentChange2"
                    :current-page="currentPage2" :page-sizes="[2, 10, 20]" :page-size="pagenum2"
                    layout="total, sizes, prev, pager, next, jumper" :total="total2">
                </el-pagination>
            </el-tab-pane>


            <el-tab-pane label="删除用户" name="third">
                <div class="searchbox" style="margin-bottom:10px;">
                    <span style="margin-right:10px;">搜索用户</span>
                    <el-input v-model="searchmes3" style="margin-right:10px; width: 300px;">
                    </el-input>
                    <span style="margin-right:10px;">注册时间</span>
                    <el-date-picker v-model="datevalue3" type="datetimerange" range-separator="至"
                        start-placeholder="开始日期" end-placeholder="结束日期" style="margin-right:10px;">
                    </el-date-picker>
                    <el-button @click="search3" type="primary">search</el-button>
                </div>
                <div style="margin-bottom: 10px;">
                    <el-checkbox :indeterminate="isIndeterminate3" v-model="checkAll3" @change="handleCheckAllChange3" style="margin-right:10px;">
                        全选
                    </el-checkbox>
                    <el-button @click="undeleteuser" type="success">
                        恢复</el-button>
                    <el-button @click="deletetoforbiduser" type="warning">
                        恢复为禁言</el-button>
                </div>
                <el-table ref="user3" :data="Userlist31" :height="370" :border="true" @sort-change="(x) => sort(x, 3)"
                    tooltip-effect="dark" style="width:100%" @selection-change="handleCheckedChange3"
                    :default-sort="{prop: 'comment_cnt', order: 'descending'}">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column prop="username" label="用户名" width="120">
                    </el-table-column>
                    <el-table-column prop="id" label="id" width="120">
                    </el-table-column>
                    <el-table-column prop="time" sortable="true" label="注册时间">
                        <template slot-scope="scope">{{ datetime(scope.row.timestamp) }}</template>
                    </el-table-column>
                    <el-table-column prop="comment_cnt" sortable="custom" label="评论数" width="120">
                    </el-table-column>
                    <el-table-column prop="reported_cnt" label="用户违规次数" sortable="custom" width="120">
                    </el-table-column>
                    <el-table-column label="是否封禁" width="90">
                        <el-tag :type="'danger'" disable-transitions>
                            删除
                        </el-tag>
                    </el-table-column>
                </el-table>
                <el-pagination @size-change="handleSizeChange3" @current-change="handlecurrentChange3"
                    :current-page="currentPage3" :page-sizes="[2, 10, 20]" :page-size="pagenum3"
                    layout="total, sizes, prev, pager, next, jumper" :total="total3">
                </el-pagination>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
<script>
    // import UserBlock from "@/components/UserBlock"
    import {
        request_json
    } from "@/utils/communication"
    export default {
        name: "UserList",
        components: {
            // UserBlock
        },
        data() {
            return {
                Userlist11: [],
                Userlist21: [],
                Userlist31: [],
                searchmes: "",
                searchmes2: "",
                searchmes3: "",
                checkAll: false,
                checkAll2: false,
                checkAll3: false,
                checklist: [],
                checkedUsers: [],
                checkedUsers2: [],
                checkedUsers3: [],
                isIndeterminate: true,
                isIndeterminate2: true,
                isIndeterminate3: true,
                activeName: "first",
                currentPage1: 1,
                currentPage2: 1,
                currentPage3: 1,
                pagenum1: 10,
                pagenum2: 10,
                pagenum3: 10,
                total1: 100000,
                total2: 100000,
                total3: 100000,
                sortprop1: "time",
                sortprop2: "time",
                sortprop3: "time",
                sortorder1: "descending",
                sortorder2: "descending",
                sortorder3: "descending",
                datevalue1: [],
                datevalue2: [],
                datevalue3: [],
                filters1: [],
                filters2: [],
                filters3: [],
                // Userlist1: [],
                // Userlist2: [],
                // Userlist3: [],
            }
        },
        props: {},
        methods: {
            handleClick(tab, event) {
                console.log(tab, event);
                // this.Userlist11 = this.Userlist1;
                // this.Userlist21 = this.Userlist2;
                // this.Userlist31 = this.Userlist3;
            },
            refresh() {
                this.sort({"column": null, "prop": this.sortprop1, "order": this.sortorder1}, 1)
                this.sort({"column": null, "prop": this.sortprop1, "order": this.sortorder2}, 2)
                this.sort({"column": null, "prop": this.sortprop1, "order": this.sortorder3}, 3)
            },
            handleCheckAllChange(val) {
                this.checkedUsers = val ? this.Userlist11 : [];
                this.isIndeterminate = false;
            },
            handleCheckedChange(value) {
                this.checkedUsers = value;
                let checkedCount = value.length;
                this.checkAll = checkedCount === this.Userlist11.length;
                this.isIndeterminate = checkedCount > 0 && checkedCount < this.Userlist11.length;
            },
            handleCheckAllChange2(val) {
                this.checkedUsers2 = val ? this.Userlist21 : [];
                this.isIndeterminate2 = false;
            },
            handleCheckedChange2(value) {
                this.checkedUsers2 = value;
                let checkedCount = value.length;
                this.checkAll2 = checkedCount === this.Userlist21.length;
                this.isIndeterminate2 = checkedCount > 0 && checkedCount < this.Userlist21.length;
            },
            handleCheckAllChange3(val) {
                this.checkedUsers3 = val ? this.Userlist31 : [];
                this.isIndeterminate3 = false;
            },
            handleCheckedChange3(value) {
                this.checkedUsers3 = value;
                let checkedCount = value.length;
                this.checkAll3 = checkedCount === this.Userlist31.length;
                this.isIndeterminate3 = checkedCount > 0 && checkedCount < this.Userlist31.length;
            },

            handleSizeChange1(val) {
                console.log(`每页 ${val} 条`);
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = val;
                this.pagenum1 = val;
                dat['order_name'] = this.sortprop1;
                if (this.sortorder1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 1));
            },
            handlecurrentChange1(val) {
                console.log(`当前页: ${val}`);
                var dat = {};
                this.currentPage1 = val;
                dat['type'] = "user";
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                dat['order_name'] = this.sortprop1;
                if (this.sortorder1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 1));
            },
            handleSizeChange2(val) {
                console.log(`每页 ${val} 条`);
                this.pagenum2 = val;
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                dat['order_name'] = this.sortprop2;
                if (this.sortorder2 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 2));
            },
            handlecurrentChange2(val) {
                console.log(`当前页: ${val}`);
                this.currentPage2 = val;
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                dat['order_name'] = this.sortprop2;
                if (this.sortorder2 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 2));
            },
            handleSizeChange3(val) {
                console.log(`每页 ${val} 条`);
                this.pagenum3 = val;
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                dat['order_name'] = this.sortprop3;
                if (this.sortorder1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 3));
            },
            handlecurrentChange3(val) {
                console.log(`当前页: ${val}`);
                this.currentPage3 = val;
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                dat['order_name'] = this.sortprop3;
                if (this.sortorder1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 3));
            },



            forbiduser() {
                var sd = {};
                var request = "forbiduser";
                sd['wanted'] = request;
                if (this.checkedUsers.length == 0) {
                    alert("请选择用户！");
                    return;
                }
                this.checkedUsers.forEach(item => {
                    this.checklist.push(item.id);
                })
                sd['data'] = this.checklist;
                const myThis = this;
                request_json(sd, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                    myThis.$message({
                        message:"成功封禁",
                        type:"success",
                    })
                });
            },
            unforbiduser() {
                var sd = {};
                var request = "unforbiduser";
                sd['wanted'] = request;
                if (this.checkedUsers2.length == 0) {
                    alert("请选择用户！");
                    return;
                }
                this.checkedUsers2.forEach(item => {
                    this.checklist.push(item.id);
                })
                sd['data'] = this.checklist;
                const myThis = this;
                request_json(sd, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                    myThis.$message({
                        message:"成功解除封禁",
                        type:"success",
                    })
                });
            },
            undeleteuser() {
                var sd = {};
                var request = "undeleteuser";
                sd['wanted'] = request;
                if (this.checkedUsers3.length == 0) {
                    alert("请选择用户！");
                    return;
                }
                this.checkedUsers3.forEach(item => {
                    this.checklist.push(item.id);
                })
                sd['data'] = this.checklist;
                const myThis = this;
                request_json(sd, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                    myThis.$message({
                        message:"成功解除删除",
                        type:"success",
                    })
                });
            },
            deletetoforbiduser() {
                var sd = {};
                var request = "deletetoforbid";
                sd['wanted'] = request;
                if (this.checkedUsers3.length == 0) {
                    alert("请选择用户！");
                    return;
                }
                this.checkedUsers3.forEach(item => {
                    this.checklist.push(item.id);
                })
                sd['data'] = this.checklist;
                const myThis = this;
                request_json(sd, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                    myThis.$message({
                        message:"成功封禁",
                        type:"success",
                    })
                });
            },
            deleteuser() {
                var sd = {};
                var requeste = "deleteuser";
                sd['wanted'] = requeste;
                if (this.checkedUsers.length == 0) {
                    alert("请选择用户！");
                    return;
                }
                this.checkedUsers.forEach(item => {
                    this.checklist.push(item.id);
                })
                sd['data'] = this.checklist;
                const myThis = this;
                request_json(sd, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                    myThis.$message({
                        message:"成功删除",
                        type:"success",
                    })
                });
            },
            deleteuser2() {
                var sd = {};
                var requeste = "deleteuser";
                sd['wanted'] = requeste;
                if (this.checkedUsers2.length == 0) {
                    alert("请选择用户！");
                    return;
                }
                this.checkedUsers2.forEach(item => {
                    this.checklist.push(item.id);
                })
                sd['data'] = this.checklist;
                const myThis = this;
                request_json(sd, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                    myThis.$message({
                        message:"成功删除",
                        type:"success",
                    })
                });
            },
            search() {
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "visited";
                dat['negative'] = false;
                var ts = [];
                var qk = {};
                qk['name'] = this.searchmes.split(" ");
                ts.push(qk);
                qk = {};
                if (this.datevalue1 && this.datevalue1.length != 0) {
                    var min_timestamp = this.datevalue1[0].getTime();
                    var max_timestamp = this.datevalue1[1].getTime();
                    qk['min_timestamp'] = min_timestamp;
                    qk['max_timestamp'] = max_timestamp;
                    ts.push(qk);
                    qk = {};
                }
                dat['filters'] = ts;
                this.filters1 = ts;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                dat['order_name'] = this.sortprop1;
                if (this.sortorder1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 1));
            },
            search2() {
                var dat = {};
                dat['type'] = "user";
                dat['group'] = "banned";
                dat['negative'] = false;
                var ts = [];
                var qk = {};
                qk['name'] = this.searchmes2.split(" ");
                ts.push(qk);
                qk = {};
                if (this.datevalue2 && this.datevalue2.length != 0) {
                    var min_timestamp = this.datevalue2[0].getTime();
                    var max_timestamp = this.datevalue2[1].getTime();
                    qk['min_timestamp'] = min_timestamp;
                    qk['max_timestamp'] = max_timestamp;
                    ts.push(qk);
                    qk = {};
                }
                dat['filters'] = ts;
                this.filters2 = ts;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                dat['order_name'] = this.sortprop2;
                if (this.sortorder2 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 2));
            },
            search3() {
                var dat = {};
                dat['type'] = 'user';
                dat['group'] = "deleted";
                dat['negative'] = false;
                var ts = [];
                var qk = {};
                qk['name'] = this.searchmes3.split(" ");
                ts.push(qk);
                qk = {};
                if (this.datevalue3 && this.datevalue3.length != 0) {
                    var min_timestamp = this.datevalue3[0].getTime();
                    var max_timestamp = this.datevalue3[1].getTime();
                    qk['min_timestamp'] = min_timestamp;
                    qk['max_timestamp'] = max_timestamp;
                    ts.push(qk);
                    qk = {};
                }
                dat['filters'] = ts;
                this.filters1 = ts;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                dat['order_name'] = this.sortprop3;
                if (this.sortorder3 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', (x) => this.getmes(x, 3));
            },


            sort({col, prop, order}, i) {
                var send = {};
                col;
                const groups = ["visited", "banned", "deleted"];
                send['group'] = groups[i - 1];
                send['type'] = "user";
                const pages = [this.currentPage1, this.currentPage2, this.currentPage3];
                send['page'] = pages[i - 1];
                const amounts = [this.pagenum1, this.pagenum2, this.pagenum3];
                send['amount'] = amounts[i - 1];
                send['order_name'] = prop;
                send['order_method'] = (order == 'ascending');
                switch(i) {
                    case 1:
                        this.sortprop1 = prop;
                        this.sortorder1 = order;
                        break;
                    case 2:
                        this.sortprop2 = prop;
                        this.sortorder2 = order;
                        break;
                    case 3:
                        this.sortprop3 = prop;
                        this.sortorder3 = order;
                        break;
                }
                send['filters'] = [];
                request_json(send, '/api/search', 'POST', (dat) => this.getmes(dat, i));
            },

            getmes(dat, i) {
                let userlist = null;
                switch(i) {
                    case 1:
                        this.Userlist11 = dat['data'].mes;
                        userlist = this.Userlist11;
                        this.total1 = Number(dat['data'].total);
                        break;
                    case 2:
                        this.Userlist21 = dat['data'].mes;
                        userlist = this.Userlist21;
                        this.total2 = Number(dat['data'].total);
                        break;
                    case 3:
                        this.Userlist31 = dat['data'].mes;
                        userlist = this.Userlist31;
                        this.total3 = Number(dat['data'].total);
                        break;
                }
                userlist.forEach((item) => {
                    item.timestamp = Number(item.timestamp);
                    item.id = Number(item.id);
                    item.comment_cnt = Number(item.comment_cnt);
                    item.reported_cnt = Number(item.reported_cnt);
                })
            },
            sortbytime() {
                var dat = {};
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                this.sortprop1 = 'time';
                this.sortorder1 = "ascending";
                dat['order_name'] = 'time';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbytime_down() {
                var dat = {};
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                this.sortprop1 = 'time';
                this.sortorder1 = "descending";
                dat['order_name'] = 'time';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbyid() {
                var dat = {};
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                this.sortprop1 = 'comment';
                this.sortorder1 = "ascending";
                dat['order_name'] = 'comment';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbyid_down() {
                var dat = {};
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                this.sortprop1 = 'comment';
                this.sortorder1 = "descending";
                dat['order_name'] = 'comment';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbymoral() {
                var dat = {};
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                this.sortprop1 = 'user_report';
                this.sortorder1 = "ascending";
                dat['order_name'] = 'user_report';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbymoral_down() {
                var dat = {};
                dat['group'] = "visited";
                dat['filters'] = this.filters1;
                dat['page'] = this.currentPage1;
                dat['amount'] = this.pagenum1;
                this.sortprop1 = 'user_report';
                this.sortorder1 = "descending";
                dat['order_name'] = 'user_report';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbytime2() {
                var dat = {};
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                this.sortprop2 = 'time';
                this.sortorder2 = "ascending";
                dat['order_name'] = 'time';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbytime2_down() {
                var dat = {};
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                this.sortprop2 = 'time';
                this.sortorder2 = "descending";
                dat['order_name'] = 'time';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbyid2() {
                var dat = {};
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                this.sortprop2 = 'comment';
                this.sortorder2 = "ascending";
                dat['order_name'] = 'comment';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbyid2_down() {
                var dat = {};
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                this.sortprop2 = 'comment';
                this.sortorder2 = "descending";
                dat['order_name'] = 'comment';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbymoral2() {
                var dat = {};
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                this.sortprop2 = 'user_report';
                this.sortorder2 = "ascending";
                dat['order_name'] = 'user_report';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbymoral2_down() {
                var dat = {};
                dat['group'] = "banned";
                dat['filters'] = this.filters2;
                dat['page'] = this.currentPage2;
                dat['amount'] = this.pagenum2;
                this.sortprop2 = 'user_report';
                this.sortorder2 = "descending";
                dat['order_name'] = 'user_report';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbytime3() {
                var dat = {};
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                this.sortprop3 = 'time';
                this.sortorder3 = "ascending";
                dat['order_name'] = 'time';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbytime3_down() {
                var dat = {};
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                this.sortprop3 = 'time';
                this.sortorder3 = "descending";
                dat['order_name'] = 'time';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbyid3() {
                var dat = {};
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                this.sortprop3 = 'comment';
                this.sortorder3 = "ascending";
                dat['order_name'] = 'comment';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbyid3_down() {
                var dat = {};
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                this.sortprop3 = 'comment';
                this.sortorder3 = "descending";
                dat['order_name'] = 'comment';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbymoral3() {
                var dat = {};
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                this.sortprop3 = 'user_report';
                this.sortorder3 = "ascending";
                dat['order_name'] = 'user_report';
                dat['ordet_method'] = true;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            sortbymoral3_down() {
                var dat = {};
                dat['group'] = "deleted";
                dat['filters'] = this.filters3;
                dat['page'] = this.currentPage3;
                dat['amount'] = this.pagenum3;
                this.sortprop3 = 'user_report';
                this.sortorder3 = "descending";
                dat['order_name'] = 'user_report';
                dat['ordet_method'] = false;
                const myThis = this;
                request_json(dat, '/api/admintourist', 'POST', ()=>{
                    myThis.checklist = [];
                    myThis.checkedUsers = [];
                    myThis.checkedUsers2 = [];
                    myThis.checkedUsers3 = [];
                    myThis.refresh();
                });
            },
            datetime(timestamp) {
                var d = new Date();
                var a = timestamp;
                if (a < 1e12) {
                    a = a * 1000;
                }
                d.setTime(a);
                return d.toLocaleString();
            },
        },
        created() {
            this.sort({"column":null, "prop":'time', "order": "ascending"}, 1);
            this.sort({"column":null, "prop":'time', "order": "ascending"}, 2);
            this.sort({"column":null, "prop":'time', "order": "ascending"}, 3);
        },
    }
</script>
<style>
    .searchbox {
        width: 100%;
    }

    .searchblock {
        margin: 2px;
    }
</style>