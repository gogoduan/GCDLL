<template>
    <div>
        <h2>评论管理</h2>
        <el-tabs v-model="activeName" @tab-click="hdClick">
            <el-tab-pane label="照片评论" name="first">
                <div>
                    <div style="margin-bottom:10px;">
                        <span style="margin-right: 30px;">评论范围</span>
                        <!-- <el-select v-model="range1" placeholder="评论范围">
                            <el-option v-for="item in rangeoptions1" :key="item.value" :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select> -->
                        <el-radio v-model="range1" v-for="item in rangeoptions1" :key="item.value" :label="item.value">{{ item.label }}
                        </el-radio>
                        <el-checkbox v-model="searchuser1" label="用户" style="margin-right:10px;">
                        </el-checkbox>
                        <el-input v-model="searcher" class="search" placeholder="用户名" style="margin-right: 30px;"></el-input>
                        <el-checkbox v-model="searchimg" label="图片" style="margin-right:10px;">
                        </el-checkbox>
                        <el-input v-model="imgs" class="search" placeholder="图片" style="margin-right:30px;"></el-input>
                    </div>
                    <div style="margin-bottom:10px;">
                        <span style="margin-right:10px;">评论内容
                        </span>
                        <el-input v-model="searchcomment" class="search2" placeholder="评论" style="margin-right:10px;"></el-input>
                        <span style="margin-right:10px;">评论发表时间
                        </span>
                        <el-date-picker v-model="datevalue1" type="datetimerange" range-separator="至"
                            start-placeholder="开始日期" end-placeholder="结束日期">
                        </el-date-picker>
                        <el-button style="margin-top:10px;" @click="searchimage" type="danger">搜索</el-button>
                    </div>
                    <div style="margin-bottom:10px;">
                        <el-button type="danger" @click="managedelete1">集体删除</el-button>
                        <el-button type="warning" @click="managebnd1">集体封禁</el-button>
                        <el-button type="success" @click="managealive1">集体放过</el-button>
                    </div>
                </div>
                <el-table ref="multipleTable" :data="tableData" :height="370" :border="true" @sort-change="imgsort"
                    tooltip-effect="dark" style="width:100%" @selection-change="handleSelectionChange"
                    :default-sort="{prop: 'time', order: 'descending'}">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column type="expand" label="">
                        <template slot-scope="props">
                            <el-form label-position="left" inline class="demo-table-expand">
                                <el-form-item label="发送时间">
                                    <span>{{ datetime(props.row.time) }}</span>
                                </el-form-item>
                                <el-form-item label="用户名">
                                    <span>{{ props.row.user.username }}</span>
                                </el-form-item>
                                <el-form-item label="评论">
                                    <span><a>{{ props.row.comment }}</a></span>
                                </el-form-item>
                                <el-form-item label="违规次数">
                                    <span>{{ props.row.user.user_report }}</span>
                                </el-form-item>
                                <el-form-item label="图片名字">
                                    <span>{{ props.row.imgname }}</span>
                                </el-form-item>
                                <el-form-item label="图片编号">
                                    <span>{{ props.row.imgid }}</span>
                                </el-form-item>
                                <el-form-item label="图片">
                                    <span><img :src="props.row.imgsrc" width="200px" height="200px"></span>
                                </el-form-item>
                            </el-form>
                        </template>
                    </el-table-column>
                    <el-table-column sortable="custom" prop="time" label="日期" width="120">
                        <template slot-scope="scope">{{ datetime(scope.row.time) }}</template>
                    </el-table-column>
                    <el-table-column prop="user.username" label="用户名" width="120">
                    </el-table-column>
                    <el-table-column prop="user_report" label="用户违规次数" sortable="custom" width="120">
                    </el-table-column>
                    <el-table-column prop="comment_report" sortable="custom" label="评论违规次数" width="120">
                    </el-table-column>
                    <el-table-column prop="comment" label="内容">
                    </el-table-column>
                    <el-table-column prop="banned" label="是否封禁" width="90">
                        <template slot-scope="scope">
                            <el-tag :type="scope.row.banned === true ? 'danger' : 'success'" disable-transitions>
                                {{scope.row.banned === true ? '封禁' : '正常'}}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column fixed="right" label="操作" width="100">
                        <template slot-scope="scope" style="margin:0">
                            <el-button @click="dlt(scope.row)" type="danger" icon="el-icon-delete-solid" size="small">删除
                            </el-button>
                            <el-button @click="bnd(scope.row)" type="warning" icon="el-icon-warning" size="small">封禁
                            </el-button>
                            <el-button @click="alive(scope.row)" type="success" icon="el-icon-success" size="small">放过
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                    :current-page="currentPage4" :page-sizes="[10,20,50,100,200,400]" :page-size="k"
                    layout="total, sizes, prev, pager, next, jumper" :total="totalnum">
                </el-pagination>
            </el-tab-pane>
            <el-tab-pane label="展览评论" name="second">
                <div>
                    <div style="margin-bottom:10px;">
                        <span style="margin-right:30px;">评论范围</span>
                        <el-radio v-model="range2" v-for="item in rangeoptions2" :key="item.value" :label="item.value">{{ item.label }}
                        </el-radio>
                        <el-checkbox v-model="searchuser2" label="用户" style="margin-right:10px;">
                        </el-checkbox>
                        <el-input v-model="searcher2" class="search" placeholder="用户名" style="margin-right:30px;"></el-input>
                        <el-checkbox v-model="searchgal" label="展览" style="margin-right:10px;">
                        </el-checkbox>
                        <el-input v-model="gals" class="search" placeholder="展览" style="margin-right:30px;"></el-input>
                    </div>
                    <div style="margin-bottom:10px;">
                        <span style="margin-right:10px;">评论内容
                        </span>
                        <el-input v-model="searchcomment2" class="search2" placeholder="评论" style="margin-right:10px;"></el-input>
                        <span style="margin-right:10px;">评论发表时间
                        </span>
                        <el-date-picker v-model="datevalue2" type="datetimerange" range-separator="至"
                            start-placeholder="开始日期" end-placeholder="结束日期">
                        </el-date-picker>
                        <el-button style="margin-top:10px" @click="searchgallery" type="danger">搜索</el-button>
                    </div>
                    <div style="margin-bottom:10px;">
                        <el-button type="danger" @click="managedelete2">集体删除</el-button>
                        <el-button type="warning" @click="managebnd2">集体封禁</el-button>
                        <el-button type="success" @click="managealive2">集体放过</el-button>
                    </div>
                </div>
                <el-table ref="multipleTable2" :data="tableData2" :height="370" :border="true" @sort-change="galsort"
                    tooltip-effect="dark" style="width:100%" @selection-change="handleSelectionChange2"
                    :default-sort="{prop: 'time', order: 'descending'}">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column type="expand" label="">
                        <template slot-scope="props">
                            <el-form label-position="left" inline class="demo-table-expand">
                                <el-form-item label="发送时间">
                                    <span>{{ datetime(props.row.time) }}</span>
                                </el-form-item>
                                <el-form-item label="用户名">
                                    <span>{{ props.row.user.username }}</span>
                                </el-form-item>
                                <el-form-item label="评论">
                                    <span><a>{{ props.row.comment }}</a></span>
                                </el-form-item>
                                <el-form-item label="违规次数">
                                    <span>{{ props.row.user.user_report }}</span>
                                </el-form-item>
                                <el-form-item label="展览编号">
                                    <span>{{ props.row.imgid }}</span>
                                </el-form-item>
                                <el-form-item label="展览名称">
                                    <span>{{ props.row.imgname }}</span>
                                </el-form-item>
                                <el-form-item label="展览封面">
                                    <span><img :src="props.row.imgsrc" height="200px" width="200px"></span>
                                </el-form-item>
                            </el-form>
                        </template>
                    </el-table-column>
                    <el-table-column sortable="custom" prop="time" label="日期" width="120">
                        <template slot-scope="scope">{{ datetime(scope.row.time) }}</template>
                    </el-table-column>
                    <el-table-column prop="user.username" label="用户名" width="120">
                    </el-table-column>
                    <el-table-column prop="user_report" label="用户违规次数" sortable="custom" width="120">
                    </el-table-column>
                    <el-table-column prop="comment_report" sortable="custom" label="评论违规次数" width="120">
                    </el-table-column>
                    <el-table-column prop="comment" label="内容">
                    </el-table-column>
                    <el-table-column prop="ifbanned" label="是否封禁" width="90">
                        <template slot-scope="scope">
                            <el-tag :type="scope.row.banned === true ? 'danger' : 'success'" disable-transitions>
                                {{scope.row.banned === true ? '封禁' : '正常'}}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column fixed="right" label="操作" width="100">
                        <template slot-scope="scope">
                            <el-button @click="dlt2(scope.row)" type="danger" icon="el-icon-delete-solid" size="small">
                                删除</el-button>
                            <el-button @click="bnd2(scope.row)" type="warning" icon="el-icon-warning" size="small">封禁
                            </el-button>
                            <el-button @click="alive2(scope.row)" type="success" icon="el-icon-success" size="small">放过
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination @size-change="handleSizeChange2" @current-change="handleCurrentChange2"
                    :current-page="currentPage42" :page-sizes="[10,20,50,100,200,400]" :page-size="k2"
                    layout="total, sizes, prev, pager, next, jumper" :total="totalnum2">
                </el-pagination>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
<script>
    import {
        request_json
    } from '@/utils/communication.js'
    export default {
        name: "Dealcomment",
        data() {
            return {
                tableData2: [],
                tableData: [],
                range1: 'all',
                rangeoptions1: [{
                        value: 'banned',
                        label: '被封禁的评论',
                    },
                    {
                        value: 'unbanned',
                        label: '未封禁的评论',
                    },
                    {
                        value: 'all',
                        label: '所有的评论',
                    }
                ],
                range2: 'all',
                rangeoptions2: [{
                        value: 'banned',
                        label: '被封禁的评论',
                    },
                    {
                        value: 'unbanned',
                        label: '未封禁的评论',
                    },
                    {
                        value: 'all',
                        label: '所有的评论',
                    }
                ],
                multipleSelection: [],
                multipleSelection2: [],
                filters1: [],
                filters2: [],
                searcher: '',
                searcher2: '',
                imgs: '',
                gals: '',
                currentPage4: 1,
                currentPage42: 1,
                totalnum: 380078,
                totalnum2: 123999,
                searchcomment: '',
                searchcomment2: '',
                k: 50,
                k2: 50,
                activeName: 'first',
                searchuser1: false,
                searchimg: false,
                searchuser2: false,
                searchgal: false,
                order1: "descending",
                order2: "descending",
                orderprop1: "time",
                orderprop2: "time",
                datevalue1: [],
                datevalue2: [],
            }
        },
        methods: {
            hdClick(tab, event) {
                console.log(tab, event);
            },
            findtag(value, row) {
                return row.banned === value;
            },
            defaultsearch() {
                const that = this;
                var dat = {};
                dat['type'] = "photo_comment";
                dat['filters'] = this.filters1;
                dat['order_name'] = this.orderprop1;
                dat['amount'] = this.k;
                dat['page'] = this.currentPage4;
                if (this.order1 == "descending")
                dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', that.getmes);
                that.$message({
                    message:"成功操作",
                    type:"success",
                })
            },
            defaultsearch2() {
              const that = this;
                var dat = {};
                dat['type'] = "gallery_comment";
                dat['filters'] = this.filters2;
                dat['order_name'] = this.orderprop2;
                dat['amount'] = this.k2;
                dat['page'] = this.currentPage42;
                if (this.order2 == "descending")
                dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', that.getmes2);
                that.$message({
                    message:"成功操作",
                    type:"success",
                })
            },
            dlt(row) {
              const that = this;
                var d = {};
                d['operation'] = "delete";
                d['type'] = "photo_comment";
                var lst = [];
                lst.push(row.commentid);
                d['list'] = lst;
                request_json(d, '/api/admincomment', 'POST',that.defaultsearch);
            },
            alive(row) {
              const that = this;
                var d = {};
                d['operation'] = "alive";
                d['type'] = "photo_comment";
                var lst = [];
                lst.push(row.commentid);
                d['list'] = lst;
                request_json(d, '/api/admincomment', 'POST',that.defaultsearch);
            },
            bnd(row) {
            const that = this;
                var d = {};
                d['operation'] = "forbid";
                d['type'] = "photo_comment";
                var lst = [];
                lst.push(row.commentid);
                d['list'] = lst;
                request_json(d, '/api/admincomment', 'POST',that.defaultsearch);
            },
            bnd2(row) {
            const that = this;
                var d = {};
                d['operation'] = "forbid";
                d['type'] = "gallery_comment";
                var lst = [];
                lst.push(row.commentid);
                d['list'] = lst;
                request_json(d, '/api/admincomment', 'POST',that.defaultsearch2);
            },
            dlt2(row) {
            const that = this;
                var d = {};
                d['operation'] = "delete";
                d['type'] = "gallery_comment";
                var lst = [];
                lst.push(row.commentid);
                d['list'] = lst;
                request_json(d, '/api/admincomment', 'POST',that.defaultsearch2);
            },
            alive2(row) {
            const that = this;
                var d = {};
                d['operation'] = "alive";
                d['type'] = "gallery_comment";
                var lst = [];
                lst.push(row.commentid);
                d['list'] = lst;
                request_json(d, '/api/admincomment', 'POST',that.defaultsearch2);
            },
            getmes(resolve) {
                this.tableData = resolve['data'].mes;
                this.tableData.forEach(item => {
                    item.time = Number(item.time);
                    item.user.timestamp = Number(item.user.timestamp);
                    item.user.comment_cnt = Number(item.user.comment_cnt);
                    item.user.user_report = Number(item.user.user_report);
                    item.comment_report = Number(item.comment_report);
                    item.user_report = item.user.user_report;
                })
                this.totalnum = Number(resolve['data'].total);
                this.activeName = 'first';
            },
            getmes2(resolve) {
                this.tableData2 = resolve['data'].mes;
                this.tableData2.forEach(item => {
                    item.time = Number(item.time);
                    item.user.timestamp = Number(item.user.timestamp);
                    item.user.comment_cnt = Number(item.user.comment_cnt);
                    item.user.user_report = Number(item.user.user_report);
                    item.comment_report = Number(item.comment_report);
                    item.user_report = item.user.user_report;
                })
                this.totalnum2 = Number(resolve['data'].total);
                this.activeName = 'second';
            },
            getmes3(resolve) {
                this.tableData = resolve['data'].mes1;
                this.currentPage4 = resolve['data'].page1;
                this.totalnum = resolve['data'].total1;
                this.tableData2 = resolve['data'].mes2;
                this.currentPage42 = resolve['data'].page2;
                this.totalnum2 = resolve['data'].total2;
            },
            toggleSelection(rows) {
                if (rows) {
                    rows.forEach(row => {
                        this.$refs.multipleTable.toggleRowSelection(row);
                    });
                } else {
                    this.$refs.multipleTable.clearSelection();
                }
            },
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            handleSelectionChange2(val) {
                this.multipleSelection2 = val;
            },
            handleSizeChange(val) {
            const that = this;
                console.log(val);
                var dat = {};
                this.k = val;
                dat['type'] = "photo_comment";
                dat['filters'] = this.filters1;
                dat['order_name'] = this.orderprop1;
                dat['amount'] = val;
                dat['page'] = this.currentPage4;
                if (this.order1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', that.getmes);
            },
            handleCurrentChange(val) {
            const that = this;
                console.log(`当前页: ${val}`);
                var dat = {};
                this.currentPage4 = val;
                dat['type'] = "photo_comment";
                dat['filters'] = this.filters1;
                dat['order_name'] = this.orderprop1;
                dat['amount'] = this.k;
                dat['page'] = val;
                if (this.order1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', that.getmes);
            },
            searchimage() {
            const that = this;
                var dat = {};
                dat['type'] = "photo_comment";
                dat['order_name'] = this.orderprop1;
                dat['amount'] = this.k;
                dat['page'] = this.currentPage4;
                if (this.order1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                this.filters1 = [];
                var filt = {};
                filt['content'] = this.searchcomment.split(" ");
                this.filters1.push(filt);
                filt = {};
                filt['banned'] = this.range1;
                this.filters1.push(filt);
                filt = {};
                if (this.datevalue1.length != 0) {
                    filt['min_timestamp'] = this.datevalue1[0].getTime();
                    filt['max_timestamp'] = this.datevalue1[1].getTime();
                    this.filters1.push(filt);
                    filt = {};
                }
                if (this.searchuser1 == true) {
                    filt['username'] = this.searcher.split(" ");
                    this.filters1.push(filt);
                    filt = {};
                }
                if (this.searchimg == true) {
                    filt['info'] = this.imgs.split(" ");
                    this.filters1.push(filt);
                    filt = {};
                }
                dat['filters'] = this.filters1;
                this.datevalue1 = [];
                request_json(dat, '/api/search', 'POST', that.getmes);
            },
            searchgallery() {
            const that = this;
                var dat = {};
                dat['type'] = "gallery_comment";
                dat['order_name'] = this.orderprop2;
                dat['amount'] = this.k2;
                dat['page'] = this.currentPage42;
                if (this.order2 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                this.filters2 = [];
                var filt = {};
                filt['content'] = this.searchcomment2.split(" ");
                this.filters2.push(filt);
                filt = {};
                filt['banned'] = this.range2;
                this.filters2.push(filt);
                filt = {};
                if (this.datevalue2.length != 0) {
                    filt['min_timestamp'] = this.datevalue2[0].getTime();
                    filt['max_timestamp'] = this.datevalue2[1].getTime();
                    this.filters2.push(filt);
                    filt = {};
                }
                if (this.searchuser2 == true) {
                    filt['username'] = this.searcher2.split(" ");
                    this.filters2.push(filt);
                    filt = {};
                }
                if (this.searchgal == true) {
                    filt['info'] = this.gals.split(" ");
                    this.filters2.push(filt);
                    filt = {};
                }
                dat['filters'] = this.filters2;
                this.datevalue2 = [];
                request_json(dat, '/api/search', 'POST', that.getmes2);
            },

            handleSizeChange2(val) {
            const that = this;
                console.log(`当前页: ${val}`);
                var dat = {};
                this.k = val;
                dat['type'] = "gallery_comment";
                dat['filters'] = this.filters2;
                dat['order_name'] = this.orderprop1;
                dat['amount'] = val;
                dat['page'] = this.currentPage4;
                if (this.order1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', that.getmes2);
            },
            handleCurrentChange2(val) {
            const that = this;
                console.log(`当前页: ${val}`);
                var dat = {};
                this.currentPage42 = val;
                dat['type'] = "gallery_comment";
                dat['filters'] = this.filters2;
                dat['order_name'] = this.orderprop1;
                dat['amount'] = this.k;
                dat['page'] = val;
                if (this.order1 == "descending") dat['order_method'] = false;
                else dat['order_method'] = true;
                request_json(dat, '/api/search', 'POST', that.getmes2);
            },
            imgsort({
                column,
                prop,
                order
            }) {
                var send = {};
                const that = this;
                if (column) {
                    send['type'] = "photo_comment";
                    send['page'] = this.currentPage4;
                    send['amount'] = this.k;
                    send['order_name'] = prop;
                    this.orderprop1 = prop;
                    if (order == "descending") send['order_method'] = false;
                    else send['order_method'] = true;
                    this.order1 = order;
                    send['filters'] = this.filters1;
                    request_json(send, '/api/search', 'POST', that.getmes);
                } else return;
            },
            galsort({
                column,
                prop,
                order
            }) {
                var send = {};
                const that = this;
                if (column) {
                    send['type'] = "gallery_comment";
                    send['page'] = this.currentPage42;
                    send['amount'] = this.k2;
                    send['order_name'] = prop;
                    this.orderprop2 = prop;
                    if (order == "descending") send['order_method'] = false;
                    else send['order_method'] = true;
                    this.order2 = order;
                    send['filters'] = this.filters2;
                    request_json(send, '/api/search', 'POST', that.getmes2);
                } else return;
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
            managealive1() {
                var n = {};
                const that = this;
                var lst = [];
                this.multipleSelection.forEach(element => {
                    lst.push(element.commentid);
                });
                n['operation'] = "alive";
                n['type'] = "photo_comment";
                n['list'] = lst;
                this.multipleSelection = [];
                request_json(n, '/api/admincomment', 'POST',that.defaultsearch);
            },
            managebnd1() {
            const that = this;
                var n = {};
                var lst = [];
                this.multipleSelection.forEach(element => {
                    lst.push(element.commentid);
                });
                n['operation'] = "forbid";
                n['list'] = lst;
                n['type'] = "photo_comment";
                this.multipleSelection = [];
                request_json(n, '/api/admincomment', 'POST',that.defaultsearch);
            },
            managealive2() {
            const that = this;
                var n = {};
                var lst = [];
                this.multipleSelection2.forEach(element => {
                    lst.push(element.commentid);
                });
                n['operation'] = "alive";
                n['type'] = "gallery_comment";
                n['list'] = lst;
                this.multipleSelection2 = [];
                request_json(n, '/api/admincomment', 'POST',that.defaultsearch2);
            },
            managebnd2() {
            const that = this;
                var n = {};
                var lst = [];
                this.multipleSelection2.forEach(element => {
                    lst.push(element.commentid);
                });
                n['operation'] = "forbid";
                n['type'] = "gallery_comment";
                n['list'] = lst;
                this.multipleSelection2 = [];
                request_json(n, '/api/admincomment', 'POST',that.defaultsearch2);
            },
            managedelete1() {
            const that = this;
                var n = {};
                var lst = [];
                this.multipleSelection.forEach(element => {
                    lst.push(element.commentid);
                });
                n['operation'] = "delete";
                n['list'] = lst;
                n['type'] = "photo_comment";
                this.multipleSelection = [];
                request_json(n, '/api/admincomment', 'POST',that.defaultsearch);
            },
            managedelete2() {
            const that = this;
                var n = {};
                var lst = [];
                this.multipleSelection2.forEach(element => {
                    lst.push(element.commentid);
                });
                n['operation'] = "delete";
                n['list'] = lst;
                n['type'] = "gallery_comment";
                this.multipleSelection2 = [];
                request_json(n, '/api/admincomment', 'POST',that.defaultsearch2);
            },
        },
        created() {
            var dat = {};
            const that = this;
            dat['type'] = "photo_comment";
            dat['order_name'] = this.orderprop1;
            dat['amount'] = this.k;
            dat['page'] = this.currentPage4;
            if (this.order1 == "descending") dat['order_method'] = false;
            else dat['order_method'] = true;
            this.filters1 = [];
            dat['filters'] = this.filters1;
            request_json(dat, '/api/search', 'POST', that.getmes);
            dat = {};
            dat['type'] = "gallery_comment";
            dat['order_name'] = this.orderprop2;
            dat['amount'] = this.k2;
            dat['page'] = this.currentPage42;
            if (this.order1 == "descending") dat['order_method'] = false;
            else dat['order_method'] = true;
            this.filters2 = [];
            dat['filters'] = this.filters2;
            request_json(dat, '/api/search', 'POST', that.getmes2);
        }
    }
</script>

<style scoped>

    .cell .el-button{
        margin-left:0;
        margin-bottom: 5px;
    }

    .demo-table-expand {
        font-size: 0;
    }

    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }

    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        margin-left:10px;
        width: 50%;
    }

    .search {
        width: 200px;
    }

    .search2 {
        width: 500px;
    }
</style>
