<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入产品厂商"
                show-search
                label="产品厂商"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:brand:add']">新建产品厂商</el-button>
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
                            <el-form-item label="厂商名称" prop="brandName">
                                <el-input
                                        v-model="queryParams.brandName"
                                        placeholder="请输入厂商名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="是否可用(1启用，0停用)" prop="isAvailable">
                                <el-input
                                        v-model="queryParams.isAvailable"
                                        placeholder="请输入是否可用(1启用，0停用)"
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
                <el-table v-loading="loading" :data="brandList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="产品厂商id" align="center" prop="id"/>
                    <el-table-column label="厂商名称" align="center" prop="brandName"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="是否可用(1启用，0停用)" align="center" prop="isAvailable"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="删除时间(软删除)" align="center" prop="deleteTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.deleteTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:brand:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:brand:remove']">删除
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
        <!-- 添加或修改产品厂商对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="brandRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="厂商名称" prop="brandName">
                    <el-input v-model="form.brandName" placeholder="请输入厂商名称"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="是否可用(1启用，0停用)" prop="isAvailable">
                    <el-input v-model="form.isAvailable" placeholder="请输入是否可用(1启用，0停用)"/>
                </el-form-item>
                <el-form-item label="创建人id" prop="createUid">
                    <el-input v-model="form.createUid" placeholder="请输入创建人id"/>
                </el-form-item>
                <el-form-item label="删除时间(软删除)" prop="deleteTime">
                    <el-date-picker clearable
                                    v-model="form.deleteTime"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择删除时间(软删除)">
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

<script setup name="Brand">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listBrand, getBrand, delBrand, addBrand, updateBrand} from "@/api/erp/brand";

    const {proxy} = getCurrentInstance();

    const brandList = ref([]);
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
            brandName: null,
            isAvailable: null,
            createUid: null,
            deleteTime: null
        },
        rules: {
            brandName: [
                {required: true, message: "厂商名称不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "厂商名称", value: "brandName"},
        {label: "是否可用(1启用，0停用)", value: "isAvailable"},
        {label: "创建人id", value: "createUid"},
        {label: "删除时间(软删除)", value: "deleteTime"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询产品厂商列表 */
    function getList() {
        loading.value = true;
        listBrand(queryParams.value).then(response => {
            brandList.value = response.rows;
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
            brandName: null,
            remark: null,
            isAvailable: null,
            createTime: null,
            createUid: null,
            deleteTime: null
        };
        proxy.resetForm("brandRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.brandName = res,
            queryParams.value.isAvailable = res,
            queryParams.value.createUid = res,
            queryParams.value.deleteTime = res,
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
        title.value = "添加产品厂商";
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
        getBrand(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改产品厂商";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["brandRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateBrand(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addBrand(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除产品厂商编号为"' + _ids + '"的数据项？').then(function () {
            return delBrand(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/brand/export', {
            ...queryParams.value
        }, `brand_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
