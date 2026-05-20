<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入收款单"
                show-search
                label="收款单"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:receipt:add']">新建收款单</el-button>
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
                            <el-form-item label="公司id" prop="sellerId">
                                <el-input
                                        v-model="queryParams.sellerId"
                                        placeholder="请输入公司id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司父级id" prop="blocId">
                                <el-input
                                        v-model="queryParams.blocId"
                                        placeholder="请输入公司父级id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="单据类型id" prop="docTypeId">
                                <el-input
                                        v-model="queryParams.docTypeId"
                                        placeholder="请输入单据类型id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="收款人ID" prop="receiveWorkerId">
                                <el-input
                                        v-model="queryParams.receiveWorkerId"
                                        placeholder="请输入收款人ID"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="收款日期" prop="payDate">
                                <el-date-picker clearable
                                                v-model="queryParams.payDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择收款日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="销售单id" prop="saleId">
                                <el-input
                                        v-model="queryParams.saleId"
                                        placeholder="请输入销售单id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="销售单明细id" prop="saleDtlId">
                                <el-input
                                        v-model="queryParams.saleDtlId"
                                        placeholder="请输入销售单明细id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="收款金额" prop="amount">
                                <el-input
                                        v-model="queryParams.amount"
                                        placeholder="请输入收款金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
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
                            <el-form-item label="银行id" prop="sellerBankId">
                                <el-input
                                        v-model="queryParams.sellerBankId"
                                        placeholder="请输入银行id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户公司名称" prop="partnerName">
                                <el-input
                                        v-model="queryParams.partnerName"
                                        placeholder="请输入客户公司名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="收款单号" prop="paymentKey">
                                <el-input
                                        v-model="queryParams.paymentKey"
                                        placeholder="请输入收款单号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="币种" prop="currency">
                                <el-input
                                        v-model="queryParams.currency"
                                        placeholder="请输入币种"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="币种汇率" prop="currencyRate">
                                <el-input
                                        v-model="queryParams.currencyRate"
                                        placeholder="请输入币种汇率"
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
                <el-table v-loading="loading" :data="receiptList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="收款单id" align="center" prop="id"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="单据类型id" align="center" prop="docTypeId"/>
                    <el-table-column label="收款人ID" align="center" prop="receiveWorkerId"/>
                    <el-table-column label="收款日期" align="center" prop="payDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.payDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="销售单id" align="center" prop="saleId"/>
                    <el-table-column label="销售单明细id" align="center" prop="saleDtlId"/>
                    <el-table-column label="收退款类型(1：收款，2：退款)" align="center" prop="collectionRefundType"/>
                    <el-table-column label="收款金额" align="center" prop="amount"/>
                    <el-table-column label="银行名称" align="center" prop="bankName"/>
                    <el-table-column label="银行账号" align="center" prop="bankAccount"/>
                    <el-table-column label="银行id" align="center" prop="sellerBankId"/>
                    <el-table-column label="客户公司名称" align="center" prop="partnerName"/>
                    <el-table-column label="收款单号" align="center" prop="paymentKey"/>
                    <el-table-column label="币种" align="center" prop="currency"/>
                    <el-table-column label="币种汇率" align="center" prop="currencyRate"/>
                    <el-table-column label="状态" align="center" prop="status"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:receipt:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:receipt:remove']">删除
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
        <!-- 添加或修改收款单对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="receiptRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="单据类型id" prop="docTypeId">
                    <el-input v-model="form.docTypeId" placeholder="请输入单据类型id"/>
                </el-form-item>
                <el-form-item label="收款人ID" prop="receiveWorkerId">
                    <el-input v-model="form.receiveWorkerId" placeholder="请输入收款人ID"/>
                </el-form-item>
                <el-form-item label="收款日期" prop="payDate">
                    <el-date-picker clearable
                                    v-model="form.payDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择收款日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="销售单id" prop="saleId">
                    <el-input v-model="form.saleId" placeholder="请输入销售单id"/>
                </el-form-item>
                <el-form-item label="销售单明细id" prop="saleDtlId">
                    <el-input v-model="form.saleDtlId" placeholder="请输入销售单明细id"/>
                </el-form-item>
                <el-form-item label="收款金额" prop="amount">
                    <el-input v-model="form.amount" placeholder="请输入收款金额"/>
                </el-form-item>
                <el-form-item label="银行名称" prop="bankName">
                    <el-input v-model="form.bankName" placeholder="请输入银行名称"/>
                </el-form-item>
                <el-form-item label="银行账号" prop="bankAccount">
                    <el-input v-model="form.bankAccount" placeholder="请输入银行账号"/>
                </el-form-item>
                <el-form-item label="银行id" prop="sellerBankId">
                    <el-input v-model="form.sellerBankId" placeholder="请输入银行id"/>
                </el-form-item>
                <el-form-item label="客户公司名称" prop="partnerName">
                    <el-input v-model="form.partnerName" placeholder="请输入客户公司名称"/>
                </el-form-item>
                <el-form-item label="收款单号" prop="paymentKey">
                    <el-input v-model="form.paymentKey" placeholder="请输入收款单号"/>
                </el-form-item>
                <el-form-item label="币种" prop="currency">
                    <el-input v-model="form.currency" placeholder="请输入币种"/>
                </el-form-item>
                <el-form-item label="币种汇率" prop="currencyRate">
                    <el-input v-model="form.currencyRate" placeholder="请输入币种汇率"/>
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

<script setup name="Receipt">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listReceipt, getReceipt, delReceipt, addReceipt, updateReceipt} from "@/api/erp/receipt";

    const {proxy} = getCurrentInstance();

    const receiptList = ref([]);
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
            sellerId: null,
            blocId: null,
            docTypeId: null,
            receiveWorkerId: null,
            payDate: null,
            saleId: null,
            saleDtlId: null,
            collectionRefundType: null,
            amount: null,
            bankName: null,
            bankAccount: null,
            sellerBankId: null,
            partnerName: null,
            paymentKey: null,
            currency: null,
            currencyRate: null,
            status: null,
            createUid: null
        },
        rules: {
            saleId: [
                {required: true, message: "销售单id不能为空", trigger: "blur"}
            ],
            saleDtlId: [
                {required: true, message: "销售单明细id不能为空", trigger: "blur"}
            ],
            currency: [
                {required: true, message: "币种不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司id", value: "sellerId"},
        {label: "公司父级id", value: "blocId"},
        {label: "单据类型id", value: "docTypeId"},
        {label: "收款人ID", value: "receiveWorkerId"},
        {label: "收款日期", value: "payDate"},
        {label: "销售单id", value: "saleId"},
        {label: "销售单明细id", value: "saleDtlId"},
        {label: "收退款类型(1：收款，2：退款)", value: "collectionRefundType"},
        {label: "收款金额", value: "amount"},
        {label: "银行名称", value: "bankName"},
        {label: "银行账号", value: "bankAccount"},
        {label: "银行id", value: "sellerBankId"},
        {label: "客户公司名称", value: "partnerName"},
        {label: "收款单号", value: "paymentKey"},
        {label: "币种", value: "currency"},
        {label: "币种汇率", value: "currencyRate"},
        {label: "状态", value: "status"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询收款单列表 */
    function getList() {
        loading.value = true;
        listReceipt(queryParams.value).then(response => {
            receiptList.value = response.rows;
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
            sellerId: null,
            blocId: null,
            docTypeId: null,
            receiveWorkerId: null,
            payDate: null,
            saleId: null,
            saleDtlId: null,
            collectionRefundType: null,
            amount: null,
            bankName: null,
            bankAccount: null,
            sellerBankId: null,
            partnerName: null,
            paymentKey: null,
            currency: null,
            currencyRate: null,
            status: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("receiptRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.sellerId = res,
            queryParams.value.blocId = res,
            queryParams.value.docTypeId = res,
            queryParams.value.receiveWorkerId = res,
            queryParams.value.payDate = res,
            queryParams.value.saleId = res,
            queryParams.value.saleDtlId = res,
            queryParams.value.collectionRefundType = res,
            queryParams.value.amount = res,
            queryParams.value.bankName = res,
            queryParams.value.bankAccount = res,
            queryParams.value.sellerBankId = res,
            queryParams.value.partnerName = res,
            queryParams.value.paymentKey = res,
            queryParams.value.currency = res,
            queryParams.value.currencyRate = res,
            queryParams.value.status = res,
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
        title.value = "添加收款单";
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
        getReceipt(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改收款单";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["receiptRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateReceipt(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addReceipt(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除收款单编号为"' + _ids + '"的数据项？').then(function () {
            return delReceipt(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/receipt/export', {
            ...queryParams.value
        }, `receipt_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
