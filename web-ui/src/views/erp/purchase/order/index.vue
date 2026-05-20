<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入采购单主"
                show-search
                label="采购单主"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:purchase:add']">新建采购单主</el-button>
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
                            <el-form-item label="订单日期" prop="purchaseDate">
                                <el-date-picker clearable
                                                v-model="queryParams.purchaseDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择订单日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="订单key" prop="purchaseKey">
                                <el-input
                                        v-model="queryParams.purchaseKey"
                                        placeholder="请输入订单key"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购给某部门id" prop="purchaseDepartmentId">
                                <el-input
                                        v-model="queryParams.purchaseDepartmentId"
                                        placeholder="请输入采购给某部门id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购代表部门id" prop="departmentId">
                                <el-input
                                        v-model="queryParams.departmentId"
                                        placeholder="请输入采购代表部门id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购代表id" prop="workerId">
                                <el-input
                                        v-model="queryParams.workerId"
                                        placeholder="请输入采购代表id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="供应商id" prop="partnerId">
                                <el-input
                                        v-model="queryParams.partnerId"
                                        placeholder="请输入供应商id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="结算方式(用于外币采购)" prop="settlementMethod">
                                <el-input
                                        v-model="queryParams.settlementMethod"
                                        placeholder="请输入结算方式(用于外币采购)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="联系人姓名" prop="contactsName">
                                <el-input
                                        v-model="queryParams.contactsName"
                                        placeholder="请输入联系人姓名"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="联系人手机/电话" prop="contactsTel">
                                <el-input
                                        v-model="queryParams.contactsTel"
                                        placeholder="请输入联系人手机/电话"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="收款银行id" prop="bankId">
                                <el-input
                                        v-model="queryParams.bankId"
                                        placeholder="请输入收款银行id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="实物仓库id" prop="realWarehouseId">
                                <el-input
                                        v-model="queryParams.realWarehouseId"
                                        placeholder="请输入实物仓库id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="城市id(仓库所在城市)" prop="regionId">
                                <el-input
                                        v-model="queryParams.regionId"
                                        placeholder="请输入城市id(仓库所在城市)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="城市名称(仓库所在城市)" prop="regionName">
                                <el-input
                                        v-model="queryParams.regionName"
                                        placeholder="请输入城市名称(仓库所在城市)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="仓库地点(仓库所在地点)" prop="locationAddr">
                                <el-input
                                        v-model="queryParams.locationAddr"
                                        placeholder="请输入仓库地点(仓库所在地点)"
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
                            <el-form-item label="订单总金额" prop="totalOrderAmount">
                                <el-input
                                        v-model="queryParams.totalOrderAmount"
                                        placeholder="请输入订单总金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="预付款总金额" prop="totalDepositAmount">
                                <el-input
                                        v-model="queryParams.totalDepositAmount"
                                        placeholder="请输入预付款总金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="已支付总金额" prop="totalPayAmount">
                                <el-input
                                        v-model="queryParams.totalPayAmount"
                                        placeholder="请输入已支付总金额"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="协议编号(用于外币采购)" prop="contractNo">
                                <el-input
                                        v-model="queryParams.contractNo"
                                        placeholder="请输入协议编号(用于外币采购)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="协议日期(用于外币采购)" prop="contractTime">
                                <el-date-picker clearable
                                                v-model="queryParams.contractTime"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择协议日期(用于外币采购)">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="代理开证公司(用于外币采购)" prop="agencyCompanyId">
                                <el-input
                                        v-model="queryParams.agencyCompanyId"
                                        placeholder="请输入代理开证公司(用于外币采购)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="代理费(0无 1有)" prop="agencyFees">
                                <el-input
                                        v-model="queryParams.agencyFees"
                                        placeholder="请输入代理费(0无 1有)"
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
                <el-table v-loading="loading" :data="purchaseList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label=" 采购单id" align="center" prop="id"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="单据类型id" align="center" prop="docTypeId"/>
                    <el-table-column label="订单日期" align="center" prop="purchaseDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.purchaseDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="订单key" align="center" prop="purchaseKey"/>
                    <el-table-column label="订单状态" align="center" prop="status"/>
                    <el-table-column label="采购给某部门id" align="center" prop="purchaseDepartmentId"/>
                    <el-table-column label="采购代表部门id" align="center" prop="departmentId"/>
                    <el-table-column label="采购代表id" align="center" prop="workerId"/>
                    <el-table-column label="供应商id" align="center" prop="partnerId"/>
                    <el-table-column label="业务类型" align="center" prop="businessType"/>
                    <el-table-column label="结算方式(用于外币采购)" align="center" prop="settlementMethod"/>
                    <el-table-column label="联系人姓名" align="center" prop="contactsName"/>
                    <el-table-column label="联系人手机/电话" align="center" prop="contactsTel"/>
                    <el-table-column label="收款银行id" align="center" prop="bankId"/>
                    <el-table-column label="实物仓库id" align="center" prop="realWarehouseId"/>
                    <el-table-column label="城市id(仓库所在城市)" align="center" prop="regionId"/>
                    <el-table-column label="城市名称(仓库所在城市)" align="center" prop="regionName"/>
                    <el-table-column label="仓库地点(仓库所在地点)" align="center" prop="locationAddr"/>
                    <el-table-column label="单位" align="center" prop="uom"/>
                    <el-table-column label="币种" align="center" prop="currency"/>
                    <el-table-column label="币种汇率" align="center" prop="currencyRate"/>
                    <el-table-column label="税率" align="center" prop="taxRate"/>
                    <el-table-column label="订单总金额" align="center" prop="totalOrderAmount"/>
                    <el-table-column label="预付款总金额" align="center" prop="totalDepositAmount"/>
                    <el-table-column label="已支付总金额" align="center" prop="totalPayAmount"/>
                    <el-table-column label="协议编号(用于外币采购)" align="center" prop="contractNo"/>
                    <el-table-column label="协议日期(用于外币采购)" align="center" prop="contractTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.contractTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="代理开证公司(用于外币采购)" align="center" prop="agencyCompanyId"/>
                    <el-table-column label="代理费(0无 1有)" align="center" prop="agencyFees"/>
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
                                       v-hasPermi="['erp:purchase:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:purchase:remove']">删除
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
        <!-- 添加或修改采购单主对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="purchaseRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="单据类型id" prop="docTypeId">
                    <el-input v-model="form.docTypeId" placeholder="请输入单据类型id"/>
                </el-form-item>
                <el-form-item label="订单日期" prop="purchaseDate">
                    <el-date-picker clearable
                                    v-model="form.purchaseDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择订单日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="订单key" prop="purchaseKey">
                    <el-input v-model="form.purchaseKey" placeholder="请输入订单key"/>
                </el-form-item>
                <el-form-item label="采购给某部门id" prop="purchaseDepartmentId">
                    <el-input v-model="form.purchaseDepartmentId" placeholder="请输入采购给某部门id"/>
                </el-form-item>
                <el-form-item label="采购代表部门id" prop="departmentId">
                    <el-input v-model="form.departmentId" placeholder="请输入采购代表部门id"/>
                </el-form-item>
                <el-form-item label="采购代表id" prop="workerId">
                    <el-input v-model="form.workerId" placeholder="请输入采购代表id"/>
                </el-form-item>
                <el-form-item label="供应商id" prop="partnerId">
                    <el-input v-model="form.partnerId" placeholder="请输入供应商id"/>
                </el-form-item>
                <el-form-item label="结算方式(用于外币采购)" prop="settlementMethod">
                    <el-input v-model="form.settlementMethod" placeholder="请输入结算方式(用于外币采购)"/>
                </el-form-item>
                <el-form-item label="联系人姓名" prop="contactsName">
                    <el-input v-model="form.contactsName" placeholder="请输入联系人姓名"/>
                </el-form-item>
                <el-form-item label="联系人手机/电话" prop="contactsTel">
                    <el-input v-model="form.contactsTel" placeholder="请输入联系人手机/电话"/>
                </el-form-item>
                <el-form-item label="收款银行id" prop="bankId">
                    <el-input v-model="form.bankId" placeholder="请输入收款银行id"/>
                </el-form-item>
                <el-form-item label="实物仓库id" prop="realWarehouseId">
                    <el-input v-model="form.realWarehouseId" placeholder="请输入实物仓库id"/>
                </el-form-item>
                <el-form-item label="城市id(仓库所在城市)" prop="regionId">
                    <el-input v-model="form.regionId" placeholder="请输入城市id(仓库所在城市)"/>
                </el-form-item>
                <el-form-item label="城市名称(仓库所在城市)" prop="regionName">
                    <el-input v-model="form.regionName" placeholder="请输入城市名称(仓库所在城市)"/>
                </el-form-item>
                <el-form-item label="仓库地点(仓库所在地点)" prop="locationAddr">
                    <el-input v-model="form.locationAddr" placeholder="请输入仓库地点(仓库所在地点)"/>
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
                <el-form-item label="订单总金额" prop="totalOrderAmount">
                    <el-input v-model="form.totalOrderAmount" placeholder="请输入订单总金额"/>
                </el-form-item>
                <el-form-item label="预付款总金额" prop="totalDepositAmount">
                    <el-input v-model="form.totalDepositAmount" placeholder="请输入预付款总金额"/>
                </el-form-item>
                <el-form-item label="已支付总金额" prop="totalPayAmount">
                    <el-input v-model="form.totalPayAmount" placeholder="请输入已支付总金额"/>
                </el-form-item>
                <el-form-item label="协议编号(用于外币采购)" prop="contractNo">
                    <el-input v-model="form.contractNo" placeholder="请输入协议编号(用于外币采购)"/>
                </el-form-item>
                <el-form-item label="协议日期(用于外币采购)" prop="contractTime">
                    <el-date-picker clearable
                                    v-model="form.contractTime"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择协议日期(用于外币采购)">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="代理开证公司(用于外币采购)" prop="agencyCompanyId">
                    <el-input v-model="form.agencyCompanyId" placeholder="请输入代理开证公司(用于外币采购)"/>
                </el-form-item>
                <el-form-item label="代理费(0无 1有)" prop="agencyFees">
                    <el-input v-model="form.agencyFees" placeholder="请输入代理费(0无 1有)"/>
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

<script setup name="Purchase">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listPurchase, getPurchase, delPurchase, addPurchase, updatePurchase} from "@/api/erp/purchase";

    const {proxy} = getCurrentInstance();

    const purchaseList = ref([]);
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
            blocId: null,
            sellerId: null,
            docTypeId: null,
            purchaseDate: null,
            purchaseKey: null,
            status: null,
            purchaseDepartmentId: null,
            departmentId: null,
            workerId: null,
            partnerId: null,
            businessType: null,
            settlementMethod: null,
            contactsName: null,
            contactsTel: null,
            bankId: null,
            realWarehouseId: null,
            regionId: null,
            regionName: null,
            locationAddr: null,
            uom: null,
            currency: null,
            currencyRate: null,
            taxRate: null,
            totalOrderAmount: null,
            totalDepositAmount: null,
            totalPayAmount: null,
            contractNo: null,
            contractTime: null,
            agencyCompanyId: null,
            agencyFees: null,
            approvalTime: null,
            createUid: null
        },
        rules: {
            purchaseKey: [
                {required: true, message: "订单key不能为空", trigger: "blur"}
            ],
            status: [
                {required: true, message: "订单状态不能为空", trigger: "change"}
            ],
            partnerId: [
                {required: true, message: "供应商id不能为空", trigger: "blur"}
            ],
            businessType: [
                {required: true, message: "业务类型不能为空", trigger: "change"}
            ],
            contactsName: [
                {required: true, message: "联系人姓名不能为空", trigger: "blur"}
            ],
            contactsTel: [
                {required: true, message: "联系人手机/电话不能为空", trigger: "blur"}
            ],
            regionName: [
                {required: true, message: "城市名称(仓库所在城市)不能为空", trigger: "blur"}
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
        {label: "订单日期", value: "purchaseDate"},
        {label: "订单key", value: "purchaseKey"},
        {label: "订单状态", value: "status"},
        {label: "采购给某部门id", value: "purchaseDepartmentId"},
        {label: "采购代表部门id", value: "departmentId"},
        {label: "采购代表id", value: "workerId"},
        {label: "供应商id", value: "partnerId"},
        {label: "业务类型", value: "businessType"},
        {label: "结算方式(用于外币采购)", value: "settlementMethod"},
        {label: "联系人姓名", value: "contactsName"},
        {label: "联系人手机/电话", value: "contactsTel"},
        {label: "收款银行id", value: "bankId"},
        {label: "实物仓库id", value: "realWarehouseId"},
        {label: "城市id(仓库所在城市)", value: "regionId"},
        {label: "城市名称(仓库所在城市)", value: "regionName"},
        {label: "仓库地点(仓库所在地点)", value: "locationAddr"},
        {label: "单位", value: "uom"},
        {label: "币种", value: "currency"},
        {label: "币种汇率", value: "currencyRate"},
        {label: "税率", value: "taxRate"},
        {label: "订单总金额", value: "totalOrderAmount"},
        {label: "预付款总金额", value: "totalDepositAmount"},
        {label: "已支付总金额", value: "totalPayAmount"},
        {label: "协议编号(用于外币采购)", value: "contractNo"},
        {label: "协议日期(用于外币采购)", value: "contractTime"},
        {label: "代理开证公司(用于外币采购)", value: "agencyCompanyId"},
        {label: "代理费(0无 1有)", value: "agencyFees"},
        {label: "审核确认时间", value: "approvalTime"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询采购单主列表 */
    function getList() {
        loading.value = true;
        listPurchase(queryParams.value).then(response => {
            purchaseList.value = response.rows;
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
            purchaseDate: null,
            purchaseKey: null,
            status: null,
            purchaseDepartmentId: null,
            departmentId: null,
            workerId: null,
            partnerId: null,
            businessType: null,
            settlementMethod: null,
            contactsName: null,
            contactsTel: null,
            bankId: null,
            realWarehouseId: null,
            regionId: null,
            regionName: null,
            locationAddr: null,
            uom: null,
            currency: null,
            currencyRate: null,
            taxRate: null,
            totalOrderAmount: null,
            totalDepositAmount: null,
            totalPayAmount: null,
            contractNo: null,
            contractTime: null,
            agencyCompanyId: null,
            agencyFees: null,
            remark: null,
            approvalTime: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("purchaseRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.blocId = res,
            queryParams.value.sellerId = res,
            queryParams.value.docTypeId = res,
            queryParams.value.purchaseDate = res,
            queryParams.value.purchaseKey = res,
            queryParams.value.status = res,
            queryParams.value.purchaseDepartmentId = res,
            queryParams.value.departmentId = res,
            queryParams.value.workerId = res,
            queryParams.value.partnerId = res,
            queryParams.value.businessType = res,
            queryParams.value.settlementMethod = res,
            queryParams.value.contactsName = res,
            queryParams.value.contactsTel = res,
            queryParams.value.bankId = res,
            queryParams.value.realWarehouseId = res,
            queryParams.value.regionId = res,
            queryParams.value.regionName = res,
            queryParams.value.locationAddr = res,
            queryParams.value.uom = res,
            queryParams.value.currency = res,
            queryParams.value.currencyRate = res,
            queryParams.value.taxRate = res,
            queryParams.value.totalOrderAmount = res,
            queryParams.value.totalDepositAmount = res,
            queryParams.value.totalPayAmount = res,
            queryParams.value.contractNo = res,
            queryParams.value.contractTime = res,
            queryParams.value.agencyCompanyId = res,
            queryParams.value.agencyFees = res,
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
        title.value = "添加采购单主";
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
        getPurchase(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改采购单主";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["purchaseRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updatePurchase(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addPurchase(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除采购单主编号为"' + _ids + '"的数据项？').then(function () {
            return delPurchase(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/purchase/export', {
            ...queryParams.value
        }, `purchase_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
