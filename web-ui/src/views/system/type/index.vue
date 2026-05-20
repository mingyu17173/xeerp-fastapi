<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入单据类型"
                show-search
                label="单据类型"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="handleAdd" v-hasPermi="['system:type:add']">新建单据类型</el-button>
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
                            <el-form-item label="单据类型名称" prop="documentName">
                                <el-input
                                        v-model="queryParams.documentName"
                                        placeholder="请输入单据类型名称"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="前缀" prop="prefix">
                                <el-input
                                        v-model="queryParams.prefix"
                                        placeholder="请输入前缀"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="时间戳格式" prop="timeFormat">
                                <el-input
                                        v-model="queryParams.timeFormat"
                                        placeholder="请输入时间戳格式"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="连接符号" prop="joinMark">
                                <el-input
                                        v-model="queryParams.joinMark"
                                        placeholder="请输入连接符号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="起始序列号" prop="startSequence">
                                <el-input
                                        v-model="queryParams.startSequence"
                                        placeholder="请输入起始序列号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="下一个序列号" prop="nextSequence">
                                <el-input
                                        v-model="queryParams.nextSequence"
                                        placeholder="请输入下一个序列号"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="序号重新编号方式" prop="sequenceReset">
                                <el-input
                                        v-model="queryParams.sequenceReset"
                                        placeholder="请输入序号重新编号方式"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="后缀" prop="suffix">
                                <el-input
                                        v-model="queryParams.suffix"
                                        placeholder="请输入后缀"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="单据版本号，订单号新增时判断" prop="version">
                                <el-input
                                        v-model="queryParams.version"
                                        placeholder="请输入单据版本号，订单号新增时判断"
                                        clearable
                                        @keyup.enter="handleQuery"
                                />
                            </el-form-item>
                            <el-form-item label="账期受控" prop="periodControl">
                                <el-input
                                        v-model="queryParams.periodControl"
                                        placeholder="请输入账期受控"
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
                <el-table v-loading="loading" :data="typeList" border stripe show-header highlight-current-row
                          @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <el-table-column label="单据类型id" align="center" prop="id"/>
                    <el-table-column label="单据类型编号" align="center" prop="documentType"/>
                    <el-table-column label="单据类型名称" align="center" prop="documentName"/>
                    <el-table-column label="前缀" align="center" prop="prefix"/>
                    <el-table-column label="时间戳格式" align="center" prop="timeFormat"/>
                    <el-table-column label="连接符号" align="center" prop="joinMark"/>
                    <el-table-column label="起始序列号" align="center" prop="startSequence"/>
                    <el-table-column label="下一个序列号" align="center" prop="nextSequence"/>
                    <el-table-column label="序号重新编号方式" align="center" prop="sequenceReset"/>
                    <el-table-column label="后缀" align="center" prop="suffix"/>
                    <el-table-column label="备注" align="center" prop="remark"/>
                    <el-table-column label="单据版本号，订单号新增时判断" align="center" prop="version"/>
                    <el-table-column label="账期受控" align="center" prop="periodControl"/>
                    <el-table-column label="创建人id" align="center" prop="createUid"/>
                    <el-table-column label="操作" fixed="right" width="180" align="center"
                                     class-name="small-padding fixed-width">
                        <template #default="scope">
                            <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                                       v-hasPermi="['system:type:edit']">修改
                            </el-button>
                            <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                                       v-hasPermi="['system:type:remove']">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div class="p-contianer">
                    <pagination
                            v-show="total>0"
                            :total="total"
                            v-model:page="queryParams.pageNum"
                            v-model:limit="queryParams.pageSize"
                            @pagination="getList"
                    />
                </div>
            </el-col>
        </el-row>
        <!-- 添加或修改单据类型对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="typeRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="单据类型名称" prop="documentName">
                    <el-input v-model="form.documentName" placeholder="请输入单据类型名称"/>
                </el-form-item>
                <el-form-item label="前缀" prop="prefix">
                    <el-input v-model="form.prefix" placeholder="请输入前缀"/>
                </el-form-item>
                <el-form-item label="时间戳格式" prop="timeFormat">
                    <el-input v-model="form.timeFormat" placeholder="请输入时间戳格式"/>
                </el-form-item>
                <el-form-item label="连接符号" prop="joinMark">
                    <el-input v-model="form.joinMark" placeholder="请输入连接符号"/>
                </el-form-item>
                <el-form-item label="起始序列号" prop="startSequence">
                    <el-input v-model="form.startSequence" placeholder="请输入起始序列号"/>
                </el-form-item>
                <el-form-item label="下一个序列号" prop="nextSequence">
                    <el-input v-model="form.nextSequence" placeholder="请输入下一个序列号"/>
                </el-form-item>
                <el-form-item label="序号重新编号方式" prop="sequenceReset">
                    <el-input v-model="form.sequenceReset" placeholder="请输入序号重新编号方式"/>
                </el-form-item>
                <el-form-item label="后缀" prop="suffix">
                    <el-input v-model="form.suffix" placeholder="请输入后缀"/>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="form.remark" placeholder="请输入备注"/>
                </el-form-item>
                <el-form-item label="单据版本号，订单号新增时判断" prop="version">
                    <el-input v-model="form.version" placeholder="请输入单据版本号，订单号新增时判断"/>
                </el-form-item>
                <el-form-item label="账期受控" prop="periodControl">
                    <el-input v-model="form.periodControl" placeholder="请输入账期受控"/>
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

<script setup name="Type">
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'
    import {listType, getType, delType, addType, updateType} from "@/api/system/type";

    const {proxy} = getCurrentInstance();

    const typeList = ref([]);
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
            pageSize: 10,
            documentType: null,
            documentName: null,
            prefix: null,
            timeFormat: null,
            joinMark: null,
            startSequence: null,
            nextSequence: null,
            sequenceReset: null,
            suffix: null,
            version: null,
            periodControl: null,
            createUid: null
        },
        rules: {}
    });

    const showColumn = ref([
        {label: "单据类型编号", value: "documentType"},
        {label: "单据类型名称", value: "documentName"},
        {label: "前缀", value: "prefix"},
        {label: "时间戳格式", value: "timeFormat"},
        {label: "连接符号", value: "joinMark"},
        {label: "起始序列号", value: "startSequence"},
        {label: "下一个序列号", value: "nextSequence"},
        {label: "序号重新编号方式（D：每天重新编号，M：每月重新编号，N：不重新编号）", value: "sequenceReset"},
        {label: "后缀", value: "suffix"},
        {label: "单据版本号，订单号新增时判断", value: "version"},
        {label: "账期受控（Y受控，N不受控）", value: "periodControl"},
        {label: "创建人id", value: "createUid"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 查询单据类型列表 */
    function getList() {
        loading.value = true;
        listType(queryParams.value).then(response => {
            typeList.value = response.rows;
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
            documentType: null,
            documentName: null,
            prefix: null,
            timeFormat: null,
            joinMark: null,
            startSequence: null,
            nextSequence: null,
            sequenceReset: null,
            suffix: null,
            remark: null,
            version: null,
            periodControl: null,
            createTime: null,
            createUid: null
        };
        proxy.resetForm("typeRef");
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        queryParams.value.documentType = res,
            queryParams.value.documentName = res,
            queryParams.value.prefix = res,
            queryParams.value.timeFormat = res,
            queryParams.value.joinMark = res,
            queryParams.value.startSequence = res,
            queryParams.value.nextSequence = res,
            queryParams.value.sequenceReset = res,
            queryParams.value.suffix = res,
            queryParams.value.version = res,
            queryParams.value.periodControl = res,
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
        title.value = "添加单据类型";
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
        getType(_id).then(response => {
            form.value = response.data;
            open.value = true;
            title.value = "修改单据类型";
        });
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["typeRef"].validate(valid => {
            if (valid) {
                if (form.value.id != null) {
                    updateType(form.value).then(response => {
                        proxy.$modal.msgSuccess("修改成功");
                        open.value = false;
                        getList();
                    });
                } else {
                    addType(form.value).then(response => {
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
        proxy.$modal.confirm('是否确认删除单据类型编号为"' + _ids + '"的数据项？').then(function () {
            return delType(_ids);
        }).then(() => {
            getList();
            proxy.$modal.msgSuccess("删除成功");
        }).catch(() => {
        });
    }

    /** 导出按钮操作 */
    function handleExport() {
        proxy.download('system/type/export', {
            ...queryParams.value
        }, `type_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
