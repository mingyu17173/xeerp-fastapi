<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入实体仓库"
                show-search
                label="实体仓库"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:warehouse:add']">新建实体仓库</el-button>
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
                            <el-form-item label="仓库名称" prop="locationName">
                                <el-input
                                        v-model="queryParams.locationName"
                                        placeholder="请输入仓库名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓库编号" prop="warehouseId">
                                <el-input
                                        v-model="queryParams.warehouseId"
                                        placeholder="请输入仓库编号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓库所在省份id" prop="provinceId">
                                <el-input
                                        v-model="queryParams.provinceId"
                                        placeholder="请输入仓库所在省份id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="所在城市id" prop="cityId">
                                <el-input
                                        v-model="queryParams.cityId"
                                        placeholder="请输入所在城市id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="所在区域id" prop="areaId">
                                <el-input
                                        v-model="queryParams.areaId"
                                        placeholder="请输入所在区域id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓库地址" prop="locationAddr">
                                <el-input
                                        v-model="queryParams.locationAddr"
                                        placeholder="请输入仓库地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="合同开始日期" prop="contractBeginDate">
                                <el-date-picker clearable
                                                v-model="queryParams.contractBeginDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择合同开始日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="合同结束日期" prop="contractEndDate">
                                <el-date-picker clearable
                                                v-model="queryParams.contractEndDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择合同结束日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="免租期(天)" prop="freePeriod">
                                <el-input
                                        v-model="queryParams.freePeriod"
                                        placeholder="请输入免租期(天)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="是否可用(1启用 0停用)" prop="isAvailable">
                                <el-input
                                        v-model="queryParams.isAvailable"
                                        placeholder="请输入是否可用(1启用 0停用)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="联系人" prop="contacts">
                                <el-input
                                        v-model="queryParams.contacts"
                                        placeholder="请输入联系人"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="手机" prop="tel">
                                <el-input
                                        v-model="queryParams.tel"
                                        placeholder="请输入手机"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="固定电话" prop="phone">
                                <el-input
                                        v-model="queryParams.phone"
                                        placeholder="请输入固定电话"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="传真" prop="fax">
                                <el-input
                                        v-model="queryParams.fax"
                                        placeholder="请输入传真"
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
                    <el-table-column label="实体仓id" align="center" prop="id"/>
                    <el-table-column label="仓库名称" align="center" prop="locationName"/>
                    <el-table-column label="仓库编号" align="center" prop="warehouseId"/>
                    <el-table-column label="仓库所在省份id" align="center" prop="provinceId"/>
                    <el-table-column label="所在城市id" align="center" prop="cityId"/>
                    <el-table-column label="所在区域id" align="center" prop="areaId"/>
                    <el-table-column label="仓库地址" align="center" prop="locationAddr"/>
                    <el-table-column label="仓库类型 1协议仓 2公共仓" align="center" prop="locationType"/>
                    <el-table-column label="合同开始日期" align="center" prop="contractBeginDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.contractBeginDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="合同结束日期" align="center" prop="contractEndDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.contractEndDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="免租期(天)" align="center" prop="freePeriod"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="是否可用(1启用 0停用)" align="center" prop="isAvailable"/>
                    <el-table-column label="联系人" align="center" prop="contacts"/>
                    <el-table-column label="手机" align="center" prop="tel"/>
                    <el-table-column label="固定电话" align="center" prop="phone"/>
                    <el-table-column label="传真" align="center" prop="fax"/>
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
        <!-- 添加或修改实体仓库对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="warehouseRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="仓库名称" prop="locationName">
                    <el-input v-model="form.locationName" placeholder="请输入仓库名称"/>
                </el-form-item>
                <el-form-item label="仓库编号" prop="warehouseId">
                    <el-input v-model="form.warehouseId" placeholder="请输入仓库编号"/>
                </el-form-item>
                <el-form-item label="仓库所在省份id" prop="provinceId">
                    <el-input v-model="form.provinceId" placeholder="请输入仓库所在省份id"/>
                </el-form-item>
                <el-form-item label="所在城市id" prop="cityId">
                    <el-input v-model="form.cityId" placeholder="请输入所在城市id"/>
                </el-form-item>
                <el-form-item label="所在区域id" prop="areaId">
                    <el-input v-model="form.areaId" placeholder="请输入所在区域id"/>
                </el-form-item>
                <el-form-item label="仓库地址" prop="locationAddr">
                    <el-input v-model="form.locationAddr" placeholder="请输入仓库地址"/>
                </el-form-item>
                <el-form-item label="合同开始日期" prop="contractBeginDate">
                    <el-date-picker clearable
                                    v-model="form.contractBeginDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择合同开始日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="合同结束日期" prop="contractEndDate">
                    <el-date-picker clearable
                                    v-model="form.contractEndDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择合同结束日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="免租期(天)" prop="freePeriod">
                    <el-input v-model="form.freePeriod" placeholder="请输入免租期(天)"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="是否可用(1启用 0停用)" prop="isAvailable">
                    <el-input v-model="form.isAvailable" placeholder="请输入是否可用(1启用 0停用)"/>
                </el-form-item>
                <el-form-item label="联系人" prop="contacts">
                    <el-input v-model="form.contacts" placeholder="请输入联系人"/>
                </el-form-item>
                <el-form-item label="手机" prop="tel">
                    <el-input v-model="form.tel" placeholder="请输入手机"/>
                </el-form-item>
                <el-form-item label="固定电话" prop="phone">
                    <el-input v-model="form.phone" placeholder="请输入固定电话"/>
                </el-form-item>
                <el-form-item label="传真" prop="fax">
                    <el-input v-model="form.fax" placeholder="请输入传真"/>
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
    import {listWarehouse, getWarehouse, delWarehouse, addWarehouse, updateWarehouse} from "@/api/erp/realWarehouse";

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
            locationName: null,
            warehouseId: null,
            provinceId: null,
            cityId: null,
            areaId: null,
            locationAddr: null,
            locationType: null,
            contractBeginDate: null,
            contractEndDate: null,
            freePeriod: null,
            isAvailable: null,
            contacts: null,
            tel: null,
            phone: null,
            fax: null,
            createUid: null
        },
        rules: {
            locationName: [
                {required: true, message: "仓库名称不能为空", trigger: "blur"}
            ],
            warehouseId: [
                {required: true, message: "仓库编号不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "仓库名称", value: "locationName"},
        {label: "仓库编号", value: "warehouseId"},
        {label: "仓库所在省份id", value: "provinceId"},
        {label: "所在城市id", value: "cityId"},
        {label: "所在区域id", value: "areaId"},
        {label: "仓库地址", value: "locationAddr"},
        {label: "仓库类型 1协议仓 2公共仓", value: "locationType"},
        {label: "合同开始日期", value: "contractBeginDate"},
        {label: "合同结束日期", value: "contractEndDate"},
        {label: "免租期(天)", value: "freePeriod"},
        {label: "是否可用(1启用 0停用)", value: "isAvailable"},
        {label: "联系人", value: "contacts"},
        {label: "手机", value: "tel"},
        {label: "固定电话", value: "phone"},
        {label: "传真", value: "fax"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询实体仓库列表 */
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
            locationName: null,
            warehouseId: null,
            provinceId: null,
            cityId: null,
            areaId: null,
            locationAddr: null,
            locationType: null,
            contractBeginDate: null,
            contractEndDate: null,
            freePeriod: null,
            remark: null,
            isAvailable: null,
            contacts: null,
            tel: null,
            phone: null,
            fax: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("warehouseRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.locationName = res,
            queryParams.value.warehouseId = res,
            queryParams.value.provinceId = res,
            queryParams.value.cityId = res,
            queryParams.value.areaId = res,
            queryParams.value.locationAddr = res,
            queryParams.value.locationType = res,
            queryParams.value.contractBeginDate = res,
            queryParams.value.contractEndDate = res,
            queryParams.value.freePeriod = res,
            queryParams.value.isAvailable = res,
            queryParams.value.contacts = res,
            queryParams.value.tel = res,
            queryParams.value.phone = res,
            queryParams.value.fax = res,
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
        title.value = "添加实体仓库";
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
            title.value = "修改实体仓库";
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
        proxy.$modal.confirm('是否确认删除实体仓库编号为"' + _ids + '"的数据项？').then(function () {
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
