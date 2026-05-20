<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入客户信息"
                show-search
                label="客户管理"
                @search="handleQuery"
        >
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:partner:add']"
                >新建商业伙伴
                </el-button
                >
                <el-dropdown
                        v-if="headerMoreHandle.length > 0"
                        trigger="click"
                        style="margin-left: 5px; margin-right: 10px"
                        @command="headerMoreHandleClick"
                >
                    <el-button color="#f1f1f1"
                    >
                        <el-icon size="20">
                            <more-filled/>
                        </el-icon
                        >
                    </el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item
                                    v-for="(item, index) in headerMoreHandle"
                                    :key="index"
                                    :icon="item.icon"
                                    :command="item.type"
                            >{{ item.name }}
                            </el-dropdown-item
                            >
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </template>
            <template v-slot:bottom-ft>
                <AdvancedFilter :title="'高级筛选'" style="margin-right: 20px">
                    <template v-slot:content>
                        <el-form
                                :model="queryParams"
                                ref="queryRef"
                                :inline="true"
                                v-show="showSearch"
                                label-width="68px"
                        >
                            <el-form-item label="公司名称" prop="partnerName">
                                <el-input
                                        v-model="queryParams.partnerName"
                                        placeholder="请输入公司名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司唯一标识SN编号" prop="partnerKey">
                                <el-input
                                        v-model="queryParams.partnerKey"
                                        placeholder="请输入公司唯一标识SN编号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司法人" prop="partnerEntity">
                                <el-input
                                        v-model="queryParams.partnerEntity"
                                        placeholder="请输入公司法人"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="是否供应商" prop="isSupplier">
                                <el-input
                                        v-model="queryParams.isSupplier"
                                        placeholder="请输入是否供应商"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="是否客户" prop="isCustomer">
                                <el-input
                                        v-model="queryParams.isCustomer"
                                        placeholder="请输入是否客户"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司省id" prop="provinceId">
                                <el-input
                                        v-model="queryParams.provinceId"
                                        placeholder="请输入公司省id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司市id" prop="cityId">
                                <el-input
                                        v-model="queryParams.cityId"
                                        placeholder="请输入公司市id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司地区县id" prop="areaId">
                                <el-input
                                        v-model="queryParams.areaId"
                                        placeholder="请输入公司地区县id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="详细地址" prop="detailAddr">
                                <el-input
                                        v-model="queryParams.detailAddr"
                                        placeholder="请输入详细地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="营业执照" prop="partnerLicense">
                                <el-input
                                        v-model="queryParams.partnerLicense"
                                        placeholder="请输入营业执照"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户开票电话" prop="invoiceTel">
                                <el-input
                                        v-model="queryParams.invoiceTel"
                                        placeholder="请输入客户开票电话"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户开票地址" prop="invoiceAddress">
                                <el-input
                                        v-model="queryParams.invoiceAddress"
                                        placeholder="请输入客户开票地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户税号" prop="taxId">
                                <el-input
                                        v-model="queryParams.taxId"
                                        placeholder="请输入客户税号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户开户行" prop="openingBank">
                                <el-input
                                        v-model="queryParams.openingBank"
                                        placeholder="请输入客户开户行"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户银行账号" prop="bankNum">
                                <el-input
                                        v-model="queryParams.bankNum"
                                        placeholder="请输入客户银行账号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item
                                    label="客户联行号(对接银行-银行唯一识别码)"
                                    prop="interbankNum"
                            >
                                <el-input
                                        v-model="queryParams.interbankNum"
                                        placeholder="请输入客户联行号(对接银行-银行唯一识别码)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="注册资金" prop="registerCapital">
                                <el-input
                                        v-model="queryParams.registerCapital"
                                        placeholder="请输入注册资金"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="综合评分" prop="partnerScope">
                                <el-input
                                        v-model="queryParams.partnerScope"
                                        placeholder="请输入综合评分"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="主营商品" prop="mainProduct">
                                <el-input
                                        v-model="queryParams.mainProduct"
                                        placeholder="请输入主营商品"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司性质" prop="partnerNature">
                                <el-input
                                        v-model="queryParams.partnerNature"
                                        placeholder="请输入公司性质"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司信誉" prop="partnerCredit">
                                <el-input
                                        v-model="queryParams.partnerCredit"
                                        placeholder="请输入公司信誉"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司行业" prop="partnerIndustry">
                                <el-input
                                        v-model="queryParams.partnerIndustry"
                                        placeholder="请输入公司行业"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="客户来源" prop="partnerFrom">
                                <el-input
                                        v-model="queryParams.partnerFrom"
                                        placeholder="请输入客户来源"
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
                        </el-form>
                    </template>
                </AdvancedFilter>
                <RefreshView style="margin-right: 20px" @click="resetQuery"></RefreshView>
                <ShowFilter :columns="showColumn"></ShowFilter>
            </template>
        </header-view>
        <el-row :gutter="20" style="margin: 15px 0px">
            <el-col :span="24">
                <el-table
                        v-loading="loading"
                        :data="partnerList"
                        border
                        stripe
                        style="width: 100%;"
                        show-header
                        highlight-current-row
                        @selection-change="handleSelectionChange"
                >
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="公司名称" align="left" fixed prop="partnerName" width="250">
                        <template #default="scope">
                            <a style="color: #0052cc !important; text-overflow:ellipsis; white-space: nowrap; overflow:hidden; width:100%;"
                               :title="scope.row.partnerName">{{ scope.row.partnerName }}</a>
                        </template>
                    </el-table-column>
                    <el-table-column label="客户来源" align="center" prop="partnerFrom" width="120"/>
                    <el-table-column label="手机" align="center" prop="invoice_tel" width="120"/>
                    <el-table-column label="电话" align="center" prop="invoice_tel" width="120"/>
                    <el-table-column label="邮箱" align="center" prop="isSupplier" width="160"/>
                    <el-table-column label="公司性质" align="center" prop="isCustomer" width="160"/>
                    <el-table-column label="公司类型" align="center" prop="isCustomer" width="160"/>
                    <el-table-column label="客户行业" align="center" prop="isCustomer" width="160"/>
                    <el-table-column label="客户标签" align="center" prop="isCustomer" width="160"/>
                    <el-table-column label="综合评分" align="center" prop="isCustomer" width="160"/>
                    <el-table-column label="备注" align="center" prop="isCustomer" width="200"/>
                    <el-table-column label="状态" align="center" prop="status" width="120"/>
                    <el-table-column label="创建时间" align="center" prop="isCustomer" width="160"/>
                    <el-table-column label="创建人" align="center" prop="isCustomer" width="120"/>
                    <el-table-column
                            label="操作"
                            fixed="right"
                            width="180"
                            align="center"
                            class-name="small-padding fixed-width"
                    >
                        <template #default="scope">
                            <el-button
                                    link
                                    type="primary"
                                    icon="Edit"
                                    @click="handleUpdate(scope.row)"
                                    v-hasPermi="['erp:partner:edit']"
                            >修改
                            </el-button
                            >
                            <el-button
                                    link
                                    type="primary"
                                    icon="Delete"
                                    @click="handleDelete(scope.row)"
                                    v-hasPermi="['erp:partner:remove']"
                            >删除
                            </el-button
                            >
                        </template>
                    </el-table-column>
                </el-table>
                <div class="p-contianer">
                    <pagination
                            :page-sizes="[15, 20, 30, 40, 50, 100]"
                            v-show="total > 0"
                            :total="total"
                            v-model:page="queryParams.pageNum"
                            v-model:limit="queryParams.pageSize"
                            @pagination="getList"
                    />
                </div>
            </el-col>
        </el-row>

        <!-- 添加或修改商业伙伴对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="partnerRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司名称" prop="partnerName">
                    <el-input v-model="form.partnerName" placeholder="请输入公司名称"/>
                </el-form-item>
                <el-form-item label="公司唯一标识SN编号" prop="partnerKey">
                    <el-input v-model="form.partnerKey" placeholder="请输入公司唯一标识SN编号"/>
                </el-form-item>
                <el-form-item label="公司法人" prop="partnerEntity">
                    <el-input v-model="form.partnerEntity" placeholder="请输入公司法人"/>
                </el-form-item>
                <el-form-item label="是否供应商" prop="isSupplier">
                    <el-input v-model="form.isSupplier" placeholder="请输入是否供应商"/>
                </el-form-item>
                <el-form-item label="是否客户" prop="isCustomer">
                    <el-input v-model="form.isCustomer" placeholder="请输入是否客户"/>
                </el-form-item>
                <el-form-item label="公司省id" prop="provinceId">
                    <el-input v-model="form.provinceId" placeholder="请输入公司省id"/>
                </el-form-item>
                <el-form-item label="公司市id" prop="cityId">
                    <el-input v-model="form.cityId" placeholder="请输入公司市id"/>
                </el-form-item>
                <el-form-item label="公司地区县id" prop="areaId">
                    <el-input v-model="form.areaId" placeholder="请输入公司地区县id"/>
                </el-form-item>
                <el-form-item label="详细地址" prop="detailAddr">
                    <el-input v-model="form.detailAddr" placeholder="请输入详细地址"/>
                </el-form-item>
                <el-form-item label="营业执照" prop="partnerLicense">
                    <el-input v-model="form.partnerLicense" placeholder="请输入营业执照"/>
                </el-form-item>
                <el-form-item label="客户开票电话" prop="invoiceTel">
                    <el-input v-model="form.invoiceTel" placeholder="请输入客户开票电话"/>
                </el-form-item>
                <el-form-item label="客户开票地址" prop="invoiceAddress">
                    <el-input v-model="form.invoiceAddress" placeholder="请输入客户开票地址"/>
                </el-form-item>
                <el-form-item label="客户税号" prop="taxId">
                    <el-input v-model="form.taxId" placeholder="请输入客户税号"/>
                </el-form-item>
                <el-form-item label="客户开户行" prop="openingBank">
                    <el-input v-model="form.openingBank" placeholder="请输入客户开户行"/>
                </el-form-item>
                <el-form-item label="客户银行账号" prop="bankNum">
                    <el-input v-model="form.bankNum" placeholder="请输入客户银行账号"/>
                </el-form-item>
                <el-form-item label="客户联行号(对接银行-银行唯一识别码)" prop="interbankNum">
                    <el-input
                            v-model="form.interbankNum"
                            placeholder="请输入客户联行号(对接银行-银行唯一识别码)"
                    />
                </el-form-item>
                <el-form-item label="注册资金" prop="registerCapital">
                    <el-input v-model="form.registerCapital" placeholder="请输入注册资金"/>
                </el-form-item>
                <el-form-item label="综合评分" prop="partnerScope">
                    <el-input v-model="form.partnerScope" placeholder="请输入综合评分"/>
                </el-form-item>
                <el-form-item label="主营商品" prop="mainProduct">
                    <el-input v-model="form.mainProduct" placeholder="请输入主营商品"/>
                </el-form-item>
                <el-form-item label="公司性质" prop="partnerNature">
                    <el-input v-model="form.partnerNature" placeholder="请输入公司性质"/>
                </el-form-item>
                <el-form-item label="公司信誉" prop="partnerCredit">
                    <el-input v-model="form.partnerCredit" placeholder="请输入公司信誉"/>
                </el-form-item>
                <el-form-item label="公司行业" prop="partnerIndustry">
                    <el-input v-model="form.partnerIndustry" placeholder="请输入公司行业"/>
                </el-form-item>
                <el-form-item label="客户来源" prop="partnerFrom">
                    <el-input v-model="form.partnerFrom" placeholder="请输入客户来源"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="是否可用(1启用，0停用)" prop="isAvailable">
                    <el-input
                            v-model="form.isAvailable"
                            placeholder="请输入是否可用(1启用，0停用)"
                    />
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

        <Import v-model="isImport"></Import>
    </div>
</template>

<script setup name="Partner">
    import HeaderView from "@/components/HeaderView";
    import AdvancedFilter from "@/components/AdvancedFilter";
    import ShowFilter from "@/components/showFilter";
    import RefreshView from "@/components/RefreshView";
    import Import from "./components/Import.vue";

    import {
        listPartner,
        getPartner,
        delPartner,
        addPartner,
        updatePartner,
    } from "@/api/erp/partner";

    const {proxy} = getCurrentInstance();

    const partnerList = ref([]);
    const open = ref(false);
    const loading = ref(true);
    const showSearch = ref(true);
    const ids = ref([]);
    const single = ref(true);
    const multiple = ref(true);
    const total = ref(0);
    const title = ref("");
    const isImport = ref(false);

    const headerMoreHandle = ref([
        {
            icon: "import",
            name: "导入",
            type: "import",
        },
        {
            icon: "export",
            name: "导出",
            type: "export",
        },
    ]);

    const data = reactive({
        form: {},
        queryParams: {
            pageNum: 1,
            pageSize: 14,
            partnerName: null,
            partnerKey: null,
            partnerEntity: null,
            isSupplier: null,
            isCustomer: null,
            provinceId: null,
            cityId: null,
            areaId: null,
            detailAddr: null,
            partnerLicense: null,
            invoiceTel: null,
            invoiceAddress: null,
            taxId: null,
            openingBank: null,
            bankNum: null,
            interbankNum: null,
            registerCapital: null,
            partnerScope: null,
            partnerType: null,
            mainProduct: null,
            partnerNature: null,
            partnerCredit: null,
            partnerIndustry: null,
            partnerFrom: null,
            status: null,
            isAvailable: null,
            createUid: null,
        },
        rules: {
            partnerName: [{required: true, message: "公司名称不能为空", trigger: "blur"}],
            partnerKey: [
                {required: true, message: "公司唯一标识SN编号不能为空", trigger: "blur"},
            ],
            partnerEntity: [{required: true, message: "公司法人不能为空", trigger: "blur"}],
            isSupplier: [{required: true, message: "是否供应商不能为空", trigger: "blur"}],
            isCustomer: [{required: true, message: "是否客户不能为空", trigger: "blur"}],
            provinceId: [{required: true, message: "公司省id不能为空", trigger: "blur"}],
        },
    });

    const showColumn = ref([
        {label: "公司名称", value: "partnerName"},
        {label: "公司唯一标识SN编号", value: "partnerKey"},
        {label: "公司法人", value: "partnerEntity"},
        {label: "是否供应商", value: "isSupplier"},
        {label: "是否客户", value: "isCustomer"},
        {label: "公司省id", value: "provinceId"},
        {label: "公司市id", value: "cityId"},
        {label: "公司地区县id", value: "areaId"},
        {label: "详细地址", value: "detailAddr"},
        {label: "营业执照", value: "partnerLicense"},
        {label: "客户开票电话", value: "invoiceTel"},
        {label: "客户开票地址", value: "invoiceAddress"},
        {label: "客户税号", value: "taxId"},
        {label: "客户开户行", value: "openingBank"},
        {label: "客户银行账号", value: "bankNum"},
        {label: "客户联行号(对接银行-银行唯一识别码)", value: "interbankNum"},
        {label: "注册资金", value: "registerCapital"},
        {label: "综合评分", value: "partnerScope"},
        {label: "公司类型", value: "partnerType"},
        {label: "主营商品", value: "mainProduct"},
        {label: "公司性质", value: "partnerNature"},
        {label: "公司信誉", value: "partnerCredit"},
        {label: "公司行业", value: "partnerIndustry"},
        {label: "客户来源", value: "partnerFrom"},
        {label: "状态", value: "status"},
        {label: "是否可用(1启用，0停用)", value: "isAvailable"},
        {label: "创建人id", value: "createUid"},
    ]);

    const {queryParams, form, rules} = toRefs(data);

    /** 查询商业伙伴列表 */
    function getList() {
        loading.value = true;
        listPartner(queryParams.value).then((response) => {
            partnerList.value = response.rows;
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
            partnerName: null,
            partnerKey: null,
            partnerEntity: null,
            isSupplier: null,
            isCustomer: null,
            provinceId: null,
            cityId: null,
            areaId: null,
            detailAddr: null,
            partnerLicense: null,
            invoiceTel: null,
            invoiceAddress: null,
            taxId: null,
            openingBank: null,
            bankNum: null,
            interbankNum: null,
            registerCapital: null,
            partnerScope: null,
            partnerType: null,
            mainProduct: null,
            partnerNature: null,
            partnerCredit: null,
            partnerIndustry: null,
            partnerFrom: null,
            remark: null,
            status: null,
            isAvailable: null,
            createTime: null,
            createUid: null,
        };
        proxy.resetForm("partnerRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        (queryParams.value.partnerName = res),
            (queryParams.value.partnerKey = res),
            (queryParams.value.partnerEntity = res),
            (queryParams.value.isSupplier = res),
            (queryParams.value.isCustomer = res),
            (queryParams.value.provinceId = res),
            (queryParams.value.cityId = res),
            (queryParams.value.areaId = res),
            (queryParams.value.detailAddr = res),
            (queryParams.value.partnerLicense = res),
            (queryParams.value.invoiceTel = res),
            (queryParams.value.invoiceAddress = res),
            (queryParams.value.taxId = res),
            (queryParams.value.openingBank = res),
            (queryParams.value.bankNum = res),
            (queryParams.value.interbankNum = res),
            (queryParams.value.registerCapital = res),
            (queryParams.value.partnerScope = res),
            (queryParams.value.partnerType = res),
            (queryParams.value.mainProduct = res),
            (queryParams.value.partnerNature = res),
            (queryParams.value.partnerCredit = res),
            (queryParams.value.partnerIndustry = res),
            (queryParams.value.partnerFrom = res),
            (queryParams.value.status = res),
            (queryParams.value.isAvailable = res),
            (queryParams.value.createUid = res),
            (queryParams.value.pageNum = 1);
        getList();
    }

    /** 重置按钮操作 */
    function resetQuery() {
        proxy.resetForm("queryRef");
        handleQuery();
    }

    // 多选框选中数据
    function handleSelectionChange(selection) {
        ids.value = selection.map((item) => item.id);
        single.value = selection.length != 1;
        multiple.value = !selection.length;
    }

    /** 新增按钮操作 */
    function handleAdd() {
        reset();
        open.value = true;
        title.value = "添加商业伙伴";
    }

    const headerMoreHandleClick = (command) => {
        if (command == "import") {
            //导入
            console.log("导入");
            isImport.value = true;
        } else if (command == "export") {
            //导出
            proxy.download(
                "/erp/partner/export",
                {},
                `user_template_${new Date().getTime()}.xlsx`
            );
            console.log("导出");
        }
    };

    /** 修改按钮操作 */
    function handleUpdate(row) {
        reset();
        const _id = row.id || ids.value;
        getPartner(_id).then((response) => {
            form.value = response.data;
            open.value = true;
            title.value = "修改商业伙伴";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["partnerRef"].validate((valid) => {
            if (valid) {
                if (form.value.id != null) {
                    updatePartner(form.value).then((response) => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addPartner(form.value).then((response) => {
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
        proxy.$modal
            .confirm('是否确认删除商业伙伴编号为"' + _ids + '"的数据项？')
            .then(function () {
                return delPartner(_ids);
            })
            .then(() => {
                getList();
                proxy.$modal.msgSuccess("删除成功");
            })
            .catch(() => {
            });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download(
            "erp/partner/export",
            {
                ...queryParams.value,
            },
            `partner_${new Date().getTime()}.xlsx`
        );
    }

    getList();
</script>
