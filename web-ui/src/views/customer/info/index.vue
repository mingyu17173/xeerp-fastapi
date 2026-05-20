<template>
  <div class="app-container">
    <header-view
      :ftTop="'8'"
      placeholder="请输入客户/手机/邮箱"
      show-search
      :iconClass="'customer'"
      label="客户信息"
      @search="handleQuery">
      <template v-slot:ft>
          <el-button type="primary" @click="handleAdd">添加新客户</el-button>
          <el-dropdown
              v-if="headerMoreHandle.length > 0"
              trigger="click"
              style="margin-left: 5px; margin-right: 10px;"
              @command="headerMoreHandleClick">
              <el-button color="#f1f1f1">
                  <el-icon size="20">
                      <more-filled/>
                  </el-icon>xingx
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
          <RefreshView style="margin-right: 20px;" @click="resetQuery"></RefreshView>
          <ShowFilter :columns="showColumn"></ShowFilter>
      </template>
    </header-view>

    <el-row :gutter="20" style="margin: 15px 0px">
      <el-col :span="24">
        <el-table v-loading="loading" border stripe :data="infoList" style="width: 100%;" show-header @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55" align="center" />
          <el-table-column label="客户名称" align="left" fixed prop="customerName" sortable width="250">
            <template #default="scope">
              <el-tooltip class="item" effect="dark" :content="'#'+scope.row.customerId+ '   '+scope.row.customerName" placement="top-start">
                  <a style="color: #0052cc !important; text-overflow:ellipsis; white-space: nowrap; overflow:hidden; width:100%; padding:5px 0px; display: block;" @click="OpenDetail(scope.row)" :title="scope.row.customerName">{{ scope.row.customerName }}</a>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="社会信用代码" align="center" prop="customerTaxId" width="180" />
          <el-table-column label="开户银行" align="center" prop="depositBank" width="180"  />
          <el-table-column label="银行账号" align="center" prop="bankAccount" width="180"  />
          <el-table-column label="联系人" align="center" prop="contactPerson" />
          <el-table-column label="联系电话" align="center" prop="contactNumber" width="120" />
          <el-table-column label="联系邮箱" align="center" prop="contactEmail" width="180" />
          <el-table-column label="企业地址" align="center" prop="contactAddress" width="300"  />
          <el-table-column label="结算方式" align="center" prop="settlementName" />
          <el-table-column label="使用状态" align="center" prop="useStatusName" />
          <el-table-column label="备注" align="center" prop="remark" width="180"  />
          <el-table-column label="点击次数" align="center" prop="clickNumber" />
          <el-table-column label="创建者" align="center" prop="createByName" />
          <el-table-column label="创建时间" align="center" prop="createTime" width="180" />
        </el-table>
        <div class="p-contianer">
          <pagination
              :page-sizes="[12, 20, 30, 40, 50, 100]"
              v-show="total > 0"
              :total="total"
              v-model:page="queryParams.pageNum"
              v-model:limit="queryParams.pageSize"
              @pagination="getList" />
        </div>
       </el-col>
    </el-row>
    

    <!-- 添加或修改客户信息对话框 -->
    <DetailViews v-model="open" :customerData="customerData" @closeHandle="cancel"></DetailViews>

  </div>
</template>

<script setup name="Info">
import HeaderView from "@/components/HeaderView";
import RefreshView from '@/components/RefreshView'
import DetailViews from "../components/custom_detail.vue";

import ShowFilter from '@/components/showFilter'


import { listInfo, getInfo, delInfo, addInfo, updateInfo } from "@/api/customer/info";

const { proxy } = getCurrentInstance();
const {settlement_mode, use_status} = proxy.useDict("settlement_mode", "use_status");

const infoList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const customerData = ref({});



const showColumn = ref([
    {
        label: "客户名称",
        prop: "customerName",
        width: 300,
        showOverflowTooltip: true
    },
    {
        label: "社会信用代码",
        prop: "customerTaxId",
        width: 180,
        showOverflowTooltip: true
    },
    {
        label: "开户银行",
        prop: "depositBank",
        width: 180,
        showOverflowTooltip: true
    },
    {
        label: "银行账号",
        prop: "bankAccount",
        width: 180,
        showOverflowTooltip: true
    },
    {
        label: "联系人",
        prop: "contactPerson",
        width: 110
    },
    {
        label: "联系电话",
        prop: "contactNumber",
        width: 110
    },
    {
        label: "联系邮箱",
        prop: "contactEmail",
        width: 180,
        showOverflowTooltip: true
    },
    {
        label: "企业地址",
        prop: "contactAddress",
        width: 300,
        showOverflowTooltip: true
    },
    {
        label: "结算方式",
        prop: "settlementMode",
        width: 110
    },
    {
        label: "使用状态",
        prop: "useStatus",
        width: 110
    },
    {
        label: "备注",
        prop: "remark",
        width: 180,
        showOverflowTooltip: true
    },
    {
        label: "点击次数",
        prop: "clickNumber",
        width: 110
    },
    {
        label: "创建者",
        prop: "createBy",
        width: 110
    },
    {
        label: "创建时间",
        prop: "createTime",
        width: 180
    },
    {
        label: "操作",
        prop: "operation",
        width: 110
    }
])

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
    pageSize: 12,
    customerName: null,
    customerTaxId: null,
    depositBank: null,
    bankAccount: null,
    contactPerson: null,
    contactNumber: null,
    contactEmail: null,
    contactAddress: null,
    settlementMode: "0",
    useStatus: null,
    clickNumber: null,
    dataRealm: null,
    parkCode: null,
  },
  rules: {
    customerName: [
      { required: true, message: "客户名称不能为空", trigger: "blur" }
    ],
    delFlag: [
      { required: true, message: "删除标识 不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询客户信息列表 */
function getList() {
  loading.value = true;
  listInfo(queryParams.value).then(response => {
    infoList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel(res) {
  open.value = res;
  reset();
}


/**打开详情 */
function OpenDetail(res) {
    customerData.value = res
    open.value = true
}

/** 表单重置 */
function reset() {
  form.value = {
    customerId: null,
    customerName: null,
    customerTaxId: null,
    depositBank: null,
    bankAccount: null,
    contactPerson: null,
    contactNumber: null,
    contactEmail: null,
    contactAddress: null,
    settlementMode: null,
    useStatus: null,
    remark: null,
    clickNumber: null,
    dataRealm: null,
    parkCode: null,
    delFlag: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("infoRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据  */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.customerId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

  /** 新增按钮操作 */
  function handleAdd() {
    reset();
    open.value = true;
    title.value = "添加客户信息";
  }

  /** 修改按钮操作 */
  function handleUpdate(row) {
    reset();
    const _customerId = row.customerId || ids.value;
    getInfo(_customerId).then(response => {
      form.value = response.data;
      open.value = true;
      title.value = "修改客户信息";
    });
  }

  /** 提交按钮 */
  function submitForm() {
    proxy.$refs["infoRef"].validate(valid => {
      if (valid) {
        if (form.value.customerId != null) {
          updateInfo(form.value).then(response => {
            proxy.$modal.msgSuccess("修改成功");
            open.value = false;
            getList();
          });
        } else {
          addInfo(form.value).then(response => {
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
    const _customerIds = row.customerId || ids.value;
    proxy.$modal.confirm('是否确认删除客户信息编号为"' + _customerIds + '"的数据项？').then(function() {
      return delInfo(_customerIds);
    }).then(() => {
      getList();
      proxy.$modal.msgSuccess("删除成功");
    }).catch(() => {});
  }


  /** 导出按钮操作 */
  function handleExport() {
    proxy.download('system/info/export', {
      ...queryParams.value
    }, `info_${new Date().getTime()}.xlsx`);
  }

  /** 是否渲染字段 */
  function renderField(insert, edit) {
    return form.value.customerId == null ? insert : edit;
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

  onMounted(() => {
    getList();
  })

</script>