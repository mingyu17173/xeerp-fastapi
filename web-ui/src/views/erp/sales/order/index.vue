<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入销售订单"
                show-search
                label="销售订单"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['sales:sale:add']">新建销售订单</el-button>
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
                            <el-form-item label="公司父级id" prop="blocId">
                                <el-input
                                        v-model="queryParams.blocId"
                                        placeholder="请输入公司父级id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司id" prop="sellerId">
                                <el-input
                                        v-model="queryParams.sellerId"
                                        placeholder="请输入公司id"
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
                            <el-form-item label="订单日期" prop="saleDate">
                                <el-date-picker clearable
                                                v-model="queryParams.saleDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择订单日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="订单key" prop="saleKey">
                                <el-input
                                        v-model="queryParams.saleKey"
                                        placeholder="请输入订单key"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户id" prop="partnerId">
                                <el-input
                                        v-model="queryParams.partnerId"
                                        placeholder="请输入客户id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="销售代表部门id" prop="departmentId">
                                <el-input
                                        v-model="queryParams.departmentId"
                                        placeholder="请输入销售代表部门id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="销售代表id" prop="workerId">
                                <el-input
                                        v-model="queryParams.workerId"
                                        placeholder="请输入销售代表id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="销售给某部门id" prop="saleDepartmentId">
                                <el-input
                                        v-model="queryParams.saleDepartmentId"
                                        placeholder="请输入销售给某部门id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="订单总金额" prop="totalOrderAmount">
                                <el-input
                                        v-model="queryParams.totalOrderAmount"
                                        placeholder="请输入订单总金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="预收款总金额" prop="totalDepositAmount">
                                <el-input
                                        v-model="queryParams.totalDepositAmount"
                                        placeholder="请输入预收款总金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="已收款总金额" prop="totalReceiveAmount">
                                <el-input
                                        v-model="queryParams.totalReceiveAmount"
                                        placeholder="请输入已收款总金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="下单方式" prop="orderMethod">
                                <el-input
                                        v-model="queryParams.orderMethod"
                                        placeholder="请输入下单方式"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="单位" prop="uom">
                                <el-input
                                        v-model="queryParams.uom"
                                        placeholder="请输入单位"
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
                            <el-form-item label="税率" prop="taxRate">
                                <el-input
                                        v-model="queryParams.taxRate"
                                        placeholder="请输入税率"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="审核确认时间" prop="approvalTime">
                                <el-date-picker clearable
                                                v-model="queryParams.approvalTime"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择审核确认时间">
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
                <el-table v-loading="loading" :data="saleList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="销售单id" align="center" prop="id"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="单据类型id" align="center" prop="docTypeId"/>
                    <el-table-column label="订单日期" align="center" prop="saleDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.saleDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="订单key" align="center" prop="saleKey"/>
                    <el-table-column label="订单状态" align="center" prop="status"/>
                    <el-table-column label="客户id" align="center" prop="partnerId"/>
                    <el-table-column label="销售代表部门id" align="center" prop="departmentId"/>
                    <el-table-column label="销售代表id" align="center" prop="workerId"/>
                    <el-table-column label="销售给某部门id" align="center" prop="saleDepartmentId"/>
                    <el-table-column label="业务类型" align="center" prop="businessType"/>
                    <el-table-column label="支付类型" align="center" prop="payType"/>
                    <el-table-column label="订单总金额" align="center" prop="totalOrderAmount"/>
                    <el-table-column label="预收款总金额" align="center" prop="totalDepositAmount"/>
                    <el-table-column label="已收款总金额" align="center" prop="totalReceiveAmount"/>
                    <el-table-column label="下单方式" align="center" prop="orderMethod"/>
                    <el-table-column label="单位" align="center" prop="uom"/>
                    <el-table-column label="币种" align="center" prop="currency"/>
                    <el-table-column label="币种汇率" align="center" prop="currencyRate"/>
                    <el-table-column label="税率" align="center" prop="taxRate"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="审核确认时间" align="center" prop="approvalTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.approvalTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['sales:sale:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['sales:sale:remove']">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div class="p-contianer">
                    <pagination
                            v-show="total>0"
                            :total="total"
                            v-model:page="queryParams.pageNum"
                            v-model:limit="queryParams.pageSize"
                            @pagination="getList"
                    />
                </div>
            </el-col>
        </el-row>
        <!-- 添加或修改销售订单对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="saleRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="单据类型id" prop="docTypeId">
                    <el-input v-model="form.docTypeId" placeholder="请输入单据类型id"/>
                </el-form-item>
                <el-form-item label="订单日期" prop="saleDate">
                    <el-date-picker clearable
                                    v-model="form.saleDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择订单日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="订单key" prop="saleKey">
                    <el-input v-model="form.saleKey" placeholder="请输入订单key"/>
                </el-form-item>
                <el-form-item label="客户id" prop="partnerId">
                    <el-input v-model="form.partnerId" placeholder="请输入客户id"/>
                </el-form-item>
                <el-form-item label="销售代表部门id" prop="departmentId">
                    <el-input v-model="form.departmentId" placeholder="请输入销售代表部门id"/>
                </el-form-item>
                <el-form-item label="销售代表id" prop="workerId">
                    <el-input v-model="form.workerId" placeholder="请输入销售代表id"/>
                </el-form-item>
                <el-form-item label="销售给某部门id" prop="saleDepartmentId">
                    <el-input v-model="form.saleDepartmentId" placeholder="请输入销售给某部门id"/>
                </el-form-item>
                <el-form-item label="订单总金额" prop="totalOrderAmount">
                    <el-input v-model="form.totalOrderAmount" placeholder="请输入订单总金额"/>
                </el-form-item>
                <el-form-item label="预收款总金额" prop="totalDepositAmount">
                    <el-input v-model="form.totalDepositAmount" placeholder="请输入预收款总金额"/>
                </el-form-item>
                <el-form-item label="已收款总金额" prop="totalReceiveAmount">
                    <el-input v-model="form.totalReceiveAmount" placeholder="请输入已收款总金额"/>
                </el-form-item>
                <el-form-item label="下单方式" prop="orderMethod">
                    <el-input v-model="form.orderMethod" placeholder="请输入下单方式"/>
                </el-form-item>
                <el-form-item label="单位" prop="uom">
                    <el-input v-model="form.uom" placeholder="请输入单位"/>
                </el-form-item>
                <el-form-item label="币种" prop="currency">
                    <el-input v-model="form.currency" placeholder="请输入币种"/>
                </el-form-item>
                <el-form-item label="币种汇率" prop="currencyRate">
                    <el-input v-model="form.currencyRate" placeholder="请输入币种汇率"/>
                </el-form-item>
                <el-form-item label="税率" prop="taxRate">
                    <el-input v-model="form.taxRate" placeholder="请输入税率"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="审核确认时间" prop="approvalTime">
                    <el-date-picker clearable
                                    v-model="form.approvalTime"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择审核确认时间">
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

<script setup name="Sale">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listSale, getSale, delSale, addSale, updateSale} from "@/api/erp/sale";

    const {proxy} = getCurrentInstance();

    const saleList = ref([]);
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
            pageSize: 10,
            blocId: null,
            sellerId: null,
            docTypeId: null,
            saleDate: null,
            saleKey: null,
            status: null,
            partnerId: null,
            departmentId: null,
            workerId: null,
            saleDepartmentId: null,
            businessType: null,
            payType: null,
            totalOrderAmount: null,
            totalDepositAmount: null,
            totalReceiveAmount: null,
            orderMethod: null,
            uom: null,
            currency: null,
            currencyRate: null,
            taxRate: null,
            approvalTime: null,
            createUid: null
        },
        rules: {
            saleDate: [
                {required: true, message: "订单日期不能为空", trigger: "blur"}
            ],
            saleKey: [
                {required: true, message: "订单key不能为空", trigger: "blur"}
            ],
            status: [
                {required: true, message: "订单状态不能为空", trigger: "change"}
            ],
            partnerId: [
                {required: true, message: "客户id不能为空", trigger: "blur"}
            ],
            businessType: [
                {required: true, message: "业务类型不能为空", trigger: "change"}
            ],
            currency: [
                {required: true, message: "币种不能为空", trigger: "blur"}
            ],
            taxRate: [
                {required: true, message: "税率不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司父级id", value: "blocId"},
        {label: "公司id", value: "sellerId"},
        {label: "单据类型id", value: "docTypeId"},
        {label: "订单日期", value: "saleDate"},
        {label: "订单key", value: "saleKey"},
        {label: "订单状态", value: "status"},
        {label: "客户id", value: "partnerId"},
        {label: "销售代表部门id", value: "departmentId"},
        {label: "销售代表id", value: "workerId"},
        {label: "销售给某部门id", value: "saleDepartmentId"},
        {label: "业务类型", value: "businessType"},
        {label: "支付类型", value: "payType"},
        {label: "订单总金额", value: "totalOrderAmount"},
        {label: "预收款总金额", value: "totalDepositAmount"},
        {label: "已收款总金额", value: "totalReceiveAmount"},
        {label: "下单方式（报价生成、采购生成、订单复制、塑米城订单）", value: "orderMethod"},
        {label: "单位", value: "uom"},
        {label: "币种", value: "currency"},
        {label: "币种汇率", value: "currencyRate"},
        {label: "税率", value: "taxRate"},
        {label: "审核确认时间", value: "approvalTime"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询销售订单列表 */
    function getList() {
        loading.value = true;
        listSale(queryParams.value).then(response => {
            saleList.value = response.rows;
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
            blocId: null,
            sellerId: null,
            docTypeId: null,
            saleDate: null,
            saleKey: null,
            status: null,
            partnerId: null,
            departmentId: null,
            workerId: null,
            saleDepartmentId: null,
            businessType: null,
            payType: null,
            totalOrderAmount: null,
            totalDepositAmount: null,
            totalReceiveAmount: null,
            orderMethod: null,
            uom: null,
            currency: null,
            currencyRate: null,
            taxRate: null,
            remark: null,
            approvalTime: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("saleRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.blocId = res,
            queryParams.value.sellerId = res,
            queryParams.value.docTypeId = res,
            queryParams.value.saleDate = res,
            queryParams.value.saleKey = res,
            queryParams.value.status = res,
            queryParams.value.partnerId = res,
            queryParams.value.departmentId = res,
            queryParams.value.workerId = res,
            queryParams.value.saleDepartmentId = res,
            queryParams.value.businessType = res,
            queryParams.value.payType = res,
            queryParams.value.totalOrderAmount = res,
            queryParams.value.totalDepositAmount = res,
            queryParams.value.totalReceiveAmount = res,
            queryParams.value.orderMethod = res,
            queryParams.value.uom = res,
            queryParams.value.currency = res,
            queryParams.value.currencyRate = res,
            queryParams.value.taxRate = res,
            queryParams.value.approvalTime = res,
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
        title.value = "添加销售订单";
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
        getSale(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改销售订单";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["saleRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateSale(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addSale(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除销售订单编号为"' + _ids + '"的数据项？').then(function () {
            return delSale(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('sales/sale/export', {
            ...queryParams.value
        }, `sale_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
