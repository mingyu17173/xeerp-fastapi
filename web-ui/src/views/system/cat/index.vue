<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入资讯分类"
                show-search
                label="资讯分类"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:cat:add']">新建资讯分类</el-button>
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
                            <el-form-item label="分类名称" prop="name">
                                <el-input
                                        v-model="queryParams.name"
                                        placeholder="请输入分类名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="${comment}" prop="sort">
                                <el-input
                                        v-model="queryParams.sort"
                                        placeholder="请输入${comment}"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="副菜单" prop="parentId">
                                <el-input
                                        v-model="queryParams.parentId"
                                        placeholder="请输入副菜单"
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
                <el-table v-loading="loading" :data="catList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="${comment}" align="center" prop="id"/>
                    <el-table-column label="分类名称" align="center" prop="name"/>
                    <el-table-column label="${comment}" align="center" prop="sort"/>
                    <el-table-column label="副菜单" align="center" prop="parentId"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:cat:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:cat:remove']">删除
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
        <!-- 添加或修改资讯分类对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="catRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="分类名称" prop="name">
                    <el-input v-model="form.name" placeholder="请输入分类名称"/>
                </el-form-item>
                <el-form-item label="${comment}" prop="sort">
                    <el-input v-model="form.sort" placeholder="请输入${comment}"/>
                </el-form-item>
                <el-form-item label="副菜单" prop="parentId">
                    <el-input v-model="form.parentId" placeholder="请输入副菜单"/>
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

<script setup name="Cat">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listCat, getCat, delCat, addCat, updateCat} from "@/api/system/cat";

    const {proxy} = getCurrentInstance();

    const catList = ref([]);
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
            name: null,
            sort: null,
            parentId: null
        },
        rules: {
            name: [
                {required: true, message: "分类名称不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "分类名称", value: "name"},
        {label: "$column.columnComment", value: "sort"},
        {label: "副菜单", value: "parentId"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询资讯分类列表 */
    function getList() {
        loading.value = true;
        listCat(queryParams.value).then(response => {
            catList.value = response.rows;
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
            name: null,
            sort: null,
            parentId: null
        };
        proxy.resetForm("catRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.name = res,
            queryParams.value.sort = res,
            queryParams.value.parentId = res,
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
        title.value = "添加资讯分类";
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
        getCat(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改资讯分类";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["catRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateCat(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addCat(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除资讯分类编号为"' + _ids + '"的数据项？').then(function () {
            return delCat(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/cat/export', {
            ...queryParams.value
        }, `cat_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
