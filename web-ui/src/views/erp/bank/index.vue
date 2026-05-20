<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入合作伙伴银行"
                show-search
                label="合作伙伴银行"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:bank:add']">新建合作伙伴银行</el-button>
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
                            <el-form-item label="银行名称" prop="bankName">
                                <el-input
                                        v-model="queryParams.bankName"
                                        placeholder="请输入银行名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="银行账号" prop="bankAccount">
                                <el-input
                                        v-model="queryParams.bankAccount"
                                        placeholder="请输入银行账号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="电话" prop="phone">
                                <el-input
                                        v-model="queryParams.phone"
                                        placeholder="请输入电话"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="地址" prop="addr">
                                <el-input
                                        v-model="queryParams.addr"
                                        placeholder="请输入地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="联行号" prop="ibknum">
                                <el-input
                                        v-model="queryParams.ibknum"
                                        placeholder="请输入联行号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="邮政编码" prop="zipCide">
                                <el-input
                                        v-model="queryParams.zipCide"
                                        placeholder="请输入邮政编码"
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
                <el-table v-loading="loading" :data="bankList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="合作伙伴银行id" align="center" prop="id"/>
                    <el-table-column label="银行名称" align="center" prop="bankName"/>
                    <el-table-column label="银行账号" align="center" prop="bankAccount"/>
                    <el-table-column label="电话" align="center" prop="phone"/>
                    <el-table-column label="地址" align="center" prop="addr"/>
                    <el-table-column label="联行号" align="center" prop="ibknum"/>
                    <el-table-column label="邮政编码" align="center" prop="zipCide"/>
                    <el-table-column label="删除时间(软删除)" align="center" prop="deleteTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.deleteTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:bank:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:bank:remove']">删除
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
        <!-- 添加或修改合作伙伴银行对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="bankRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="银行名称" prop="bankName">
                    <el-input v-model="form.bankName" placeholder="请输入银行名称"/>
                </el-form-item>
                <el-form-item label="银行账号" prop="bankAccount">
                    <el-input v-model="form.bankAccount" placeholder="请输入银行账号"/>
                </el-form-item>
                <el-form-item label="电话" prop="phone">
                    <el-input v-model="form.phone" placeholder="请输入电话"/>
                </el-form-item>
                <el-form-item label="地址" prop="addr">
                    <el-input v-model="form.addr" placeholder="请输入地址"/>
                </el-form-item>
                <el-form-item label="联行号" prop="ibknum">
                    <el-input v-model="form.ibknum" placeholder="请输入联行号"/>
                </el-form-item>
                <el-form-item label="邮政编码" prop="zipCide">
                    <el-input v-model="form.zipCide" placeholder="请输入邮政编码"/>
                </el-form-item>
                <el-form-item label="删除时间(软删除)" prop="deleteTime">
                    <el-date-picker clearable
                                    v-model="form.deleteTime"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择删除时间(软删除)">
                    </el-date-picker>
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

<script setup name="Bank">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listBank, getBank, delBank, addBank, updateBank} from "@/api/erp/bank";

    const {proxy} = getCurrentInstance();

    const bankList = ref([]);
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
            bankName: null,
            bankAccount: null,
            phone: null,
            addr: null,
            ibknum: null,
            zipCide: null,
            deleteTime: null,
            createUid: null
        },
        rules: {}
    });

    const showColumn = ref([
        {label: "银行名称", value: "bankName"},
        {label: "银行账号", value: "bankAccount"},
        {label: "电话", value: "phone"},
        {label: "地址", value: "addr"},
        {label: "联行号", value: "ibknum"},
        {label: "邮政编码", value: "zipCide"},
        {label: "删除时间(软删除)", value: "deleteTime"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询合作伙伴银行列表 */
    function getList() {
        loading.value = true;
        listBank(queryParams.value).then(response => {
            bankList.value = response.rows;
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
            bankName: null,
            bankAccount: null,
            phone: null,
            addr: null,
            ibknum: null,
            zipCide: null,
            deleteTime: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("bankRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.bankName = res,
            queryParams.value.bankAccount = res,
            queryParams.value.phone = res,
            queryParams.value.addr = res,
            queryParams.value.ibknum = res,
            queryParams.value.zipCide = res,
            queryParams.value.deleteTime = res,
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
        title.value = "添加合作伙伴银行";
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
        getBank(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改合作伙伴银行";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["bankRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateBank(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addBank(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除合作伙伴银行编号为"' + _ids + '"的数据项？').then(function () {
            return delBank(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/bank/export', {
            ...queryParams.value
        }, `bank_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
