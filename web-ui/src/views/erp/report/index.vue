<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入采购库存"
                show-search
                label="采购库存"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:report:add']">新建采购库存</el-button>
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
                            <el-form-item label="订单id" prop="orderId">
                                <el-input
                                        v-model="queryParams.orderId"
                                        placeholder="请输入订单id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="销售/采购详情id" prop="orderDtlId">
                                <el-input
                                        v-model="queryParams.orderDtlId"
                                        placeholder="请输入销售/采购详情id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="库存数量" prop="num">
                                <el-input
                                        v-model="queryParams.num"
                                        placeholder="请输入库存数量"
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
                            <el-form-item label="已报价数量" prop="quoteNum">
                                <el-input
                                        v-model="queryParams.quoteNum"
                                        placeholder="请输入已报价数量"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="库存所处单" prop="sourceKey">
                                <el-input
                                        v-model="queryParams.sourceKey"
                                        placeholder="请输入库存所处单"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="调拨单id" prop="moveId">
                                <el-input
                                        v-model="queryParams.moveId"
                                        placeholder="请输入调拨单id"
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
                            <el-form-item label="虚拟仓库id" prop="virtualWarehouseId">
                                <el-input
                                        v-model="queryParams.virtualWarehouseId"
                                        placeholder="请输入虚拟仓库id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="虚拟仓位id" prop="virtualLocationId">
                                <el-input
                                        v-model="queryParams.virtualLocationId"
                                        placeholder="请输入虚拟仓位id"
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
                <el-table v-loading="loading" :data="reportList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="采购库存id" align="center" prop="id"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="订单id" align="center" prop="orderId"/>
                    <el-table-column label="销售/采购详情id" align="center" prop="orderDtlId"/>
                    <el-table-column label="库存数量" align="center" prop="num"/>
                    <el-table-column label="单位" align="center" prop="uom"/>
                    <el-table-column label="已报价数量" align="center" prop="quoteNum"/>
                    <el-table-column label="库存所处单" align="center" prop="sourceKey"/>
                    <el-table-column label="库存状态 0负库存 1正库存" align="center" prop="status"/>
                    <el-table-column label="调拨单id" align="center" prop="moveId"/>
                    <el-table-column label="产品id" align="center" prop="productId"/>
                    <el-table-column label="虚拟仓库id" align="center" prop="virtualWarehouseId"/>
                    <el-table-column label="虚拟仓位id" align="center" prop="virtualLocationId"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:report:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:report:remove']">删除
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
        <!-- 添加或修改采购库存对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="reportRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="订单id" prop="orderId">
                    <el-input v-model="form.orderId" placeholder="请输入订单id"/>
                </el-form-item>
                <el-form-item label="销售/采购详情id" prop="orderDtlId">
                    <el-input v-model="form.orderDtlId" placeholder="请输入销售/采购详情id"/>
                </el-form-item>
                <el-form-item label="库存数量" prop="num">
                    <el-input v-model="form.num" placeholder="请输入库存数量"/>
                </el-form-item>
                <el-form-item label="单位" prop="uom">
                    <el-input v-model="form.uom" placeholder="请输入单位"/>
                </el-form-item>
                <el-form-item label="已报价数量" prop="quoteNum">
                    <el-input v-model="form.quoteNum" placeholder="请输入已报价数量"/>
                </el-form-item>
                <el-form-item label="库存所处单" prop="sourceKey">
                    <el-input v-model="form.sourceKey" placeholder="请输入库存所处单"/>
                </el-form-item>
                <el-form-item label="调拨单id" prop="moveId">
                    <el-input v-model="form.moveId" placeholder="请输入调拨单id"/>
                </el-form-item>
                <el-form-item label="产品id" prop="productId">
                    <el-input v-model="form.productId" placeholder="请输入产品id"/>
                </el-form-item>
                <el-form-item label="虚拟仓库id" prop="virtualWarehouseId">
                    <el-input v-model="form.virtualWarehouseId" placeholder="请输入虚拟仓库id"/>
                </el-form-item>
                <el-form-item label="虚拟仓位id" prop="virtualLocationId">
                    <el-input v-model="form.virtualLocationId" placeholder="请输入虚拟仓位id"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
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

<script setup name="Report">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listReport, getReport, delReport, addReport, updateReport} from "@/api/erp/report";

    const {proxy} = getCurrentInstance();

    const reportList = ref([]);
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
            orderId: null,
            orderDtlId: null,
            num: null,
            uom: null,
            quoteNum: null,
            sourceKey: null,
            status: null,
            moveId: null,
            productId: null,
            virtualWarehouseId: null,
            virtualLocationId: null,
        },
        rules: {
            orderId: [
                {required: true, message: "订单id不能为空", trigger: "blur"}
            ],
            num: [
                {required: true, message: "库存数量不能为空", trigger: "blur"}
            ],
            quoteNum: [
                {required: true, message: "已报价数量不能为空", trigger: "blur"}
            ],
            status: [
                {required: true, message: "库存状态 0负库存 1正库存不能为空", trigger: "change"}
            ],
            moveId: [
                {required: true, message: "调拨单id不能为空", trigger: "blur"}
            ],
            productId: [
                {required: true, message: "产品id不能为空", trigger: "blur"}
            ],
            virtualWarehouseId: [
                {required: true, message: "虚拟仓库id不能为空", trigger: "blur"}
            ],
            virtualLocationId: [
                {required: true, message: "虚拟仓位id不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司父级id", value: "blocId"},
        {label: "公司id", value: "sellerId"},
        {label: "订单id", value: "orderId"},
        {label: "销售/采购详情id", value: "orderDtlId"},
        {label: "库存数量", value: "num"},
        {label: "单位", value: "uom"},
        {label: "已报价数量", value: "quoteNum"},
        {label: "库存所处单", value: "sourceKey"},
        {label: "库存状态 0负库存 1正库存", value: "status"},
        {label: "调拨单id", value: "moveId"},
        {label: "产品id", value: "productId"},
        {label: "虚拟仓库id", value: "virtualWarehouseId"},
        {label: "虚拟仓位id", value: "virtualLocationId"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询采购库存列表 */
    function getList() {
        loading.value = true;
        listReport(queryParams.value).then(response => {
            reportList.value = response.rows;
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
            orderId: null,
            orderDtlId: null,
            num: null,
            uom: null,
            quoteNum: null,
            sourceKey: null,
            status: null,
            moveId: null,
            productId: null,
            virtualWarehouseId: null,
            virtualLocationId: null,
            remark: null
        };
        proxy.resetForm("reportRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.blocId = res,
            queryParams.value.sellerId = res,
            queryParams.value.orderId = res,
            queryParams.value.orderDtlId = res,
            queryParams.value.num = res,
            queryParams.value.uom = res,
            queryParams.value.quoteNum = res,
            queryParams.value.sourceKey = res,
            queryParams.value.status = res,
            queryParams.value.moveId = res,
            queryParams.value.productId = res,
            queryParams.value.virtualWarehouseId = res,
            queryParams.value.virtualLocationId = res,
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
        title.value = "添加采购库存";
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
        getReport(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改采购库存";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["reportRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateReport(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addReport(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除采购库存编号为"' + _ids + '"的数据项？').then(function () {
            return delReport(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/report/export', {
            ...queryParams.value
        }, `report_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
