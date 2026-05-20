<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入合同模版"
                show-search
                label="合同模版"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['erp:template:add']">新建合同模版</el-button>
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
                            <el-form-item label="模版名称" prop="templateName">
                                <el-input
                                        v-model="queryParams.templateName"
                                        placeholder="请输入模版名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="是否有效" prop="isActive">
                                <el-input
                                        v-model="queryParams.isActive"
                                        placeholder="请输入是否有效"
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
                            <el-form-item label="修改人id" prop="updateUid">
                                <el-input
                                        v-model="queryParams.updateUid"
                                        placeholder="请输入修改人id"
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
                <el-table v-loading="loading" :data="templateList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="模版id" align="center" prop="templateId"/>
                    <el-table-column label="公司id" align="center" prop="sellerId"/>
                    <el-table-column label="公司父级id" align="center" prop="blocId"/>
                    <el-table-column label="模版名称" align="center" prop="templateName"/>
                    <el-table-column label="合同内容" align="center" prop="content"/>
                    <el-table-column label="是否有效" align="center" prop="isActive"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="修改人id" align="center" prop="updateUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['erp:template:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['erp:template:remove']">删除
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
        <!-- 添加或修改合同模版对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="templateRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="公司id" prop="sellerId">
                    <el-input v-model="form.sellerId" placeholder="请输入公司id"/>
                </el-form-item>
                <el-form-item label="公司父级id" prop="blocId">
                    <el-input v-model="form.blocId" placeholder="请输入公司父级id"/>
                </el-form-item>
                <el-form-item label="模版名称" prop="templateName">
                    <el-input v-model="form.templateName" placeholder="请输入模版名称"/>
                </el-form-item>
                <el-form-item label="合同内容">
                    <editor v-model="form.content" :min-height="192"/>
                </el-form-item>
                <el-form-item label="是否有效" prop="isActive">
                    <el-input v-model="form.isActive" placeholder="请输入是否有效"/>
                </el-form-item>
                <el-form-item label="创建人id" prop="createUid">
                    <el-input v-model="form.createUid" placeholder="请输入创建人id"/>
                </el-form-item>
                <el-form-item label="修改人id" prop="updateUid">
                    <el-input v-model="form.updateUid" placeholder="请输入修改人id"/>
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

<script setup name="Template">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listTemplate, getTemplate, delTemplate, addTemplate, updateTemplate} from "@/api/erp/template";

    const {proxy} = getCurrentInstance();

    const templateList = ref([]);
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
            templateName: null,
            content: null,
            isActive: null,
            createUid: null,
            updateUid: null
        },
        rules: {
            templateName: [
                {required: true, message: "模版名称不能为空", trigger: "blur"}
            ],
            content: [
                {required: true, message: "合同内容不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "公司id", value: "sellerId"},
        {label: "公司父级id", value: "blocId"},
        {label: "模版名称", value: "templateName"},
        {label: "合同内容", value: "content"},
        {label: "是否有效（1有效 0无效）", value: "isActive"},
        {label: "创建人id", value: "createUid"},
        {label: "修改人id", value: "updateUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询合同模版列表 */
    function getList() {
        loading.value = true;
        listTemplate(queryParams.value).then(response => {
            templateList.value = response.rows;
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
            templateId: null,
            sellerId: null,
            blocId: null,
            templateName: null,
            content: null,
            isActive: null,
            createTime: null,
            createUid: null,
            updateTime: null,
            updateUid: null
        };
        proxy.resetForm("templateRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.sellerId = res,
            queryParams.value.blocId = res,
            queryParams.value.templateName = res,
            queryParams.value.content = res,
            queryParams.value.isActive = res,
            queryParams.value.createUid = res,
            queryParams.value.updateUid = res,
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
        ids.value = selection.map(item => item.templateId);
        single.value = selection.length != 1;
        multiple.value = !selection.length;
    }

    /** 新增按钮操作 */
    function handleAdd() {
        reset();
        open.value = true;
        title.value = "添加合同模版";
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
        const _templateId = row.templateId || ids.value
        getTemplate(_templateId).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改合同模版";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["templateRef"].validate(valid => {
            if (valid) {
                if (form.value.templateId != null) {
                    updateTemplate(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addTemplate(form.value).then(response => {
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
        const _templateIds = row.templateId || ids.value;
        proxy.$modal.confirm('是否确认删除合同模版编号为"' + _templateIds + '"的数据项？').then(function () {
            return delTemplate(_templateIds);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('erp/template/export', {
            ...queryParams.value
        }, `template_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
