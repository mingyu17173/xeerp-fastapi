<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入虚拟仓位"
                show-search
                label="虚拟仓位"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:location:add']">新建虚拟仓位</el-button>
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
                            <el-form-item label="仓库id" prop="virtualWarehouseId">
                                <el-input
                                        v-model="queryParams.virtualWarehouseId"
                                        placeholder="请输入仓库id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓位名称" prop="locationName">
                                <el-input
                                        v-model="queryParams.locationName"
                                        placeholder="请输入仓位名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label=" 是否默认(0否 1是)" prop="isDefault">
                                <el-input
                                        v-model="queryParams.isDefault"
                                        placeholder="请输入 是否默认(0否 1是)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="使用部门" prop="departmentId">
                                <el-input
                                        v-model="queryParams.departmentId"
                                        placeholder="请输入使用部门"
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
                <el-table v-loading="loading" :data="locationList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="虚拟仓位id" align="center" prop="id"/>
                    <el-table-column label="仓库组id" align="center" prop="groupId"/>
                    <el-table-column label="仓库id" align="center" prop="virtualWarehouseId"/>
                    <el-table-column label="仓位名称" align="center" prop="locationName"/>
                    <el-table-column label=" 是否默认(0否 1是)" align="center" prop="isDefault"/>
                    <el-table-column label="使用部门" align="center" prop="departmentId"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:location:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:location:remove']">删除
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
        <!-- 添加或修改虚拟仓位对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="locationRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="仓库组id" prop="groupId">
                    <el-input v-model="form.groupId" placeholder="请输入仓库组id"/>
                </el-form-item>
                <el-form-item label="仓库id" prop="virtualWarehouseId">
                    <el-input v-model="form.virtualWarehouseId" placeholder="请输入仓库id"/>
                </el-form-item>
                <el-form-item label="仓位名称" prop="locationName">
                    <el-input v-model="form.locationName" placeholder="请输入仓位名称"/>
                </el-form-item>
                <el-form-item label=" 是否默认(0否 1是)" prop="isDefault">
                    <el-input v-model="form.isDefault" placeholder="请输入 是否默认(0否 1是)"/>
                </el-form-item>
                <el-form-item label="使用部门" prop="departmentId">
                    <el-input v-model="form.departmentId" placeholder="请输入使用部门"/>
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

<script setup name="Location">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listLocation, getLocation, delLocation, addLocation, updateLocation} from "@/api/erp/location";

    const {proxy} = getCurrentInstance();

    const locationList = ref([]);
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
            virtualWarehouseId: null,
            locationName: null,
            isDefault: null,
            departmentId: null,
            createUid: null
        },
        rules: {
            groupId: [
                {required: true, message: "仓库组id不能为空", trigger: "blur"}
            ],
            virtualWarehouseId: [
                {required: true, message: "仓库id不能为空", trigger: "blur"}
            ],
            locationName: [
                {required: true, message: "仓位名称不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "仓库组id", value: "groupId"},
        {label: "仓库id", value: "virtualWarehouseId"},
        {label: "仓位名称", value: "locationName"},
        {label: " 是否默认(0否 1是)", value: "isDefault"},
        {label: "使用部门", value: "departmentId"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询虚拟仓位列表 */
    function getList() {
        loading.value = true;
        listLocation(queryParams.value).then(response => {
            locationList.value = response.rows;
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
            virtualWarehouseId: null,
            locationName: null,
            isDefault: null,
            departmentId: null,
            remark: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("locationRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.groupId = res,
            queryParams.value.virtualWarehouseId = res,
            queryParams.value.locationName = res,
            queryParams.value.isDefault = res,
            queryParams.value.departmentId = res,
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
        title.value = "添加虚拟仓位";
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
        getLocation(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改虚拟仓位";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["locationRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateLocation(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addLocation(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除虚拟仓位编号为"' + _ids + '"的数据项？').then(function () {
            return delLocation(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/location/export', {
            ...queryParams.value
        }, `location_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
