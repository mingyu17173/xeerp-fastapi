<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入流程定义"
                show-search
                label="流程定义"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['system:process:add']">新建流程定义</el-button>
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
                            <el-form-item label="租户ID" prop="tenantId">
                                <el-input
                                        v-model="queryParams.tenantId"
                                        placeholder="请输入租户ID"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="创建人ID" prop="createId">
                                <el-input
                                        v-model="queryParams.createId"
                                        placeholder="请输入创建人ID"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="流程定义 key 唯一标识" prop="processKey">
                                <el-input
                                        v-model="queryParams.processKey"
                                        placeholder="请输入流程定义 key 唯一标识"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="流程定义名称" prop="processName">
                                <el-input
                                        v-model="queryParams.processName"
                                        placeholder="请输入流程定义名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="流程图标地址" prop="processIcon">
                                <el-input
                                        v-model="queryParams.processIcon"
                                        placeholder="请输入流程图标地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="流程版本，默认 1" prop="processVersion">
                                <el-input
                                        v-model="queryParams.processVersion"
                                        placeholder="请输入流程版本，默认 1"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="实例地址" prop="instanceUrl">
                                <el-input
                                        v-model="queryParams.instanceUrl"
                                        placeholder="请输入实例地址"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="使用范围 0，全员 1，指定人员" prop="useScope">
                                <el-input
                                        v-model="queryParams.useScope"
                                        placeholder="请输入使用范围 0，全员 1，指定人员"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="流程状态 0，不可用 1，可用 2，历史版本" prop="processState">
                                <el-input
                                        v-model="queryParams.processState"
                                        placeholder="请输入流程状态 0，不可用 1，可用 2，历史版本"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="排序" prop="sort">
                                <el-input
                                        v-model="queryParams.sort"
                                        placeholder="请输入排序"
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
                <el-table v-loading="loading" :data="processList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="主键ID" align="center" prop="id"/>
                    <el-table-column label="租户ID" align="center" prop="tenantId"/>
                    <el-table-column label="创建人ID" align="center" prop="createId"/>
                    <el-table-column label="流程定义 key 唯一标识" align="center" prop="processKey"/>
                    <el-table-column label="流程定义名称" align="center" prop="processName"/>
                    <el-table-column label="流程图标地址" align="center" prop="processIcon"/>
                    <el-table-column label="流程类型" align="center" prop="processType"/>
                    <el-table-column label="流程版本，默认 1" align="center" prop="processVersion"/>
                    <el-table-column label="实例地址" align="center" prop="instanceUrl"/>
                    <el-table-column label="备注说明" align="center" prop="remark"/>
                    <el-table-column label="使用范围 0，全员 1，指定人员" align="center" prop="useScope"/>
                    <el-table-column label="流程状态 0，不可用 1，可用 2，历史版本" align="center" prop="processState"/>
                    <el-table-column label="流程模型定义JSON内容" align="center" prop="modelContent"/>
                    <el-table-column label="排序" align="center" prop="sort"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['system:process:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['system:process:remove']">删除
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
        <!-- 添加或修改流程定义对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="processRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="租户ID" prop="tenantId">
                    <el-input v-model="form.tenantId" placeholder="请输入租户ID"/>
                </el-form-item>
                <el-form-item label="创建人ID" prop="createId">
                    <el-input v-model="form.createId" placeholder="请输入创建人ID"/>
                </el-form-item>
                <el-form-item label="流程定义 key 唯一标识" prop="processKey">
                    <el-input v-model="form.processKey" placeholder="请输入流程定义 key 唯一标识"/>
                </el-form-item>
                <el-form-item label="流程定义名称" prop="processName">
                    <el-input v-model="form.processName" placeholder="请输入流程定义名称"/>
                </el-form-item>
                <el-form-item label="流程图标地址" prop="processIcon">
                    <el-input v-model="form.processIcon" placeholder="请输入流程图标地址"/>
                </el-form-item>
                <el-form-item label="流程版本，默认 1" prop="processVersion">
                    <el-input v-model="form.processVersion" placeholder="请输入流程版本，默认 1"/>
                </el-form-item>
                <el-form-item label="实例地址" prop="instanceUrl">
                    <el-input v-model="form.instanceUrl" placeholder="请输入实例地址"/>
                </el-form-item>
                <el-form-item label="备注说明" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注说明"/>
                </el-form-item>
                <el-form-item label="使用范围 0，全员 1，指定人员" prop="useScope">
                    <el-input v-model="form.useScope" placeholder="请输入使用范围 0，全员 1，指定人员"/>
                </el-form-item>
                <el-form-item label="流程状态 0，不可用 1，可用 2，历史版本" prop="processState">
                    <el-input v-model="form.processState" placeholder="请输入流程状态 0，不可用 1，可用 2，历史版本"/>
                </el-form-item>
                <el-form-item label="流程模型定义JSON内容">
                    <editor v-model="form.modelContent" :min-height="192"/>
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input v-model="form.sort" placeholder="请输入排序"/>
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

<script setup name="Process">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listProcess, getProcess, delProcess, addProcess, updateProcess} from "@/api/system/process";

    const {proxy} = getCurrentInstance();

    const processList = ref([]);
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
            tenantId: null,
            createId: null,
            processKey: null,
            processName: null,
            processIcon: null,
            processType: null,
            processVersion: null,
            instanceUrl: null,
            useScope: null,
            processState: null,
            modelContent: null,
            sort: null
        },
        rules: {
            createId: [
                {required: true, message: "创建人ID不能为空", trigger: "blur"}
            ],
            createBy: [
                {required: true, message: "创建人名称不能为空", trigger: "blur"}
            ],
            createTime: [
                {required: true, message: "创建时间不能为空", trigger: "blur"}
            ],
            processKey: [
                {required: true, message: "流程定义 key 唯一标识不能为空", trigger: "blur"}
            ],
            processName: [
                {required: true, message: "流程定义名称不能为空", trigger: "blur"}
            ],
            processVersion: [
                {required: true, message: "流程版本，默认 1不能为空", trigger: "blur"}
            ],
            useScope: [
                {required: true, message: "使用范围 0，全员 1，指定人员不能为空", trigger: "blur"}
            ],
            processState: [
                {required: true, message: "流程状态 0，不可用 1，可用 2，历史版本不能为空", trigger: "blur"}
            ],
        }
    });

    const showColumn = ref([
        {label: "租户ID", value: "tenantId"},
        {label: "创建人ID", value: "createId"},
        {label: "流程定义 key 唯一标识", value: "processKey"},
        {label: "流程定义名称", value: "processName"},
        {label: "流程图标地址", value: "processIcon"},
        {label: "流程类型", value: "processType"},
        {label: "流程版本，默认 1", value: "processVersion"},
        {label: "实例地址", value: "instanceUrl"},
        {label: "使用范围 0，全员 1，指定人员（业务关联） 2，均不可提交", value: "useScope"},
        {label: "流程状态 0，不可用 1，可用 2，历史版本", value: "processState"},
        {label: "流程模型定义JSON内容", value: "modelContent"},
        {label: "排序", value: "sort"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询流程定义列表 */
    function getList() {
        loading.value = true;
        listProcess(queryParams.value).then(response => {
            processList.value = response.rows;
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
            tenantId: null,
            createId: null,
            createBy: null,
            createTime: null,
            processKey: null,
            processName: null,
            processIcon: null,
            processType: null,
            processVersion: null,
            instanceUrl: null,
            remark: null,
            useScope: null,
            processState: null,
            modelContent: null,
            sort: null
        };
        proxy.resetForm("processRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.tenantId = res,
            queryParams.value.createId = res,
            queryParams.value.processKey = res,
            queryParams.value.processName = res,
            queryParams.value.processIcon = res,
            queryParams.value.processType = res,
            queryParams.value.processVersion = res,
            queryParams.value.instanceUrl = res,
            queryParams.value.useScope = res,
            queryParams.value.processState = res,
            queryParams.value.modelContent = res,
            queryParams.value.sort = res,
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
        title.value = "添加流程定义";
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
        getProcess(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改流程定义";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["processRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateProcess(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addProcess(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除流程定义编号为"' + _ids + '"的数据项？').then(function () {
            return delProcess(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('system/process/export', {
            ...queryParams.value
        }, `process_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
