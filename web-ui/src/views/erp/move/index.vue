<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入调拨单"
                show-search
                label="调拨单"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:move:add']">新建调拨单</el-button>
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
                            <el-form-item label="调拨单编号" prop="moveNo">
                                <el-input
                                        v-model="queryParams.moveNo"
                                        placeholder="请输入调拨单编号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="调拨单日期" prop="moveDate">
                                <el-date-picker clearable
                                                v-model="queryParams.moveDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择调拨单日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="业务员部门id" prop="departmentId">
                                <el-input
                                        v-model="queryParams.departmentId"
                                        placeholder="请输入业务员部门id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="业务员id" prop="workerId">
                                <el-input
                                        v-model="queryParams.workerId"
                                        placeholder="请输入业务员id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="合作伙伴" prop="partnerId">
                                <el-input
                                        v-model="queryParams.partnerId"
                                        placeholder="请输入合作伙伴"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="交货日期/提货日期" prop="stockDate">
                                <el-date-picker clearable
                                                v-model="queryParams.stockDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择交货日期/提货日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="审核确认时间" prop="approvalTime">
                                <el-date-picker clearable
                                                v-model="queryParams.approvalTime"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择审核确认时间">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="单位" prop="uom">
                                <el-input
                                        v-model="queryParams.uom"
                                        placeholder="请输入单位"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购库存id" prop="stockVirtualId">
                                <el-input
                                        v-model="queryParams.stockVirtualId"
                                        placeholder="请输入采购库存id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购单id" prop="purchaseId">
                                <el-input
                                        v-model="queryParams.purchaseId"
                                        placeholder="请输入采购单id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购单明细id" prop="purchaseDtlId">
                                <el-input
                                        v-model="queryParams.purchaseDtlId"
                                        placeholder="请输入采购单明细id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="采购单据号" prop="purchaseKey">
                                <el-input
                                        v-model="queryParams.purchaseKey"
                                        placeholder="请输入采购单据号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="虚拟仓库(调出仓库)" prop="warehouseFromId">
                                <el-input
                                        v-model="queryParams.warehouseFromId"
                                        placeholder="请输入虚拟仓库(调出仓库)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="虚拟仓位(调出仓位)" prop="locationFromId">
                                <el-input
                                        v-model="queryParams.locationFromId"
                                        placeholder="请输入虚拟仓位(调出仓位)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="目标虚拟仓库(调入仓库)" prop="warehouseToId">
                                <el-input
                                        v-model="queryParams.warehouseToId"
                                        placeholder="请输入目标虚拟仓库(调入仓库)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="目标虚拟仓位(调入仓位)" prop="locationToId">
                                <el-input
                                        v-model="queryParams.locationToId"
                                        placeholder="请输入目标虚拟仓位(调入仓位)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="产品id" prop="productId">
                                <el-input
                                        v-model="queryParams.productId"
                                        placeholder="请输入产品id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="数量" prop="num">
                                <el-input
                                        v-model="queryParams.num"
                                        placeholder="请输入数量"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="单价(未税)" prop="priceUntax">
                                <el-input
                                        v-model="queryParams.priceUntax"
                                        placeholder="请输入单价(未税)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="金额(未税)" prop="amountUntax">
                                <el-input
                                        v-model="queryParams.amountUntax"
                                        placeholder="请输入金额(未税)"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="含税单价" prop="price">
                                <el-input
                                        v-model="queryParams.price"
                                        placeholder="请输入含税单价"
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
                <el-table v-loading="loading" :data="moveList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="调拨单id" align="center" prop="id"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="单据类型id" align="center" prop="docTypeId"/>
                    <el-table-column label="调拨单编号" align="center" prop="moveNo"/>
                    <el-table-column label="调拨单日期" align="center" prop="moveDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.moveDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="业务员部门id" align="center" prop="departmentId"/>
                    <el-table-column label="业务员id" align="center" prop="workerId"/>
                    <el-table-column label="合作伙伴" align="center" prop="partnerId"/>
                    <el-table-column label="交货日期/提货日期" align="center" prop="stockDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.stockDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="状态(1待审核 2已审核 -1作废)" align="center" prop="status"/>
                    <el-table-column label="审核确认时间" align="center" prop="approvalTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.approvalTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="单位" align="center" prop="uom"/>
                    <el-table-column label="采购库存id" align="center" prop="stockVirtualId"/>
                    <el-table-column label="采购单id" align="center" prop="purchaseId"/>
                    <el-table-column label="采购单明细id" align="center" prop="purchaseDtlId"/>
                    <el-table-column label="采购单据号" align="center" prop="purchaseKey"/>
                    <el-table-column label="虚拟仓库(调出仓库)" align="center" prop="warehouseFromId"/>
                    <el-table-column label="虚拟仓位(调出仓位)" align="center" prop="locationFromId"/>
                    <el-table-column label="目标虚拟仓库(调入仓库)" align="center" prop="warehouseToId"/>
                    <el-table-column label="目标虚拟仓位(调入仓位)" align="center" prop="locationToId"/>
                    <el-table-column label="产品id" align="center" prop="productId"/>
                    <el-table-column label="数量" align="center" prop="num"/>
                    <el-table-column label="单价(未税)" align="center" prop="priceUntax"/>
                    <el-table-column label="金额(未税)" align="center" prop="amountUntax"/>
                    <el-table-column label="含税单价" align="center" prop="price"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:move:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:move:remove']">删除
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
        <!-- 添加或修改调拨单对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="moveRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="单据类型id" prop="docTypeId">
                    <el-input v-model="form.docTypeId" placeholder="请输入单据类型id"/>
                </el-form-item>
                <el-form-item label="调拨单编号" prop="moveNo">
                    <el-input v-model="form.moveNo" placeholder="请输入调拨单编号"/>
                </el-form-item>
                <el-form-item label="调拨单日期" prop="moveDate">
                    <el-date-picker clearable
                                    v-model="form.moveDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择调拨单日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="业务员部门id" prop="departmentId">
                    <el-input v-model="form.departmentId" placeholder="请输入业务员部门id"/>
                </el-form-item>
                <el-form-item label="业务员id" prop="workerId">
                    <el-input v-model="form.workerId" placeholder="请输入业务员id"/>
                </el-form-item>
                <el-form-item label="合作伙伴" prop="partnerId">
                    <el-input v-model="form.partnerId" placeholder="请输入合作伙伴"/>
                </el-form-item>
                <el-form-item label="交货日期/提货日期" prop="stockDate">
                    <el-date-picker clearable
                                    v-model="form.stockDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择交货日期/提货日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="审核确认时间" prop="approvalTime">
                    <el-date-picker clearable
                                    v-model="form.approvalTime"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择审核确认时间">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="单位" prop="uom">
                    <el-input v-model="form.uom" placeholder="请输入单位"/>
                </el-form-item>
                <el-form-item label="采购库存id" prop="stockVirtualId">
                    <el-input v-model="form.stockVirtualId" placeholder="请输入采购库存id"/>
                </el-form-item>
                <el-form-item label="采购单id" prop="purchaseId">
                    <el-input v-model="form.purchaseId" placeholder="请输入采购单id"/>
                </el-form-item>
                <el-form-item label="采购单明细id" prop="purchaseDtlId">
                    <el-input v-model="form.purchaseDtlId" placeholder="请输入采购单明细id"/>
                </el-form-item>
                <el-form-item label="采购单据号" prop="purchaseKey">
                    <el-input v-model="form.purchaseKey" placeholder="请输入采购单据号"/>
                </el-form-item>
                <el-form-item label="虚拟仓库(调出仓库)" prop="warehouseFromId">
                    <el-input v-model="form.warehouseFromId" placeholder="请输入虚拟仓库(调出仓库)"/>
                </el-form-item>
                <el-form-item label="虚拟仓位(调出仓位)" prop="locationFromId">
                    <el-input v-model="form.locationFromId" placeholder="请输入虚拟仓位(调出仓位)"/>
                </el-form-item>
                <el-form-item label="目标虚拟仓库(调入仓库)" prop="warehouseToId">
                    <el-input v-model="form.warehouseToId" placeholder="请输入目标虚拟仓库(调入仓库)"/>
                </el-form-item>
                <el-form-item label="目标虚拟仓位(调入仓位)" prop="locationToId">
                    <el-input v-model="form.locationToId" placeholder="请输入目标虚拟仓位(调入仓位)"/>
                </el-form-item>
                <el-form-item label="产品id" prop="productId">
                    <el-input v-model="form.productId" placeholder="请输入产品id"/>
                </el-form-item>
                <el-form-item label="数量" prop="num">
                    <el-input v-model="form.num" placeholder="请输入数量"/>
                </el-form-item>
                <el-form-item label="单价(未税)" prop="priceUntax">
                    <el-input v-model="form.priceUntax" placeholder="请输入单价(未税)"/>
                </el-form-item>
                <el-form-item label="金额(未税)" prop="amountUntax">
                    <el-input v-model="form.amountUntax" placeholder="请输入金额(未税)"/>
                </el-form-item>
                <el-form-item label="含税单价" prop="price">
                    <el-input v-model="form.price" placeholder="请输入含税单价"/>
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

<script setup name="Move">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listMove, getMove, delMove, addMove, updateMove} from "@/api/erp/move";

    const {proxy} = getCurrentInstance();

    const moveList = ref([]);
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
            moveNo: null,
            moveDate: null,
            departmentId: null,
            workerId: null,
            partnerId: null,
            stockDate: null,
            status: null,
            approvalTime: null,
            uom: null,
            stockVirtualId: null,
            purchaseId: null,
            purchaseDtlId: null,
            purchaseKey: null,
            warehouseFromId: null,
            locationFromId: null,
            warehouseToId: null,
            locationToId: null,
            productId: null,
            num: null,
            priceUntax: null,
            amountUntax: null,
            price: null,
            createUid: null
        },
        rules: {
            moveNo: [
                {required: true, message: "调拨单编号不能为空", trigger: "blur"}
            ],
            moveDate: [
                {required: true, message: "调拨单日期不能为空", trigger: "blur"}
            ],
            partnerId: [
                {required: true, message: "合作伙伴不能为空", trigger: "blur"}
            ],
            status: [
                {required: true, message: "状态(1待审核 2已审核 -1作废)不能为空", trigger: "change"}
            ],
            stockVirtualId: [
                {required: true, message: "采购库存id不能为空", trigger: "blur"}
            ],
            purchaseId: [
                {required: true, message: "采购单id不能为空", trigger: "blur"}
            ],
            purchaseDtlId: [
                {required: true, message: "采购单明细id不能为空", trigger: "blur"}
            ],
            productId: [
                {required: true, message: "产品id不能为空", trigger: "blur"}
            ],
            num: [
                {required: true, message: "数量不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司父级id", value: "blocId"},
        {label: "公司id", value: "sellerId"},
        {label: "单据类型id", value: "docTypeId"},
        {label: "调拨单编号", value: "moveNo"},
        {label: "调拨单日期", value: "moveDate"},
        {label: "业务员部门id", value: "departmentId"},
        {label: "业务员id", value: "workerId"},
        {label: "合作伙伴", value: "partnerId"},
        {label: "交货日期/提货日期", value: "stockDate"},
        {label: "状态(1待审核 2已审核 -1作废)", value: "status"},
        {label: "审核确认时间", value: "approvalTime"},
        {label: "单位", value: "uom"},
        {label: "采购库存id", value: "stockVirtualId"},
        {label: "采购单id", value: "purchaseId"},
        {label: "采购单明细id", value: "purchaseDtlId"},
        {label: "采购单据号", value: "purchaseKey"},
        {label: "虚拟仓库(调出仓库)", value: "warehouseFromId"},
        {label: "虚拟仓位(调出仓位)", value: "locationFromId"},
        {label: "目标虚拟仓库(调入仓库)", value: "warehouseToId"},
        {label: "目标虚拟仓位(调入仓位)", value: "locationToId"},
        {label: "产品id", value: "productId"},
        {label: "数量", value: "num"},
        {label: "单价(未税)", value: "priceUntax"},
        {label: "金额(未税)", value: "amountUntax"},
        {label: "含税单价", value: "price"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询调拨单列表 */
    function getList() {
        loading.value = true;
        listMove(queryParams.value).then(response => {
            moveList.value = response.rows;
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
            moveNo: null,
            moveDate: null,
            departmentId: null,
            workerId: null,
            partnerId: null,
            stockDate: null,
            status: null,
            approvalTime: null,
            uom: null,
            stockVirtualId: null,
            purchaseId: null,
            purchaseDtlId: null,
            purchaseKey: null,
            warehouseFromId: null,
            locationFromId: null,
            warehouseToId: null,
            locationToId: null,
            productId: null,
            num: null,
            priceUntax: null,
            amountUntax: null,
            price: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("moveRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.blocId = res,
            queryParams.value.sellerId = res,
            queryParams.value.docTypeId = res,
            queryParams.value.moveNo = res,
            queryParams.value.moveDate = res,
            queryParams.value.departmentId = res,
            queryParams.value.workerId = res,
            queryParams.value.partnerId = res,
            queryParams.value.stockDate = res,
            queryParams.value.status = res,
            queryParams.value.approvalTime = res,
            queryParams.value.uom = res,
            queryParams.value.stockVirtualId = res,
            queryParams.value.purchaseId = res,
            queryParams.value.purchaseDtlId = res,
            queryParams.value.purchaseKey = res,
            queryParams.value.warehouseFromId = res,
            queryParams.value.locationFromId = res,
            queryParams.value.warehouseToId = res,
            queryParams.value.locationToId = res,
            queryParams.value.productId = res,
            queryParams.value.num = res,
            queryParams.value.priceUntax = res,
            queryParams.value.amountUntax = res,
            queryParams.value.price = res,
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
        title.value = "添加调拨单";
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
        getMove(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改调拨单";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["moveRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateMove(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addMove(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除调拨单编号为"' + _ids + '"的数据项？').then(function () {
            return delMove(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/move/export', {
            ...queryParams.value
        }, `move_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
