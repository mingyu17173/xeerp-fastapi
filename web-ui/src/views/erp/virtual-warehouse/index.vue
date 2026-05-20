<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入虚拟仓库"
                show-search
                label="虚拟仓库"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:warehouse:add']">新建虚拟仓库</el-button>
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
                            <el-form-item label="仓库组id" prop="groupId">
                                <el-input
                                        v-model="queryParams.groupId"
                                        placeholder="请输入仓库组id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓库编号" prop="warehouseKey">
                                <el-input
                                        v-model="queryParams.warehouseKey"
                                        placeholder="请输入仓库编号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓库名称" prop="warehouseName">
                                <el-input
                                        v-model="queryParams.warehouseName"
                                        placeholder="请输入仓库名称"
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
                        </el-form>
                    </template>
                </AdvancedFilter>
                <RefreshView style="margin-right: 20px;" @click="resetQuery"></RefreshView>
                <ShowFilter :columns="showColumn"></ShowFilter>
            </template>
        </header-view>
        <el-row :gutter="20" style="margin: 15px 0px;">
            <el-col :span="24">
                <el-table v-loading="loading" :data="warehouseList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="虚拟仓库id" align="center" prop="id"/>
                    <el-table-column label="仓库组id" align="center" prop="groupId"/>
                    <el-table-column label="仓库编号" align="center" prop="warehouseKey"/>
                    <el-table-column label="仓库名称" align="center" prop="warehouseName"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:warehouse:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:warehouse:remove']">删除
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
        <!-- 添加或修改虚拟仓库对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="warehouseRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="仓库组id" prop="groupId">
                    <el-input v-model="form.groupId" placeholder="请输入仓库组id"/>
                </el-form-item>
                <el-form-item label="仓库编号" prop="warehouseKey">
                    <el-input v-model="form.warehouseKey" placeholder="请输入仓库编号"/>
                </el-form-item>
                <el-form-item label="仓库名称" prop="warehouseName">
                    <el-input v-model="form.warehouseName" placeholder="请输入仓库名称"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="创建人id" prop="createUid">
                    <el-input v-model="form.createUid" placeholder="请输入创建人id"/>
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

<script setup name="Warehouse">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listWarehouse, getWarehouse, delWarehouse, addWarehouse, updateWarehouse} from "@/api/erp/virtualWarehouse";

    const {proxy} = getCurrentInstance();

    const warehouseList = ref([]);
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
            groupId: null,
            warehouseKey: null,
            warehouseName: null,
            createUid: null
        },
        rules: {
            groupId: [
                {required: true, message: "仓库组id不能为空", trigger: "blur"}
            ],
            warehouseKey: [
                {required: true, message: "仓库编号不能为空", trigger: "blur"}
            ],
            warehouseName: [
                {required: true, message: "仓库名称不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "仓库组id", value: "groupId"},
        {label: "仓库编号", value: "warehouseKey"},
        {label: "仓库名称", value: "warehouseName"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询虚拟仓库列表 */
    function getList() {
        loading.value = true;
        listWarehouse(queryParams.value).then(response => {
            warehouseList.value = response.rows;
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
            groupId: null,
            warehouseKey: null,
            warehouseName: null,
            remark: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("warehouseRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.groupId = res,
            queryParams.value.warehouseKey = res,
            queryParams.value.warehouseName = res,
            queryParams.value.createUid = res,
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
        title.value = "添加虚拟仓库";
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
        getWarehouse(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改虚拟仓库";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["warehouseRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateWarehouse(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addWarehouse(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除虚拟仓库编号为"' + _ids + '"的数据项？').then(function () {
            return delWarehouse(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/warehouse/export', {
            ...queryParams.value
        }, `warehouse_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
