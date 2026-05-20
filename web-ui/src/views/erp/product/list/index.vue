<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入产品信息"
                show-search
                label="产品信息"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['product:product:add']">新建产品信息</el-button>
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
                            <el-form-item label="产品全称" prop="originalName">
                                <el-input
                                        v-model="queryParams.originalName"
                                        placeholder="请输入产品全称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="产品名称" prop="productName">
                                <el-input
                                        v-model="queryParams.productName"
                                        placeholder="请输入产品名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="产品编号" prop="productCode">
                                <el-input
                                        v-model="queryParams.productCode"
                                        placeholder="请输入产品编号"
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
                            <el-form-item label="是否可用" prop="isAvailable">
                                <el-input
                                        v-model="queryParams.isAvailable"
                                        placeholder="请输入是否可用"
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
                <el-table v-loading="loading" style="width: 100%" :data="productList" border stripe show-header
                          highlight-current-row @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column fixed label="分类名称" align="center" prop="categoryName" width="80"/>
                    <el-table-column fixed label="产品名称" align="center" prop="productName" width="120"/>
                    <el-table-column fixed label="厂商名称" align="center" prop="brandName" width="120"/>
                    <el-table-column label="产品全称" align="center" prop="originalName" width="160"/>
                    <el-table-column label="产品编号" align="center" prop="productCode" width="180"/>
                    <el-table-column label="单位" align="center" prop="uom" width="120">
                        <template #default="scope">
                            <dict-tag :options="sys_uom_type" :value="scope.row.uom"/>
                        </template>
                    </el-table-column>
                    <el-table-column label="状态" align="center" prop="isAvailable" width="120">
                        <template #default="scope">
                            <dict-tag :options="sys_normal_disable" :value="scope.row.uom"/>
                        </template>
                    </el-table-column>
                    <el-table-column label="创建人id" align="center" prop="createUid" width="120"/>
                    <el-table-column label="删除时间(软删除)" align="center" prop="deleteTime" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.deleteTime, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="备注" align="center" prop="remark"/>
                </el-table>
                <div class="p-contianer">
                    <pagination
                            :page-sizes="[14, 20, 30, 40, 50, 100]"
                            v-show="total>0"
                            :total="total"
                            v-model:page="queryParams.pageNum"
                            v-model:limit="queryParams.pageSize"
                            @pagination="getList"
                    />
                </div>
            </el-col>
        </el-row>
        <!-- 添加或修改产品基本信息对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="productRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="产品全称" prop="originalName">
                    <el-input v-model="form.originalName" placeholder="请输入产品全称"/>
                </el-form-item>
                <el-form-item label="产品名称" prop="productName">
                    <el-input v-model="form.productName" placeholder="请输入产品名称"/>
                </el-form-item>
                <el-form-item label="产品编号" prop="productCode">
                    <el-input v-model="form.productCode" placeholder="请输入产品编号"/>
                </el-form-item>
                <el-form-item label="单位">
                    <el-select v-model="form.uom" prop="uom" placeholder="请输入单位">
                        <el-option
                                v-for="dict in sys_uom_type"
                                :key="dict.value"
                                :label="dict.label"
                                :value="dict.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="是否可用" prop="isAvailable">
                    <el-input v-model="form.isAvailable" placeholder="请输入是否可用"/>
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

<script setup name="Product">
    import useDictStore from '@/store/modules/dict'
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listProduct, getProduct, delProduct, addProduct, updateProduct} from "@/api/erp/product";

    const {proxy} = getCurrentInstance();
    const {sys_uom_type, sys_normal_disable} = proxy.useDict("sys_uom_type", "sys_normal_disable");

    const productList = ref([]);
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
            brandId: null,
            categoryId: null,
            originalName: null,
            productName: null,
            productCode: null,
            uom: null,
            isAvailable: null,
            createUid: null,
            deleteTime: null
        },
        rules: {}
    });

    const showColumn = ref([
        {label: "产品厂商", value: "brandId"},
        {label: "产品分类", value: "categoryId"},
        {label: "产品全称", value: "originalName"},
        {label: "产品名称", value: "productName"},
        {label: "产品编号（牌号）", value: "productCode"},
        {label: "单位", value: "uom"},
        {label: "是否可用（1启用，0停用）", value: "isAvailable"},
        {label: "创建人id", value: "createUid"},
        {label: "删除时间(软删除)", value: "deleteTime"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询产品基本信息列表 */
    function getList() {
        loading.value = true;
        listProduct(queryParams.value).then(response => {
            productList.value = response.rows;
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
            brandId: null,
            categoryId: null,
            originalName: null,
            productName: null,
            productCode: null,
            uom: null,
            remark: null,
            isAvailable: null,
            createTime: null,
            createUid: null,
            deleteTime: null
        };
        proxy.resetForm("productRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.productCode = res
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
        title.value = "添加产品基本信息";
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
        getProduct(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改产品基本信息";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["productRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateProduct(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addProduct(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除产品基本信息编号为"' + _ids + '"的数据项？').then(function () {
            return delProduct(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('product/product/export', {
            ...queryParams.value
        }, `product_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
