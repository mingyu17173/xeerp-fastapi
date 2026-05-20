<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入企业工商数据"
                show-search
                label="企业工商数据"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:information:add']">新建企业工商数据</el-button>
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
                            <el-form-item label="商业伙伴id" prop="partnerId">
                                <el-input
                                        v-model="queryParams.partnerId"
                                        placeholder="请输入商业伙伴id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="公司名称" prop="partnerName">
                                <el-input
                                        v-model="queryParams.partnerName"
                                        placeholder="请输入公司名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="法定代表人" prop="operName">
                                <el-input
                                        v-model="queryParams.operName"
                                        placeholder="请输入法定代表人"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="成立日期" prop="startDate">
                                <el-date-picker clearable
                                                v-model="queryParams.startDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择成立日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="营业期限自" prop="termStart">
                                <el-date-picker clearable
                                                v-model="queryParams.termStart"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择营业期限自">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="营业期限至" prop="teamEnd">
                                <el-date-picker clearable
                                                v-model="queryParams.teamEnd"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择营业期限至">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="核准日期" prop="checkDate">
                                <el-date-picker clearable
                                                v-model="queryParams.checkDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择核准日期">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="登记机关" prop="belongOrg">
                                <el-input
                                        v-model="queryParams.belongOrg"
                                        placeholder="请输入登记机关"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="所在省份缩写" prop="province">
                                <el-input
                                        v-model="queryParams.province"
                                        placeholder="请输入所在省份缩写"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="记录更新时间" prop="updatedDate">
                                <el-date-picker clearable
                                                v-model="queryParams.updatedDate"
                                                type="date"
                                                value-format="YYYY-MM-DD"
                                                placeholder="请选择记录更新时间">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="信用代码" prop="creditCode">
                                <el-input
                                        v-model="queryParams.creditCode"
                                        placeholder="请输入信用代码"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="注册号或统一社会信用代码，默认统一社会信用代码" prop="registNo">
                                <el-input
                                        v-model="queryParams.registNo"
                                        placeholder="请输入注册号或统一社会信用代码，默认统一社会信用代码"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="注册资本" prop="registCapi">
                                <el-input
                                        v-model="queryParams.registCapi"
                                        placeholder="请输入注册资本"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="类型" prop="econKind">
                                <el-input
                                        v-model="queryParams.econKind"
                                        placeholder="请输入类型"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="地址" prop="address">
                                <el-input
                                        v-model="queryParams.address"
                                        placeholder="请输入地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="经营范围" prop="scope">
                                <el-input
                                        v-model="queryParams.scope"
                                        placeholder="请输入经营范围"
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
                <RefreshView style="margin-right: 20px;" @click="resetQuery"></RefreshView>
                <ShowFilter :columns="showColumn"></ShowFilter>
            </template>
        </header-view>
        <el-row :gutter="20" style="margin: 15px 0px;">
            <el-col :span="24">
                <el-table v-loading="loading" :data="informationList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="企业工商信息id" align="center" prop="id"/>
                    <el-table-column label="商业伙伴id" align="center" prop="partnerId"/>
                    <el-table-column label="公司名称" align="center" prop="partnerName"/>
                    <el-table-column label="法定代表人" align="center" prop="operName"/>
                    <el-table-column label="成立日期" align="center" prop="startDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.startDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="营业期限自" align="center" prop="termStart" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.termStart, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="营业期限至" align="center" prop="teamEnd" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.teamEnd, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="核准日期" align="center" prop="checkDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.checkDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="登记状态" align="center" prop="status"/>
                    <el-table-column label="登记机关" align="center" prop="belongOrg"/>
                    <el-table-column label="所在省份缩写" align="center" prop="province"/>
                    <el-table-column label="记录更新时间" align="center" prop="updatedDate" width="180">
                        <template #default="scope">
                            <span>{{ parseTime(scope.row.updatedDate, '{y}-{m}-{d}') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="信用代码" align="center" prop="creditCode"/>
                    <el-table-column label="注册号或统一社会信用代码，默认统一社会信用代码" align="center" prop="registNo"/>
                    <el-table-column label="注册资本" align="center" prop="registCapi"/>
                    <el-table-column label="类型" align="center" prop="econKind"/>
                    <el-table-column label="地址" align="center" prop="address"/>
                    <el-table-column label="经营范围" align="center" prop="scope"/>
                    <el-table-column label="是否可用(1启用，0停用)" align="center" prop="isAvailable"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:information:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:information:remove']">删除
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
        <!-- 添加或修改企业工商数据对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="informationRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="商业伙伴id" prop="partnerId">
                    <el-input v-model="form.partnerId" placeholder="请输入商业伙伴id"/>
                </el-form-item>
                <el-form-item label="公司名称" prop="partnerName">
                    <el-input v-model="form.partnerName" placeholder="请输入公司名称"/>
                </el-form-item>
                <el-form-item label="法定代表人" prop="operName">
                    <el-input v-model="form.operName" placeholder="请输入法定代表人"/>
                </el-form-item>
                <el-form-item label="成立日期" prop="startDate">
                    <el-date-picker clearable
                                    v-model="form.startDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择成立日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="营业期限自" prop="termStart">
                    <el-date-picker clearable
                                    v-model="form.termStart"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择营业期限自">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="营业期限至" prop="teamEnd">
                    <el-date-picker clearable
                                    v-model="form.teamEnd"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择营业期限至">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="核准日期" prop="checkDate">
                    <el-date-picker clearable
                                    v-model="form.checkDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择核准日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="登记机关" prop="belongOrg">
                    <el-input v-model="form.belongOrg" placeholder="请输入登记机关"/>
                </el-form-item>
                <el-form-item label="所在省份缩写" prop="province">
                    <el-input v-model="form.province" placeholder="请输入所在省份缩写"/>
                </el-form-item>
                <el-form-item label="记录更新时间" prop="updatedDate">
                    <el-date-picker clearable
                                    v-model="form.updatedDate"
                                    type="date"
                                    value-format="YYYY-MM-DD"
                                    placeholder="请选择记录更新时间">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="信用代码" prop="creditCode">
                    <el-input v-model="form.creditCode" placeholder="请输入信用代码"/>
                </el-form-item>
                <el-form-item label="注册号或统一社会信用代码，默认统一社会信用代码" prop="registNo">
                    <el-input v-model="form.registNo" placeholder="请输入注册号或统一社会信用代码，默认统一社会信用代码"/>
                </el-form-item>
                <el-form-item label="注册资本" prop="registCapi">
                    <el-input v-model="form.registCapi" placeholder="请输入注册资本"/>
                </el-form-item>
                <el-form-item label="类型" prop="econKind">
                    <el-input v-model="form.econKind" placeholder="请输入类型"/>
                </el-form-item>
                <el-form-item label="地址" prop="address">
                    <el-input v-model="form.address" placeholder="请输入地址"/>
                </el-form-item>
                <el-form-item label="经营范围" prop="scope">
                    <el-input v-model="form.scope" placeholder="请输入经营范围"/>
                </el-form-item>
                <el-form-item label="是否可用(1启用，0停用)" prop="isAvailable">
                    <el-input v-model="form.isAvailable" placeholder="请输入是否可用(1启用，0停用)"/>
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

<script setup name="Information">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {
        listInformation,
        getInformation,
        delInformation,
        addInformation,
        updateInformation
    } from "@/api/erp/information";

    const {proxy} = getCurrentInstance();

    const informationList = ref([]);
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
            partnerId: null,
            partnerName: null,
            operName: null,
            startDate: null,
            termStart: null,
            teamEnd: null,
            checkDate: null,
            status: null,
            belongOrg: null,
            province: null,
            updatedDate: null,
            creditCode: null,
            registNo: null,
            registCapi: null,
            econKind: null,
            address: null,
            scope: null,
            isAvailable: null,
            createUid: null
        },
        rules: {
            partnerId: [
                {required: true, message: "商业伙伴id不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "商业伙伴id", value: "partnerId"},
        {label: "公司名称", value: "partnerName"},
        {label: "法定代表人", value: "operName"},
        {label: "成立日期", value: "startDate"},
        {label: "营业期限自", value: "termStart"},
        {label: "营业期限至", value: "teamEnd"},
        {label: "核准日期", value: "checkDate"},
        {label: "登记状态", value: "status"},
        {label: "登记机关", value: "belongOrg"},
        {label: "所在省份缩写", value: "province"},
        {label: "记录更新时间", value: "updatedDate"},
        {label: "信用代码", value: "creditCode"},
        {label: "注册号或统一社会信用代码，默认统一社会信用代码", value: "registNo"},
        {label: "注册资本", value: "registCapi"},
        {label: "类型", value: "econKind"},
        {label: "地址", value: "address"},
        {label: "经营范围", value: "scope"},
        {label: "是否可用(1启用，0停用)", value: "isAvailable"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询企业工商数据列表 */
    function getList() {
        loading.value = true;
        listInformation(queryParams.value).then(response => {
            informationList.value = response.rows;
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
            partnerId: null,
            partnerName: null,
            operName: null,
            startDate: null,
            termStart: null,
            teamEnd: null,
            checkDate: null,
            status: null,
            belongOrg: null,
            province: null,
            updatedDate: null,
            creditCode: null,
            registNo: null,
            registCapi: null,
            econKind: null,
            address: null,
            scope: null,
            isAvailable: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("informationRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.partnerId = res,
            queryParams.value.partnerName = res,
            queryParams.value.operName = res,
            queryParams.value.startDate = res,
            queryParams.value.termStart = res,
            queryParams.value.teamEnd = res,
            queryParams.value.checkDate = res,
            queryParams.value.status = res,
            queryParams.value.belongOrg = res,
            queryParams.value.province = res,
            queryParams.value.updatedDate = res,
            queryParams.value.creditCode = res,
            queryParams.value.registNo = res,
            queryParams.value.registCapi = res,
            queryParams.value.econKind = res,
            queryParams.value.address = res,
            queryParams.value.scope = res,
            queryParams.value.isAvailable = res,
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
        title.value = "添加企业工商数据";
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
        getInformation(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改企业工商数据";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["informationRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateInformation(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addInformation(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除企业工商数据编号为"' + _ids + '"的数据项？').then(function () {
            return delInformation(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/information/export', {
            ...queryParams.value
        }, `information_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
