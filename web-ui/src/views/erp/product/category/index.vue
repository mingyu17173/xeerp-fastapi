<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入商品分类"
                show-search
                label="商品分类"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:category:add']">新建商品分类</el-button>
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
                            <el-form-item label="分类名称" prop="categoryName">
                                <el-input
                                        v-model="queryParams.categoryName"
                                        placeholder="请输入分类名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="父级分类id" prop="parentId">
                                <el-input
                                        v-model="queryParams.parentId"
                                        placeholder="请输入父级分类id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="是否可用" prop="isAvailable">
                                <el-input
                                        v-model="queryParams.isAvailable"
                                        placeholder="请输入是否可用"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="创建人id" prop="createUid">
                                <el-input
                                        v-model="queryParams.createUid"
                                        placeholder="请输入创建人id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="删除时间(软删除)" prop="deleteTime">
                                <el-date-picker clearable
                                                v-model="queryParams.deleteTime"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择删除时间(软删除)">
                                </el-date-picker>
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
                <el-table
                        v-if="refreshTable"
                        border stripe show-header highlight-current-row
                        v-loading="loading"
                        :data="categoryList"
                        row-key="id"
                        :default-expand-all="isExpandAll"
                        :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
                >
                    <el-table-column label="分类名称" prop="categoryName"/>
                    <el-table-column label="父级分类id" align="center" prop="parentId"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="是否可用" align="center" prop="isAvailable"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="删除时间(软删除)" align="center" prop="deleteTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.deleteTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:category:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Plus" @click="handleAdd(scope.row)"
                                       v-hasPermi="['erp:category:add']">新增
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:category:remove']">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <!-- 添加或修改商品分类对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="categoryRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="分类名称" prop="categoryName">
                    <el-input v-model="form.categoryName" placeholder="请输入分类名称"/>
                </el-form-item>
                <el-form-item label="父级分类id" prop="parentId">
                    <el-tree-select
                            v-model="form.parentId"
                            :data="categoryOptions"
                            :props="{ value: 'id', label: 'categoryName', children: 'children' }"
                            value-key="id"
                            placeholder="请选择父级分类id"
                            check-strictly
                    />
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="是否可用" prop="isAvailable">
                    <el-input v-model="form.isAvailable" placeholder="请输入是否可用"/>
                </el-form-item>
                <el-form-item label="创建人id" prop="createUid">
                    <el-input v-model="form.createUid" placeholder="请输入创建人id"/>
                </el-form-item>
                <el-form-item label="删除时间(软删除)" prop="deleteTime">
                    <el-date-picker clearable
                                    v-model="form.deleteTime"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="选择删除时间(软删除)">
                    </el-date-picker>
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

<script setup name="Category">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listCategory, getCategory, delCategory, addCategory, updateCategory} from "@/api/erp/category";

    const {proxy} = getCurrentInstance();

    const categoryList = ref([]);
    const categoryOptions = ref([]);
    const open = ref(false);
    const loading = ref(true);
    const showSearch = ref(true);
    const title = ref("");
    const isExpandAll = ref(true);
    const refreshTable = ref(true);

    const data = reactive({
        form: {},
        queryParams: {
            categoryName: null,
            parentId: null,
            isAvailable: null,
            createUid: null,
            deleteTime: null
        },
        rules: {
            categoryName: [
                {required: true, message: "分类名称不能为空", trigger: "blur"}
            ],
        }
    });


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

    const showColumn = ref([
        {label: "分类名称", value: "categoryName"},
        {label: "父级分类id", value: "parentId"},
        {label: "是否可用（1启用，0停用）", value: "isAvailable"},
        {label: "创建人id", value: "createUid"},
        {label: "删除时间(软删除)", value: "deleteTime"},
    ])

    const {queryParams, form, rules} = toRefs(data);

    /** 查询商品分类列表 */
    function getList() {
        loading.value = true;
        listCategory(queryParams.value).then(response => {
            categoryList.value = proxy.handleTree(response.data, "id", "parentId");
            loading.value = false;
        });
    }

    /** 查询商品分类下拉树结构 */
    function getTreeselect() {
        listCategory().then(response => {
            categoryOptions.value = [];
            const data = {id: 0, categoryName: '顶级节点', children: []};
            data.children = proxy.handleTree(response.data, "id", "parentId");
            categoryOptions.value.push(data);
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
            categoryName: null,
            parentId: null,
            remark: null,
            isAvailable: null,
            createTime: null,
            createUid: null,
            deleteTime: null
        };
        proxy.resetForm("categoryRef");
    }

    /** 搜索按钮操作 */
    function handleQuery() {
        getList();
    }

    /** 重置按钮操作 */
    function resetQuery() {
        proxy.resetForm("queryRef");
        handleQuery();
    }

    /** 新增按钮操作 */
    function handleAdd(row) {
        reset();
        getTreeselect();
        if (row != null && row.id) {
            form.value.parentId = row.id;
        } else {
            form.value.parentId = 0;
        }
        open.value = true;
        title.value = "添加商品分类";
    }

    /** 展开/折叠操作 */
    function toggleExpandAll() {
        refreshTable.value = false;
        isExpandAll.value = !isExpandAll.value;
        nextTick(() => {
            refreshTable.value = true;
        });
    }

    /** 修改按钮操作 */
    async function handleUpdate(row) {
        reset();
        await getTreeselect();
        if (row != null) {
            form.value.parentId = row.parentId;
        }
        getCategory(row.id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改商品分类";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["categoryRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateCategory(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addCategory(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除商品分类编号为"' + row.id + '"的数据项？').then(function () {
            return delCategory(row.id);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    getList();
</script>
