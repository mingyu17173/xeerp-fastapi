<template>
    <el-dialog v-model="dialogVisible" :title="titleMap[type-1]" :width="type==1?680:460" destroy-on-close
               append-to-body @closed="emit('closed')">

        <template v-if="type==1">
            <div class="sc-user-select">
                <div class="sc-user-select__left">
                    <div class="sc-user-select__search">
                        <el-input v-model="keyword" prefix-icon="search" placeholder="搜索成员">
                            <template #append>
                                <el-button icon="search" @click="search"></el-button>
                            </template>
                        </el-input>
                    </div>
                    <div class="sc-user-select__select">
                        <div class="sc-user-select__tree" v-loading="showGrouploading">
                            <el-scrollbar>
                                <el-tree class="menu" ref="groupTree" :data="group" :node-key="groupProps.key"
                                         :props="groupProps" highlight-current :expand-on-click-node="false"
                                         :current-node-key="groupId" @node-click="groupClick"/>
                            </el-scrollbar>
                        </div>
                        <div class="sc-user-select__user" v-loading="showUserloading">
                            <div class="sc-user-select__user__list">
                                <el-scrollbar ref="userScrollbar">
                                    <el-tree class="menu" ref="userTree" :data="user" :node-key="userProps.key"
                                             :props="userProps" :default-checked-keys="selectedIds" show-checkbox
                                             check-on-click-node @check-change="userClick"></el-tree>
                                </el-scrollbar>
                            </div>
                            <footer>
                                <el-pagination background layout="prev,next" small :total="total" :page-size="pageSize"
                                               v-model:currentPage="currentPage"
                                               @current-change="paginationChange"></el-pagination>
                            </footer>
                        </div>
                    </div>
                </div>
                <div class="sc-user-select__toicon">
                    <el-icon>
                        <ArrowRight/>
                    </el-icon>
                </div>
                <div class="sc-user-select__selected">
                    <header>已选 ({{selected.length}})</header>
                    <ul>
                        <el-scrollbar>
                            <li v-for="(item, index) in selected" :key="item.id">
                            <span class="name">
                                <el-avatar size="small">{{item.name.substring(0,1)}}</el-avatar>
                                <label>{{item.name}}</label>
                            </span>
                                <span class="delete">
                                <el-button type="danger" icon="Delete" circle size="small"
                                           @click="deleteSelected(index)"></el-button>
                            </span>
                            </li>
                        </el-scrollbar>
                    </ul>
                </div>
            </div>
        </template>

        <template v-if="type==2">
            <div class="sc-user-select sc-user-select-role">
                <div class="sc-user-select__left">
                    <div class="sc-user-select__select">
                        <div class="sc-user-select__tree" v-loading="showGrouploading">
                            <el-scrollbar>
                                <el-tree class="menu" ref="groupTree" :data="role" :node-key="roleProps.key"
                                         :props="roleProps" show-checkbox check-strictly check-on-click-node
                                         :expand-on-click-node="false" :default-checked-keys="selectedIds"
                                         @check-change="roleClick"/>
                            </el-scrollbar>
                        </div>
                    </div>
                </div>
                <div class="sc-user-select__toicon">
                    <el-icon>
                        <ArrowRight/>
                    </el-icon>
                </div>
                <div class="sc-user-select__selected">
                    <header>已选 ({{selected.length}})</header>
                    <ul>
                        <el-scrollbar>
                            <li v-for="(item, index) in selected" :key="item.id">
                            <span class="name">
                                <label>{{item.name}}</label>
                            </span>
                                <span class="delete">
                                <el-button type="danger" icon="Delete" circle size="small"
                                           @click="deleteSelected(index)"></el-button>
                            </span>
                            </li>
                        </el-scrollbar>
                    </ul>
                </div>
            </div>
        </template>
        <template #footer>
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="save">确 认</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
    import config from './workflow'

    import {getCurrentInstance} from "vue"

    const {proxy} = getCurrentInstance();

    const props = defineProps({
        modelValue: {
            type: Object,
            default: () => {
            }
        }
    })

    const emit = defineEmits(['update'])

    const state = reactive({
        groupProps: config.group.props,
        userProps: config.user.props,
        roleProps: config.role.props,
        titleMap: ['人员选择', '角色选择'],
        dialogVisible: false,
        showGrouploading: false,
        showUserloading: false,
        keyword: '',
        groupId: '',
        pageSize: config.user.pageSize,
        total: 0,
        currentPage: 1,
        group: [],
        user: [],
        role: [],
        type: 1,
        selected: [],
        value: []
    })

    const selectedIds = computed(() => {
        return state.selected.map(t => t.id)
    })

    //打开赋值
    const open = (type, data) => {
        state.type = type
        state.value = data || []
        state.selected = JSON.parse(JSON.stringify(data || []))
        state.dialogVisible = true

        if (state.type == 1) {
            getGroup()
            getUser()
        } else if (state.type == 2) {
            getRole()
        }
    }

    //获取组织
    const getGroup = async () => {
        state.showGrouploading = true;
        var res = await config.group.apiObj.get();
        state.showGrouploading = false;
        var allNode = {[config.group.props.key]: '', [config.group.props.label]: '所有'}
        res.data.unshift(allNode);
        state.group = config.group.parseData(res).rows
    }

    //获取用户
    const getUser = async () => {
        state.showUserloading = true;
        var params = {
            [config.user.request.keyword]: state.keyword || null,
            [config.user.request.groupId]: state.groupId || null,
            [config.user.request.page]: state.currentPage,
            [config.user.request.pageSize]: state.pageSize
        }
        var res = await config.user.apiObj.get(params);
        state.showUserloading = false;
        state.user = config.user.parseData(res).rows;
        state.total = config.user.parseData(res).total || 0;
        proxy.$refs.userScrollbar.setScrollTop(0)
    }

    //获取角色
    const getRole = async () => {
        state.showGrouploading = true;
        var res = await config.role.apiObj.get();
        state.showGrouploading = false;
        state.role = config.role.parseData(res).rows
    }

    //组织点击
    const groupClick = (data) => {
        state.keyword = ''
        state.currentPage = 1
        state.groupId = data[config.group.props.key]
        getUser()
    }

    //用户点击
    const userClick = (data, checked) => {
        if (checked) {
            state.selected.push({
                id: data[config.user.props.key],
                name: data[config.user.props.label]
            })
        } else {
            state.selected = state.selected.filter(item => item.id != data[config.user.props.key])
        }
    }

    //用户分页点击
    const paginationChange = () => {
        getUser()
    }

    //用户搜索
    const search = () => {
        state.groupId = ''
        proxy.$refs.groupTree.setCurrentKey(state.groupId)
        state.currentPage = 1
        getUser()
    }

    //删除已选
    const deleteSelected = (index) => {
        state.selected.splice(index, 1);
        if (state.type == 1) {
            proxy.$refs.userTree.setCheckedKeys(state.selectedIds)
        } else if (state.type == 2) {
            proxy.$refs.groupTree.setCheckedKeys(state.selectedIds)
        }
    }

    //角色点击
    const roleClick = (data, checked) => {
        if (checked) {
            state.selected.push({
                id: data[config.role.props.key],
                name: data[config.role.props.label]
            })
        } else {
            state.selected = state.selected.filter(item => item.id != data[config.role.props.key])
        }
    }

    //提交保存
    const save = () => {
        state.value.splice(0, state.value.length);
        state.selected.map(item => {
            state.value.push(item)
        })
        state.dialogVisible = false
    }
</script>

<style scoped>
    .sc-user-select {
        display: flex;
    }

    .sc-user-select__left {
        width: 400px;
    }

    .sc-user-select__right {
        flex: 1;
    }

    .sc-user-select__search {
        padding-bottom: 10px;
    }

    .sc-user-select__select {
        display: flex;
        border: 1px solid var(--el-border-color-light);
        background: var(--el-color-white);
    }

    .sc-user-select__tree {
        width: 200px;
        height: 300px;
        border-right: 1px solid var(--el-border-color-light);
    }

    .sc-user-select__user {
        width: 200px;
        height: 300px;
        display: flex;
        flex-direction: column;
    }

    .sc-user-select__user__list {
        flex: 1;
        overflow: auto;
    }

    .sc-user-select__user footer {
        height: 36px;
        padding-top: 5px;
        border-top: 1px solid var(--el-border-color-light);
    }

    .sc-user-select__toicon {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 10px;
    }

    .sc-user-select__toicon i {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #ccc;
        width: 20px;
        height: 20px;
        text-align: center;
        line-height: 20px;
        border-radius: 50%;
        color: #fff;
    }

    .sc-user-select__selected {
        height: 345px;
        width: 200px;
        border: 1px solid var(--el-border-color-light);
        background: var(--el-color-white);
    }

    .sc-user-select__selected header {
        height: 43px;
        line-height: 43px;
        border-bottom: 1px solid var(--el-border-color-light);
        padding: 0 15px;
        font-size: 12px;
    }

    .sc-user-select__selected ul {
        height: 300px;
        overflow: auto;
    }

    .sc-user-select__selected li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 5px 5px 5px 15px;
        height: 38px;
    }

    .sc-user-select__selected li .name {
        display: flex;
        align-items: center;
    }

    .sc-user-select__selected li .name .el-avatar {
        background: #0052cc;
        margin-right: 10px;
    }

    .sc-user-select__selected li .name label {
    }

    .sc-user-select__selected li .delete {
        display: none;
    }

    .sc-user-select__selected li:hover {
        background: var(--el-color-primary-light-9);
    }

    .sc-user-select__selected li:hover .delete {
        display: inline-block;
    }

    .sc-user-select-role .sc-user-select__left {
        width: 200px;
    }

    .sc-user-select-role .sc-user-select__tree {
        border: none;
        height: 343px;
    }

    .sc-user-select-role .sc-user-select__selected {
    }

    [data-theme='dark'] .sc-user-select__selected li:hover {
        background: rgba(0, 0, 0, 0.2);
    }

    [data-theme='dark'] .sc-user-select__toicon i {
        background: #383838;
    }
</style>