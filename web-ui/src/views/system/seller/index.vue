<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入公司列表"
                show-search
                label="公司列表"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['system:seller:add']">新建公司列表</el-button>
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
                            <el-form-item label="公司名称" prop="sellerName">
                                <el-input
                                        v-model="queryParams.sellerName"
                                        placeholder="请输入公司名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司简称" prop="shortName">
                                <el-input
                                        v-model="queryParams.shortName"
                                        placeholder="请输入公司简称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="父级名称" prop="blocName">
                                <el-input
                                        v-model="queryParams.blocName"
                                        placeholder="请输入父级名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司地址" prop="address">
                                <el-input
                                        v-model="queryParams.address"
                                        placeholder="请输入公司地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司logo" prop="logo">
                                <el-input
                                        v-model="queryParams.logo"
                                        placeholder="请输入公司logo"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司电话" prop="tel">
                                <el-input
                                        v-model="queryParams.tel"
                                        placeholder="请输入公司电话"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="总账期间" prop="period">
                                <el-input
                                        v-model="queryParams.period"
                                        placeholder="请输入总账期间"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="总账期间年" prop="periodYear">
                                <el-input
                                        v-model="queryParams.periodYear"
                                        placeholder="请输入总账期间年"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="总账期间月" prop="periodMonth">
                                <el-input
                                        v-model="queryParams.periodMonth"
                                        placeholder="请输入总账期间月"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="头部状态栏颜色" prop="headerColor">
                                <el-input
                                        v-model="queryParams.headerColor"
                                        placeholder="请输入头部状态栏颜色"
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
                            <el-form-item label="公司税号" prop="sellerIdentifier">
                                <el-input
                                        v-model="queryParams.sellerIdentifier"
                                        placeholder="请输入公司税号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司开票地址" prop="sellerRegisterAddr">
                                <el-input
                                        v-model="queryParams.sellerRegisterAddr"
                                        placeholder="请输入公司开票地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司联系电话" prop="sellerRegisterPhone">
                                <el-input
                                        v-model="queryParams.sellerRegisterPhone"
                                        placeholder="请输入公司联系电话"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司开户行" prop="sellerOpeningBank">
                                <el-input
                                        v-model="queryParams.sellerOpeningBank"
                                        placeholder="请输入公司开户行"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司银行账号" prop="sellerBankAccount">
                                <el-input
                                        v-model="queryParams.sellerBankAccount"
                                        placeholder="请输入公司银行账号"
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
                <el-table v-loading="loading" :data="sellerList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="公司id" align="center" prop="id"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="公司名称" align="center" prop="sellerName"/>
                    <el-table-column label="公司简称" align="center" prop="shortName"/>
                    <el-table-column label="父级名称" align="center" prop="blocName"/>
                    <el-table-column label="企业注册类型(SINGLE-单公司,MULTIPLE-多公司)" align="center" prop="signType"/>
                    <el-table-column label="项目类型(INSIDE-内部公司,OUTSIDE-外部公司)" align="center" prop="projectType"/>
                    <el-table-column label="公司地址" align="center" prop="address"/>
                    <el-table-column label="公司logo" align="center" prop="logo"/>
                    <el-table-column label="公司电话" align="center" prop="tel"/>
                    <el-table-column label="总账期间" align="center" prop="period"/>
                    <el-table-column label="总账期间年" align="center" prop="periodYear"/>
                    <el-table-column label="总账期间月" align="center" prop="periodMonth"/>
                    <el-table-column label="头部状态栏颜色" align="center" prop="headerColor"/>
                    <el-table-column label="是否可用(1启用 0停用)" align="center" prop="isAvailable"/>
                    <el-table-column label="公司税号" align="center" prop="sellerIdentifier"/>
                    <el-table-column label="公司开票地址" align="center" prop="sellerRegisterAddr"/>
                    <el-table-column label="公司联系电话" align="center" prop="sellerRegisterPhone"/>
                    <el-table-column label="公司开户行" align="center" prop="sellerOpeningBank"/>
                    <el-table-column label="公司银行账号" align="center" prop="sellerBankAccount"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['system:seller:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['system:seller:remove']">删除
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
        <!-- 添加或修改公司列表对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="sellerRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="公司名称" prop="sellerName">
                    <el-input v-model="form.sellerName" placeholder="请输入公司名称"/>
                </el-form-item>
                <el-form-item label="公司简称" prop="shortName">
                    <el-input v-model="form.shortName" placeholder="请输入公司简称"/>
                </el-form-item>
                <el-form-item label="父级名称" prop="blocName">
                    <el-input v-model="form.blocName" placeholder="请输入父级名称"/>
                </el-form-item>
                <el-form-item label="公司地址" prop="address">
                    <el-input v-model="form.address" placeholder="请输入公司地址"/>
                </el-form-item>
                <el-form-item label="公司logo" prop="logo">
                    <el-input v-model="form.logo" placeholder="请输入公司logo"/>
                </el-form-item>
                <el-form-item label="公司电话" prop="tel">
                    <el-input v-model="form.tel" placeholder="请输入公司电话"/>
                </el-form-item>
                <el-form-item label="总账期间" prop="period">
                    <el-input v-model="form.period" placeholder="请输入总账期间"/>
                </el-form-item>
                <el-form-item label="总账期间年" prop="periodYear">
                    <el-input v-model="form.periodYear" placeholder="请输入总账期间年"/>
                </el-form-item>
                <el-form-item label="总账期间月" prop="periodMonth">
                    <el-input v-model="form.periodMonth" placeholder="请输入总账期间月"/>
                </el-form-item>
                <el-form-item label="头部状态栏颜色" prop="headerColor">
                    <el-input v-model="form.headerColor" placeholder="请输入头部状态栏颜色"/>
                </el-form-item>
                <el-form-item label="是否可用(1启用 0停用)" prop="isAvailable">
                    <el-input v-model="form.isAvailable" placeholder="请输入是否可用(1启用 0停用)"/>
                </el-form-item>
                <el-form-item label="公司税号" prop="sellerIdentifier">
                    <el-input v-model="form.sellerIdentifier" placeholder="请输入公司税号"/>
                </el-form-item>
                <el-form-item label="公司开票地址" prop="sellerRegisterAddr">
                    <el-input v-model="form.sellerRegisterAddr" placeholder="请输入公司开票地址"/>
                </el-form-item>
                <el-form-item label="公司联系电话" prop="sellerRegisterPhone">
                    <el-input v-model="form.sellerRegisterPhone" placeholder="请输入公司联系电话"/>
                </el-form-item>
                <el-form-item label="公司开户行" prop="sellerOpeningBank">
                    <el-input v-model="form.sellerOpeningBank" placeholder="请输入公司开户行"/>
                </el-form-item>
                <el-form-item label="公司银行账号" prop="sellerBankAccount">
                    <el-input v-model="form.sellerBankAccount" placeholder="请输入公司银行账号"/>
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

<script setup name="Seller">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listSeller, getSeller, delSeller, addSeller, updateSeller} from "@/api/system/seller";

    const {proxy} = getCurrentInstance();

    const sellerList = ref([]);
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
            sellerName: null,
            shortName: null,
            blocName: null,
            signType: null,
            projectType: null,
            address: null,
            logo: null,
            tel: null,
            period: null,
            periodYear: null,
            periodMonth: null,
            headerColor: null,
            isAvailable: null,
            sellerIdentifier: null,
            sellerRegisterAddr: null,
            sellerRegisterPhone: null,
            sellerOpeningBank: null,
            sellerBankAccount: null,
        },
        rules: {
            sellerName: [
                {required: true, message: "公司名称不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司父级id", value: "blocId"},
        {label: "公司名称", value: "sellerName"},
        {label: "公司简称", value: "shortName"},
        {label: "父级名称", value: "blocName"},
        {label: "企业注册类型(SINGLE-单公司,MULTIPLE-多公司)", value: "signType"},
        {label: "项目类型(INSIDE-内部公司,OUTSIDE-外部公司)", value: "projectType"},
        {label: "公司地址", value: "address"},
        {label: "公司logo", value: "logo"},
        {label: "公司电话", value: "tel"},
        {label: "总账期间", value: "period"},
        {label: "总账期间年", value: "periodYear"},
        {label: "总账期间月", value: "periodMonth"},
        {label: "头部状态栏颜色", value: "headerColor"},
        {label: "是否可用(1启用 0停用)", value: "isAvailable"},
        {label: "公司税号", value: "sellerIdentifier"},
        {label: "公司开票地址", value: "sellerRegisterAddr"},
        {label: "公司联系电话", value: "sellerRegisterPhone"},
        {label: "公司开户行", value: "sellerOpeningBank"},
        {label: "公司银行账号", value: "sellerBankAccount"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询公司列表列表 */
    function getList() {
        loading.value = true;
        listSeller(queryParams.value).then(response => {
            sellerList.value = response.rows;
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
            sellerName: null,
            shortName: null,
            blocName: null,
            signType: null,
            projectType: null,
            address: null,
            logo: null,
            tel: null,
            period: null,
            periodYear: null,
            periodMonth: null,
            headerColor: null,
            isAvailable: null,
            sellerIdentifier: null,
            sellerRegisterAddr: null,
            sellerRegisterPhone: null,
            sellerOpeningBank: null,
            sellerBankAccount: null,
            createTime: null,
            updateTime: null,
            remark: null
        };
        proxy.resetForm("sellerRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.blocId = res,
            queryParams.value.sellerName = res,
            queryParams.value.shortName = res,
            queryParams.value.blocName = res,
            queryParams.value.signType = res,
            queryParams.value.projectType = res,
            queryParams.value.address = res,
            queryParams.value.logo = res,
            queryParams.value.tel = res,
            queryParams.value.period = res,
            queryParams.value.periodYear = res,
            queryParams.value.periodMonth = res,
            queryParams.value.headerColor = res,
            queryParams.value.isAvailable = res,
            queryParams.value.sellerIdentifier = res,
            queryParams.value.sellerRegisterAddr = res,
            queryParams.value.sellerRegisterPhone = res,
            queryParams.value.sellerOpeningBank = res,
            queryParams.value.sellerBankAccount = res,
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
        title.value = "添加公司列表";
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
        getSeller(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改公司列表";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["sellerRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateSeller(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addSeller(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除公司列表编号为"' + _ids + '"的数据项？').then(function () {
            return delSeller(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('system/seller/export', {
            ...queryParams.value
        }, `seller_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
