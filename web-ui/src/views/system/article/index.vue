<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入资讯"
                show-search
                label="资讯"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['system:article:add']">新建资讯</el-button>
                <el-dropdown
                        v-if="headerMoreHandle.length > 0"
                        trigger="click"
                        style="margin-left: 5px; margin-right: 10px;"
                        @command="headerMoreHandleClick">
                    <el-button color="#f1f1f1">
                        <el-icon size="20">
                            <more-filled/>
                        </el-icon>
                    </el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item
                                    v-for="(item, index) in headerMoreHandle"
                                    :key="index"
                                    :icon="item.icon"
                                    :command="item.type">{{ item.name }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </template>
            <template v-slot:bottom-ft>
                <AdvancedFilter :title="'高级筛选'" style="margin-right: 20px;">
                    <template v-slot:content>
                        <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch"
                                 label-width="68px">
                            <el-form-item label="分类" prop="catId">
                                <el-input
                                        v-model="queryParams.catId"
                                        placeholder="请输入分类"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="名称" prop="title">
                                <el-input
                                        v-model="queryParams.title"
                                        placeholder="请输入名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="关键词" prop="keywords">
                                <el-input
                                        v-model="queryParams.keywords"
                                        placeholder="请输入关键词"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="介绍" prop="description">
                                <el-input
                                        v-model="queryParams.description"
                                        placeholder="请输入介绍"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="排序" prop="sort">
                                <el-input
                                        v-model="queryParams.sort"
                                        placeholder="请输入排序"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                        </el-form>
                    </template>
                </AdvancedFilter>
                <RefreshView style="margin-right: 20px;" @click="resetQuery"></RefreshView>
                <ShowFilter :columns="showColumn"></ShowFilter>
            </template>
        </header-view>
        <el-row :gutter="20" style="margin: 15px 0px;">
            <el-col :span="24">
                <el-table v-loading="loading" :data="articleList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="${comment}" align="center" prop="id"/>
                    <el-table-column label="分类" align="center" prop="catId"/>
                    <el-table-column label="名称" align="center" prop="title"/>
                    <el-table-column label="内容" align="center" prop="content"/>
                    <el-table-column label="关键词" align="center" prop="keywords"/>
                    <el-table-column label="介绍" align="center" prop="description"/>
                    <el-table-column label="是否显示0，显示，1不显示" align="center" prop="status"/>
                    <el-table-column label="排序" align="center" prop="sort"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['system:article:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['system:article:remove']">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div class="p-contianer">
                    <pagination
                            :page-sizes="[15, 20, 30, 40, 50, 100]"
                            v-show="total>0"
                            :total="total"
                            v-model:page="queryParams.pageNum"
                            v-model:limit="queryParams.pageSize"
                            @pagination="getList"
                    />
                </div>
            </el-col>
        </el-row>
        <!-- 添加或修改资讯对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="articleRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="分类" prop="catId">
                    <el-input v-model="form.catId" placeholder="请输入分类"/>
                </el-form-item>
                <el-form-item label="名称" prop="title">
                    <el-input v-model="form.title" placeholder="请输入名称"/>
                </el-form-item>
                <el-form-item label="内容">
                    <editor v-model="form.content" :min-height="192"/>
                </el-form-item>
                <el-form-item label="关键词" prop="keywords">
                    <el-input v-model="form.keywords" placeholder="请输入关键词"/>
                </el-form-item>
                <el-form-item label="介绍" prop="description">
                    <el-input v-model="form.description" placeholder="请输入介绍"/>
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input v-model="form.sort" placeholder="请输入排序"/>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="submitForm">确 定</el-button>
                    <el-button @click="cancel">取 消</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup name="Article">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listArticle, getArticle, delArticle, addArticle, updateArticle} from "@/api/system/article";

    const {proxy} = getCurrentInstance();

    const articleList = ref([]);
    const open = ref(false);
    const loading = ref(true);
    const showSearch = ref(true);
    const ids = ref([]);
    const single = ref(true);
    const multiple = ref(true);
    const total = ref(0);
    const title = ref("");

    const headerMoreHandle = ref([
        {
            icon: 'import',
            name: '导入',
            type: 'import'
        },
        {
            icon: 'export',
            name: '导出',
            type: 'export'
        }
    ])

    const data = reactive({
        form: {},
        queryParams: {
            pageNum: 1,
            pageSize: 14,
            catId: null,
            title: null,
            content: null,
            keywords: null,
            description: null,
            status: null,
            sort: null
        },
        rules: {}
    });

    const showColumn = ref([
        {label: "分类", value: "catId"},
        {label: "名称", value: "title"},
        {label: "内容", value: "content"},
        {label: "关键词", value: "keywords"},
        {label: "介绍", value: "description"},
        {label: "是否显示0，显示，1不显示", value: "status"},
        {label: "排序", value: "sort"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询资讯列表 */
    function getList() {
        loading.value = true;
        listArticle(queryParams.value).then(response => {
            articleList.value = response.rows;
            total.value = response.total;
            loading.value = false;
        });
    }

    // 取消按钮
    function cancel() {
        open.value = false;
        reset();
    }

    // 表单重置
    function reset() {
        form.value = {
            id: null,
            catId: null,
            title: null,
            content: null,
            keywords: null,
            description: null,
            status: null,
            sort: null
        };
        proxy.resetForm("articleRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.catId = res,
            queryParams.value.title = res,
            queryParams.value.content = res,
            queryParams.value.keywords = res,
            queryParams.value.description = res,
            queryParams.value.status = res,
            queryParams.value.sort = res,
            queryParams.value.pageNum = 1;
        getList();
    }

    /** 重置按钮操作 */
    function resetQuery() {
        proxy.resetForm("queryRef");
        handleQuery();
    }

    // 多选框选中数据
    function handleSelectionChange(selection) {
        ids.value = selection.map(item => item.id);
        single.value = selection.length != 1;
        multiple.value = !selection.length;
    }

    /** 新增按钮操作 */
    function handleAdd() {
        reset();
        open.value = true;
        title.value = "添加资讯";
    }

    const headerMoreHandleClick = (command) => {
        if (command == 'export') {
            //导入
            console.log("导入")
        } else if (command == 'import') {
            //导出
            console.log("导出")
        }
    }

    /** 修改按钮操作 */
    function handleUpdate(row) {
        reset();
        const _id = row.id || ids.value
        getArticle(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改资讯";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["articleRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateArticle(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addArticle(form.value).then(response => {
                        proxy.$modal.msgSuccess("新增成功");
                        open.value = false;
                        getList();
                    });
                }
            }
        });
    }

    /** 删除按钮操作 */
    function handleDelete(row) {
        const _ids = row.id || ids.value;
        proxy.$modal.confirm('是否确认删除资讯编号为"' + _ids + '"的数据项？').then(function () {
            return delArticle(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('system/article/export', {
            ...queryParams.value
        }, `article_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
