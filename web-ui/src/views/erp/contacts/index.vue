<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入联系人"
                show-search
                label="联系人"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:contacts:add']">新建联系人</el-button>
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
                            <el-form-item label="商业伙伴id" prop="partnerId">
                                <el-input
                                        v-model="queryParams.partnerId"
                                        placeholder="请输入商业伙伴id"
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
                            <el-form-item label="联系人邮箱" prop="email">
                                <el-input
                                        v-model="queryParams.email"
                                        placeholder="请输入联系人邮箱"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="联系人qq/wx" prop="qq">
                                <el-input
                                        v-model="queryParams.qq"
                                        placeholder="请输入联系人qq/wx"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="联系人传真" prop="fax">
                                <el-input
                                        v-model="queryParams.fax"
                                        placeholder="请输入联系人传真"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="交易员id" prop="workerId">
                                <el-input
                                        v-model="queryParams.workerId"
                                        placeholder="请输入交易员id"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="部门id" prop="departmentId">
                                <el-input
                                        v-model="queryParams.departmentId"
                                        placeholder="请输入部门id"
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
                <el-table v-loading="loading" :data="contactsList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="联系人id" align="center" prop="id"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="商业伙伴id" align="center" prop="partnerId"/>
                    <el-table-column label="联系人姓名" align="center" prop="contactsName"/>
                    <el-table-column label="联系人手机/电话" align="center" prop="contactsTel"/>
                    <el-table-column label="联系人邮箱" align="center" prop="email"/>
                    <el-table-column label="联系人qq/wx" align="center" prop="qq"/>
                    <el-table-column label="联系人传真" align="center" prop="fax"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="状态" align="center" prop="status"/>
                    <el-table-column label="交易员id" align="center" prop="workerId"/>
                    <el-table-column label="部门id" align="center" prop="departmentId"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:contacts:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:contacts:remove']">删除
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
        <!-- 添加或修改联系人对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="contactsRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="商业伙伴id" prop="partnerId">
                    <el-input v-model="form.partnerId" placeholder="请输入商业伙伴id"/>
                </el-form-item>
                <el-form-item label="联系人姓名" prop="contactsName">
                    <el-input v-model="form.contactsName" placeholder="请输入联系人姓名"/>
                </el-form-item>
                <el-form-item label="联系人手机/电话" prop="contactsTel">
                    <el-input v-model="form.contactsTel" placeholder="请输入联系人手机/电话"/>
                </el-form-item>
                <el-form-item label="联系人邮箱" prop="email">
                    <el-input v-model="form.email" placeholder="请输入联系人邮箱"/>
                </el-form-item>
                <el-form-item label="联系人qq/wx" prop="qq">
                    <el-input v-model="form.qq" placeholder="请输入联系人qq/wx"/>
                </el-form-item>
                <el-form-item label="联系人传真" prop="fax">
                    <el-input v-model="form.fax" placeholder="请输入联系人传真"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="交易员id" prop="workerId">
                    <el-input v-model="form.workerId" placeholder="请输入交易员id"/>
                </el-form-item>
                <el-form-item label="部门id" prop="departmentId">
                    <el-input v-model="form.departmentId" placeholder="请输入部门id"/>
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

<script setup name="Contacts">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listContacts, getContacts, delContacts, addContacts, updateContacts} from "@/api/erp/contacts";

    const {proxy} = getCurrentInstance();

    const contactsList = ref([]);
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
            partnerId: null,
            contactsName: null,
            contactsTel: null,
            email: null,
            qq: null,
            fax: null,
            status: null,
            workerId: null,
            departmentId: null,
            createUid: null
        },
        rules: {
            partnerId: [
                {required: true, message: "商业伙伴id不能为空", trigger: "blur"}
            ],
            contactsName: [
                {required: true, message: "联系人姓名不能为空", trigger: "blur"}
            ],
            contactsTel: [
                {required: true, message: "联系人手机/电话不能为空", trigger: "blur"}
            ],
            status: [
                {required: true, message: "状态不能为空", trigger: "change"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司父级id", value: "blocId"},
        {label: "公司id", value: "sellerId"},
        {label: "商业伙伴id", value: "partnerId"},
        {label: "联系人姓名", value: "contactsName"},
        {label: "联系人手机/电话", value: "contactsTel"},
        {label: "联系人邮箱", value: "email"},
        {label: "联系人qq/wx", value: "qq"},
        {label: "联系人传真", value: "fax"},
        {label: "状态", value: "status"},
        {label: "交易员id", value: "workerId"},
        {label: "部门id", value: "departmentId"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询联系人列表 */
    function getList() {
        loading.value = true;
        listContacts(queryParams.value).then(response => {
            contactsList.value = response.rows;
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
            partnerId: null,
            contactsName: null,
            contactsTel: null,
            email: null,
            qq: null,
            fax: null,
            remark: null,
            status: null,
            workerId: null,
            departmentId: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("contactsRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.blocId = res,
            queryParams.value.sellerId = res,
            queryParams.value.partnerId = res,
            queryParams.value.contactsName = res,
            queryParams.value.contactsTel = res,
            queryParams.value.email = res,
            queryParams.value.qq = res,
            queryParams.value.fax = res,
            queryParams.value.status = res,
            queryParams.value.workerId = res,
            queryParams.value.departmentId = res,
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
        title.value = "添加联系人";
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
        getContacts(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改联系人";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["contactsRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateContacts(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addContacts(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除联系人编号为"' + _ids + '"的数据项？').then(function () {
            return delContacts(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/contacts/export', {
            ...queryParams.value
        }, `contacts_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
